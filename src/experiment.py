"""IEEE-CIS separado do M5. Classificação, regressão, agrupamento e decisão.

Uma observação é uma transação. O alvo de regressão Amount*isFraud é exposição
monetária rotulada, não perda líquida observada. Políticas de revisão têm a MESMA
capacidade diária e custos/eficácia assumidos. Nenhum resultado é lucro realizado.
"""
from pathlib import Path
import os,sys,json,time,hashlib,platform,warnings
ROOT=Path(__file__).resolve().parents[1]
# Dependência local usada só neste ambiente; num venv, requirements.txt basta.
if (ROOT/'work/python_packages').exists():sys.path.insert(0,str(ROOT/'work/python_packages'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'work/matplotlib'))
os.environ.setdefault('OMP_NUM_THREADS','4')
import numpy as np,pandas as pd
import pyarrow.parquet as pq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression,Ridge,Lasso,LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (HistGradientBoostingClassifier,
 RandomForestRegressor,HistGradientBoostingRegressor)
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (mean_absolute_error,mean_squared_error,r2_score,accuracy_score,precision_score,
 recall_score,f1_score,roc_auc_score,average_precision_score,brier_score_loss,confusion_matrix,
 silhouette_score,davies_bouldin_score,adjusted_rand_score,roc_curve,precision_recall_curve)
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
from sklearn.decomposition import PCA
from sklearn.inspection import permutation_importance
from sklearn.calibration import calibration_curve
from scipy.special import expit,logit
SEED=42
# Lista definida antes de olhar o teste, sem seleção supervisionada de atributos.
NUM=['TransactionAmt','dist1','dist2']+[f'C{i}' for i in range(1,15)]+[f'D{i}' for i in range(1,16)]+[f'V{i}' for i in [1,3,5,7,13,20,30,50,70,100,130,150,200,250,300]]+['hour_sin','hour_cos','missing_count']
CAT=['ProductCD','card1','card2','card3','card4','card5','card6','addr1','addr2','P_emaildomain','R_emaildomain','M1','M2','M3','M4','M5','M6','M7','M8','M9','DeviceType']
CONFIG=dict(curricular_revision='15 techniques; test period previously inspected in earlier version; retrospective evaluation, not a fresh holdout',seed=42,sample='every fifth source row; no stratification',training_budget=30000,
 timeline='whole relative days 60% train,15% validation,10% calibration,15% test',
 capacity=.02,cost=2.,efficacy=.8,false_positive_penalty=0.,
 selection_classifier='largest labeled fraud amount captured with 2% daily review in validation',
 selection_regressor='smallest validation MSE; target TransactionAmt*isFraud',
 monetary_unit='USD according to Empulse documentation; no conversion to BRL')

def save(obj,name):
 (ROOT/'results'/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str))

def preprocess(num=None):
 return ColumnTransformer([
  ('numeric',Pipeline([('impute',SimpleImputer(strategy='median',add_indicator=True,keep_empty_features=True)),('scale',StandardScaler())]),NUM if num is None else num),
  ('categorical',OneHotEncoder(handle_unknown='infrequent_if_exist',min_frequency=50,max_categories=15,sparse_output=False),CAT)])

def build_dataset():
 path=ROOT/'data/raw/ieee_cis.parquet';schema=pq.ParquetFile(path).schema.names
 cols=[c for c in NUM+CAT+['TransactionDT','isFraud'] if c in schema]
 raw=pd.read_parquet(path,columns=cols)
 raw['source_row']=np.arange(len(raw));raw['isFraud']=raw.isFraud.astype(float).astype(int)
 audit=dict(raw_rows=len(raw),raw_frauds=int(raw.isFraud.sum()),raw_fields=len(schema),
 raw_time_min=int(raw.TransactionDT.min()),raw_time_max=int(raw.TransactionDT.max()),
 raw_missing_fraction=float(raw[cols].isna().mean().mean()),transaction_id_present='TransactionID' in schema)
 # Seleção sistemática, não pelo rótulo nem pelo valor. Preserva a ordem observada.
 d=raw[raw.source_row%5==0].copy()
 d['day']=((d.TransactionDT-audit['raw_time_min'])//86400).astype(int)
 maxday=int(d.day.max())
 # Exclui extremos incompletos para comparar orçamentos em dias inteiros interiores.
 d=d[(d.day>0)&(d.day<maxday)].copy()
 cut=[int(maxday*.60),int(maxday*.75),int(maxday*.85)]
 d['split']=np.select([d.day<cut[0],d.day<cut[1],d.day<cut[2]],['train','validation','calibration'],default='test')
 hour=(d.TransactionDT%86400)/3600
 d['hour_sin']=np.sin(2*np.pi*hour/24);d['hour_cos']=np.cos(2*np.pi*hour/24)
 d['missing_count']=d[[c for c in cols if c not in ['isFraud','TransactionDT']]].isna().sum(axis=1)
 for c in CAT:d[c]=d[c].astype('object').where(d[c].notna(),'__MISSING__').astype(str)
 d['exposure']=d.TransactionAmt*d.isFraud
 d=d.sort_values(['TransactionDT','source_row']).reset_index(drop=True)
 assert set(NUM+CAT).issubset(d.columns)
 assert not set(['isFraud','exposure','TransactionDT','day','source_row']).intersection(NUM+CAT)
 assert (d.TransactionAmt>0).all() and d.isFraud.isin([0,1]).all()
 audit.update(sample_rows=len(d),sample_frauds=int(d.isFraud.sum()),sample_fraction=len(d)/len(raw),cut_days=cut,
 sample_fraud_amount=float(d.exposure.sum()),days=d.day.nunique(),
 duplicated_selected_feature_vectors=int(d.duplicated(NUM+CAT+['TransactionDT','isFraud']).sum()),
 splits=d.groupby('split').agg(n=('isFraud','size'),days=('day','nunique'),start=('day','min'),end=('day','max'),frauds=('isFraud','sum'),amount=('exposure','sum')).reset_index().to_dict('records'))
 d.to_parquet(ROOT/'data/processed/transactions.parquet',index=False)
 d[['source_row','TransactionDT','day','split','isFraud','TransactionAmt','exposure']].to_csv(ROOT/'data/processed/decision_metadata.csv',index=False)
 pd.DataFrame({'feature':NUM+CAT,'missing_fraction':d[d.split=='train'][NUM+CAT].replace('__MISSING__',np.nan).isna().mean()}).to_csv(ROOT/'results/missing_features.csv',index=False)
 save(audit,'audit.json');save(CONFIG,'config.json')
 sha=hashlib.sha256(path.read_bytes()).hexdigest()
 save(dict(original='https://www.kaggle.com/competitions/ieee-fraud-detection/data',mirror='https://data.openml.org/datasets/0004/46858/dataset_46858.pq',openml_id=46858,
 loader_reference='https://empulse.readthedocs.io/en/latest/guide/datasets/ieee_fraud_detection.html',
 sha256=sha,bytes=path.stat().st_size,note='Local parquet hash; OpenML MD5 refers to ARFF, not verified against parquet'), 'provenance.json')
 return d,audit

def budget_sample(d):
 return d.sample(min(CONFIG['training_budget'],len(d)),random_state=SEED).sort_values(['day','source_row'])

def folds(train):
 days=np.sort(train.day.unique())
 for frac in [.65,.80,.95]:
  end=max(1,int(len(days)*frac)); start=max(1,end-10)
  tr=train.day<days[start];va=train.day.isin(days[start:end])
  assert train.loc[tr,'day'].max()<train.loc[va,'day'].min()
  yield train.index[tr],train.index[va]

def review_mask(d,score,capacity=.02):
 """Ranking diário; empates por linha de origem, nunca pelo rótulo."""
 s=pd.Series(np.asarray(score),index=d.index)
 assert np.isfinite(s).all()
 selected=pd.Series(False,index=d.index)
 for day,g in d.groupby('day',sort=True):
  k=int(np.ceil(capacity*len(g)))
  order=pd.DataFrame({'score':s.loc[g.index],'source_row':g.source_row}).sort_values(['score','source_row'],ascending=[False,True],kind='stable')
  selected.loc[order.index[:k]]=True
 return selected.to_numpy()

def financial(d,mask,cost=2.,efficacy=.8,fp_penalty=0.):
 y=d.isFraud.to_numpy();a=d.TransactionAmt.to_numpy();mask=np.asarray(mask)
 captured=float(np.sum(mask*y*a));n=int(mask.sum());fp=int(np.sum(mask*(1-y)))
 baseline=float(np.sum(y*a))
 net=efficacy*captured-cost*n-fp_penalty*fp
 return dict(reviewed=n,fraud_reviewed=int(np.sum(mask*y)),legitimate_reviewed=fp,
  precision=float(np.sum(mask*y)/max(n,1)),recall=float(np.sum(mask*y)/max(y.sum(),1)),
  labeled_amount_captured=captured,amount_recall=captured/max(baseline,1),
  review_cost=cost*n,net_benefit=net,total_loss=baseline-net,no_action_loss=baseline)

def reg_metrics(y,p):
 return dict(MAE=float(mean_absolute_error(y,p)),MSE=float(mean_squared_error(y,p)),RMSE=float(np.sqrt(mean_squared_error(y,p))),R2=float(r2_score(y,p)))
def cls_metrics(y,p,t):
 pred=p>=t
 return dict(accuracy=float(accuracy_score(y,pred)),precision=float(precision_score(y,pred,zero_division=0)),recall=float(recall_score(y,pred,zero_division=0)),F1=float(f1_score(y,pred,zero_division=0)),ROC_AUC=float(roc_auc_score(y,p)),AP=float(average_precision_score(y,p)),Brier=float(brier_score_loss(y,p)),threshold=float(t))

def specs(task):
 if task=='classification':
  return {
  'Logistic':(LogisticRegression(max_iter=600),[{'C':.1},{'C':1.}]),
  # LDA regularizado: covariância compartilhada; shrinkage reduz singularidade no one-hot.
  'LDA':(LinearDiscriminantAnalysis(solver='lsqr'),[{'shrinkage':.1},{'shrinkage':'auto'}]),
  'HistGradientBoosting':(HistGradientBoostingClassifier(max_iter=120,random_state=SEED),[{'max_leaf_nodes':15,'l2_regularization':10.},{'max_leaf_nodes':31,'l2_regularization':20.}]),
  'KNN':(KNeighborsClassifier(n_jobs=4),[{'n_neighbors':15},{'n_neighbors':45}]),
  'GaussianNB':(GaussianNB(),[{'var_smoothing':1e-5},{'var_smoothing':1e-3}])}
 return {
  'Linear':(LinearRegression(),[{}]),'Ridge':(Ridge(),[{'alpha':10.},{'alpha':100.}]),
  'Lasso':(Lasso(max_iter=1500),[{'alpha':.1},{'alpha':1.}]),
  'DecisionTree':(DecisionTreeRegressor(random_state=SEED),[{'max_depth':5,'min_samples_leaf':50},{'max_depth':10,'min_samples_leaf':25}]),
  'RandomForest':(RandomForestRegressor(n_estimators=60,n_jobs=4,random_state=SEED),[{'max_depth':10,'min_samples_leaf':10},{'max_depth':15,'min_samples_leaf':5}]),
  'HistGradientBoosting':(HistGradientBoostingRegressor(max_iter=120,random_state=SEED),[{'max_leaf_nodes':15,'l2_regularization':50.},{'max_leaf_nodes':31,'l2_regularization':100.}])}

def train(d,task):
 train=d[d.split=='train'];val=d[d.split=='validation'];ft=d[d.split.isin(['train','validation'])]
 target='isFraud' if task=='classification' else 'exposure'
 metricrows=[];cvrows=[];predrows=[];params={};models={};thresholds={};calibrators={};val_scores={}
 for name,(base,grid) in specs(task).items():
  started=time.time();cand=[]
  for par in grid:
   scores=[]
   for fold,(tri,vai) in enumerate(folds(train),1):
    tr=budget_sample(d.loc[tri]);va=d.loc[vai]
    m=Pipeline([('pre',preprocess()),('model',clone(base).set_params(**par))]);m.fit(tr[NUM+CAT],tr[target])
    if task=='classification':score=-average_precision_score(va.isFraud,m.predict_proba(va[NUM+CAT])[:,1])
    else:score=mean_squared_error(va.exposure,np.maximum(0,m.predict(va[NUM+CAT])))
    scores.append(score);cvrows.append(dict(model=name,params=json.dumps(par),fold=fold,score=score,train_end=int(tr.day.max()),val_start=int(va.day.min())))
   cand.append((np.mean(scores),par))
  par=min(cand,key=lambda x:x[0])[1];params[name]=par
  m=Pipeline([('pre',preprocess()),('model',clone(base).set_params(**par))])
  tr=budget_sample(train);m.fit(tr[NUM+CAT],tr[target])
  if task=='classification':
   pv=m.predict_proba(val[NUM+CAT])[:,1]
   threshold=max(np.linspace(.02,.70,35),key=lambda t:f1_score(val.isFraud,pv>=t,zero_division=0));thresholds[name]=float(threshold)
   f=financial(val,review_mask(val,pv*val.TransactionAmt));val_scores[name]=f['labeled_amount_captured']
   metricrows.append(dict(model=name,split='validation',captured_at_2pct=f['labeled_amount_captured'],**cls_metrics(val.isFraud,pv,threshold)))
  else:
   pv=np.maximum(0,m.predict(val[NUM+CAT]));val_scores[name]=-mean_squared_error(val.exposure,pv)
   metricrows.append(dict(model=name,split='validation',**reg_metrics(val.exposure,pv)))
  # Cada estimador recebe o mesmo sorteio de no máximo 30 mil linhas, sem oversampling.
  tr=budget_sample(ft);m.fit(tr[NUM+CAT],tr[target]);models[name]=m
  cal=d[d.split=='calibration']
  if task=='classification':
   pc=m.predict_proba(cal[NUM+CAT])[:,1]
   platt=LogisticRegression(C=1.,max_iter=500).fit(logit(np.clip(pc,1e-6,1-1e-6)).reshape(-1,1),cal.isFraud)
   calibrators[name]=platt
  for split in ['calibration','test']:
   z=d[d.split==split]
   if task=='classification':
    raw=m.predict_proba(z[NUM+CAT])[:,1]
    p=calibrators[name].predict_proba(logit(np.clip(raw,1e-6,1-1e-6)).reshape(-1,1))[:,1]
    # Métricas operacionais por limiar usam score bruto e limiar congelado; políticas usam calibrado.
    metricrows.append(dict(model=name,split=split,calibrated_Brier=float(brier_score_loss(z.isFraud,p)),**cls_metrics(z.isFraud,raw,thresholds[name])))
   else:raw=p=np.maximum(0,m.predict(z[NUM+CAT]));metricrows.append(dict(model=name,split=split,**reg_metrics(z.exposure,p)))
   assert np.isfinite(raw).all() and np.isfinite(p).all()
   for idx,a,b in zip(z.index,raw,p):predrows.append(dict(row=int(idx),model=name,split=split,raw=float(a),prediction=float(b)))
  print(task,name,round(time.time()-started,1),'s',flush=True)
 winner=max(val_scores,key=val_scores.get)
 pd.DataFrame(metricrows).to_csv(ROOT/f'results/{task}_metrics.csv',index=False)
 pd.DataFrame(cvrows).to_csv(ROOT/f'results/{task}_cv.csv',index=False)
 pred=pd.DataFrame(predrows);pred.to_csv(ROOT/f'results/{task}_predictions.csv',index=False)
 save(dict(winner=winner,params=params,thresholds=thresholds,validation_selection_scores=val_scores,
  budget_final=len(budget_sample(ft))),f'{task}_selection.json')
 return pd.DataFrame(metricrows),pred,models,winner,calibrators

def policies(d,cp,rp,cwin,rwin):
 z=d[d.split=='test'];cal=d[d.split=='calibration']
 def get(pred,name,split,rows):return pred[(pred.model==name)&(pred.split==split)].set_index('row').loc[rows.index,'prediction'].to_numpy()
 pc=get(cp,cwin,'test',z);pr=get(rp,rwin,'test',z)
 # Score aleatório determinístico, independente de valor e rótulo.
 rand=np.random.default_rng(SEED).random(len(z))
 # Regra simples de taxa histórica por ProductCD, suavizada com prevalência global.
 tr=d[d.split=='train'];globalrate=tr.isFraud.mean();g=tr.groupby('ProductCD').isFraud.agg(['sum','size'])
 rates=(g['sum']+100*globalrate)/(g['size']+100)
 # Refit da regra simples também recebe treino + validação, como os modelos.
 ft=d[d.split.isin(['train','validation'])];ftrate=ft.isFraud.mean()
 fg=ft.groupby('ProductCD').isFraud.agg(['sum','size'])
 frates=(fg['sum']+100*ftrate)/(fg['size']+100)
 group=z.ProductCD.map(frates).fillna(ftrate).to_numpy()*z.TransactionAmt.to_numpy()
 scores={'Random':rand,'LargestAmount':z.TransactionAmt.to_numpy(),'ProductRateAmount':group,
         'ML_Probability':pc,'ML_ExpectedAmount':pc*z.TransactionAmt.to_numpy(),'RegressionExposure':pr}
 rows=[];detail=[]
 for cap in [.01,.02,.05,.10]:
  for name,score in scores.items():
   mask=review_mask(z,score,cap)
   # Custos monetários e eficácia são cenários, sem reotimizar scores no teste.
   for scenario,cost,eff,fp in [('central',2.,.8,0.),('low_efficacy',2.,.5,0.),('high_cost',10.,.8,0.),('fp_penalty',2.,.8,10.)]:
    f=financial(z,mask,cost,eff,fp)
    rows.append(dict(policy=name,capacity=cap,scenario=scenario,cost=cost,efficacy=eff,fp_penalty=fp,**f))
   part=z[['source_row','day','isFraud','TransactionAmt','exposure']].copy();part['review']=mask;part['policy']=name;part['capacity']=cap
   detail.append(part)
 table=pd.DataFrame(rows);det=pd.concat(detail,ignore_index=True)
 table.to_csv(ROOT/'results/financial_policies.csv',index=False);det.to_parquet(ROOT/'results/policy_detail.parquet',index=False)
 # Baseline comparador escolhido na validação, antes de olhar o resultado do teste.
 va=d[d.split=='validation'];rng=np.random.default_rng(SEED);vscore={'Random':rng.random(len(va)),'LargestAmount':va.TransactionAmt.to_numpy(),
 'ProductRateAmount':va.ProductCD.map(rates).fillna(globalrate).to_numpy()*va.TransactionAmt.to_numpy()}
 valbase=[]
 for name,score in vscore.items():valbase.append(dict(policy=name,**financial(va,review_mask(va,score))))
 base=max(valbase,key=lambda r:r['net_benefit'])['policy']
 save(dict(comparator=base,validation=valbase),'baseline_selection.json')
 # Política principal definida a priori: probabilidade calibrada * valor, capacidade 2%.
 main='ML_ExpectedAmount';q=det[det.capacity==.02].copy()
 q['benefit']=q.review*(.8*q.exposure-2.)
 wide=q.groupby(['day','policy']).benefit.sum().unstack();delta=(wide[main]-wide[base]).to_numpy();n=len(delta)
 rng=np.random.default_rng(SEED);boot=[]
 for _ in range(5000):
  starts=rng.integers(0,n,size=int(np.ceil(n/7)));idx=np.concatenate([(s+np.arange(7))%n for s in starts])[:n];boot.append(delta[idx].sum())
 save(dict(main_policy=main,comparator=base,capacity=.02,incremental_benefit=float(delta.sum()),
 ci95_low=float(np.quantile(boot,.025)),ci95_high=float(np.quantile(boot,.975)),days=n,block_days=7,
 note='Exploratory paired circular bootstrap; few independent temporal blocks; no causal claim'),'financial_bootstrap.json')
 return table,det

def unsupervised(d):
 # Agrupa transações históricas, sem rótulo e sem dados de teste.
 tr=d[d.split=='train'].sample(2000,random_state=SEED).copy()
 cols=['TransactionAmt','C1','C2','C5','C13','D1','D4','dist1','missing_count']
 X=SimpleImputer(strategy='median').fit_transform(tr[cols])
 # log1p em quantidades não negativas reduz domínio de caudas antes da distância.
 X=np.log1p(np.maximum(X,0));X=StandardScaler().fit_transform(X)
 rows=[];labels={}
 for method in ['KMeans','Hierarchical']:
  for k in [2,3,4,5,6]:
   lab=KMeans(n_clusters=k,n_init=15,random_state=SEED).fit_predict(X) if method=='KMeans' else AgglomerativeClustering(n_clusters=k).fit_predict(X)
   rows.append(dict(method=method,config=f'k={k}',silhouette=silhouette_score(X,lab),DB=davies_bouldin_score(X,lab),noise=0.))
   labels[(method,f'k={k}')]=lab
 for eps in [.7,1.,1.5,2.]:
  lab=DBSCAN(eps=eps,min_samples=10).fit_predict(X);mask=lab!=-1;n=len(set(lab[mask]))
  rows.append(dict(method='DBSCAN',config=f'eps={eps}',silhouette=silhouette_score(X[mask],lab[mask]) if 1<n<mask.sum() else np.nan,
    DB=davies_bouldin_score(X[mask],lab[mask]) if 1<n<mask.sum() else np.nan,noise=float((~mask).mean())))
 table=pd.DataFrame(rows);best=table[table.method=='KMeans'].sort_values('silhouette',ascending=False).iloc[0]
 tr['cluster']=labels[('KMeans',best.config)];pca=PCA().fit(X);coords=pca.transform(X);tr['PC1']=coords[:,0];tr['PC2']=coords[:,1]
 tr[['source_row','cluster','PC1','PC2','isFraud']+cols].to_csv(ROOT/'results/cluster_assignments.csv',index=False)
 tr.groupby('cluster').agg(n=('isFraud','size'),fraud_rate=('isFraud','mean'),amount=('TransactionAmt','mean')).to_csv(ROOT/'results/cluster_profiles.csv')
 table.to_csv(ROOT/'results/clustering_metrics.csv',index=False)
 pd.DataFrame(dict(component=np.arange(1,len(cols)+1),variance=pca.explained_variance_ratio_,cumulative=np.cumsum(pca.explained_variance_ratio_))).to_csv(ROOT/'results/pca_variance.csv',index=False)
 pd.DataFrame(pca.components_,columns=cols).to_csv(ROOT/'results/pca_coefficients.csv',index=False)
 stab=[]
 for seed in [7,21,84]:
  lab=KMeans(n_clusters=int(best.config.split('=')[1]),n_init=15,random_state=seed).fit_predict(X)
  stab.append(dict(seed=seed,ARI=adjusted_rand_score(tr.cluster,lab)))
 pd.DataFrame(stab).to_csv(ROOT/'results/cluster_stability.csv',index=False)
 return tr,table

def validate(d,cp,rp,det):
 checks=[]
 def check(name,c):
  assert c,name;checks.append(dict(check=name,passed=True))
 check('Unique source rows',not d.source_row.duplicated().any())
 check('Targets excluded',not {'isFraud','exposure','source_row','day','TransactionDT'}.intersection(NUM+CAT))
 for a,b in zip(['train','validation','calibration'],['validation','calibration','test']):check('Temporal '+a+'/'+b,d[d.split==a].day.max()<d[d.split==b].day.min())
 check('Class target valid',d.isFraud.isin([0,1]).all());check('Monetary proxy identity',np.allclose(d.exposure,d.isFraud*d.TransactionAmt))
 check('Finite predictions',np.isfinite(cp.prediction).all() and np.isfinite(rp.prediction).all())
 z=d[d.split=='test']
 for cap,q in det.groupby('capacity'):
  sizes=q.groupby(['day','policy']).review.sum().unstack()
  check(f'Equal review budgets {cap}',sizes.nunique(axis=1).eq(1).all())
  for day,g in z.groupby('day'):check(f'Capacity {cap} day{day}',int(sizes.loc[day].iloc[0])==int(np.ceil(cap*len(g))))
 # Rótulos embaralhados não podem alterar as decisões de uma política já pontuada.
 p=cp[(cp.split=='test')&(cp.model==json.loads((ROOT/'results/classification_selection.json').read_text())['winner'])].set_index('row').loc[z.index,'prediction'].to_numpy()
 shuffled=z.copy();shuffled['isFraud']=np.random.default_rng(SEED).permutation(shuffled.isFraud)
 check('Label-independent decisions',np.array_equal(review_mask(z,p*z.TransactionAmt),review_mask(shuffled,p*shuffled.TransactionAmt)))
 pd.DataFrame(checks).to_csv(ROOT/'results/verification.csv',index=False)
 return len(checks)

def figures(d,cm,rm,cp,rp,cwin,rwin,fin,det,clusters,models):
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':140})
 def savefig(name):plt.tight_layout();plt.savefig(ROOT/f'results/figures/{name}.png',bbox_inches='tight');plt.close()
 fig,ax=plt.subplots(figsize=(10,4))
 for split,g in d.groupby('split',sort=False):ax.plot(g.groupby('day').isFraud.mean(),label=split)
 ax.set(xlabel='Dia relativo (não data civil)',ylabel='Fração de fraudes',title='Mudança temporal da prevalência');ax.legend();savefig('timeline')
 z=cm[cm.split=='test'].sort_values('AP');fig,ax=plt.subplots(figsize=(9,4));ax.barh(z.model,z.AP,color='#12395B');ax.axvline(d[d.split=='test'].isFraud.mean(),color='grey',ls='--');ax.set(xlabel='Average precision',title='Classificação no teste');savefig('classification_models')
 test=d[d.split=='test'];pred=cp[(cp.model==cwin)&(cp.split=='test')].set_index('row').loc[test.index]
 prob=pred.raw.to_numpy();calprob=pred.prediction.to_numpy();threshold=json.loads((ROOT/'results/classification_selection.json').read_text())['thresholds'][cwin]
 confusion=confusion_matrix(test.isFraud,prob>=threshold);pd.DataFrame(confusion,index=['real0','real1'],columns=['pred0','pred1']).to_csv(ROOT/'results/confusion_matrix.csv')
 fig,axs=plt.subplots(1,3,figsize=(13,3.7));axs[0].imshow(confusion,cmap='Blues')
 for (i,j),v in np.ndenumerate(confusion):axs[0].text(j,i,str(v),ha='center',va='center')
 axs[0].set(xlabel='Previsto',ylabel='Real',xticks=[0,1],yticks=[0,1],title='Matriz / limiar F1')
 fpr,tpr,_=roc_curve(test.isFraud,prob);axs[1].plot(fpr,tpr);axs[1].set(xlabel='Falsos positivos',ylabel='Recall',title='ROC')
 precision,recall,_=precision_recall_curve(test.isFraud,prob);axs[2].plot(recall,precision);axs[2].axhline(test.isFraud.mean(),ls='--',color='grey');axs[2].set(xlabel='Recall',ylabel='Precisão',title='Precisão–recall');savefig('classification_diagnostics')
 fig,ax=plt.subplots(figsize=(7,4))
 for name,p in [('Bruta',prob),('Platt',calprob)]:
  f,m=calibration_curve(test.isFraud,p,n_bins=8,strategy='quantile');ax.plot(m,f,'o-',label=name)
 ax.plot([0,1],[0,1],'--',color='grey');ax.set(xlabel='Probabilidade prevista',ylabel='Frequência',title='Calibração no teste');ax.legend();savefig('calibration')
 q=fin[(fin.scenario=='central')&(fin.capacity==.02)].sort_values('net_benefit');fig,ax=plt.subplots(figsize=(10,4));ax.barh(q.policy,q.net_benefit,color='#12395B');ax.set(xlabel='Benefício líquido simulado (US$)',title='Mesma capacidade: 2% das transações por dia');savefig('financial_comparison')
 q=fin[(fin.scenario=='central')];fig,ax=plt.subplots(figsize=(9,4))
 for name,g in q.groupby('policy'):ax.plot(g.capacity*100,g.amount_recall*100,'o-',label=name)
 ax.set(xlabel='Capacidade diária (%)',ylabel='Valor fraudulento identificado (%)',title='Capacidade e cobertura monetária');ax.legend(fontsize=8);savefig('capacity')
 q=det[det.capacity==.02].copy();q['net']=q.review*(.8*q.exposure-2)
 fig,ax=plt.subplots(figsize=(10,4));q.groupby(['day','policy']).net.sum().unstack().cumsum().plot(ax=ax);ax.set(ylabel='Benefício acumulado simulado (US$)',title='Evolução temporal do benefício');savefig('financial_timeline')
 z=rm[rm.split=='test'].sort_values('RMSE');fig,ax=plt.subplots(figsize=(9,4));ax.barh(z.model,z.RMSE,color='#12395B');ax.set(xlabel='RMSE da exposição rotulada (US$)',title='Regressão de alvo com muitos zeros');savefig('regression_models')
 fig,axs=plt.subplots(1,2,figsize=(11,4));axs[0].scatter(clusters.PC1,clusters.PC2,c=clusters.cluster,cmap='tab10',s=5,alpha=.5);axs[0].set(xlabel='PC1',ylabel='PC2',title='Transações de treino')
 v=pd.read_csv(ROOT/'results/pca_variance.csv');axs[1].plot(v.component,v.cumulative,'o-');axs[1].set(xlabel='Componentes',ylabel='Variância acumulada');savefig('clusters_pca')
 # Permutação no período de calibração: não usa teste para selecionar atributos.
 sample=d[d.split=='calibration'].sample(1200,random_state=SEED)
 imp=permutation_importance(models[cwin],sample[NUM+CAT],sample.isFraud,scoring='average_precision',n_repeats=3,random_state=SEED,n_jobs=1)
 table=pd.DataFrame(dict(feature=NUM+CAT,importance=imp.importances_mean,std=imp.importances_std)).sort_values('importance',ascending=False)
 table.to_csv(ROOT/'results/permutation_importance.csv',index=False)
 z=table.head(12).iloc[::-1];fig,ax=plt.subplots(figsize=(9,4));ax.barh(z.feature,z.importance,color='#12395B');ax.set(xlabel='Queda em average precision ao embaralhar',title='Importância preditiva na calibração');savefig('importance')

def run():
 for sub in ['data/processed','results/figures','work']:(ROOT/sub).mkdir(parents=True,exist_ok=True)
 start=time.time();d,a=build_dataset();print('DATA',len(d),a['splits'],flush=True)
 cm,cp,cmodels,cwin,cal=train(d,'classification');rm,rp,rmodels,rwin,_=train(d,'regression')
 fin,det=policies(d,cp,rp,cwin,rwin);cl,clmetrics=unsupervised(d)
 from additional_analysis import evaluate_classifiers
 evaluate_classifiers(d,cp)
 checks=validate(d,cp,rp,det)
 # Referências de regressão e classificação, adicionais à contagem de técnicas.
 tr=d[d.split=='train'];test=d[d.split=='test'];br=[]
 for name,p in [('Zero',np.zeros(len(test))),('TrainingMean',np.full(len(test),tr.exposure.mean())),('GlobalRateAmount',test.TransactionAmt.to_numpy()*tr.isFraud.mean())]:br.append(dict(model=name,**reg_metrics(test.exposure,p)))
 pd.DataFrame(br).to_csv(ROOT/'results/regression_baselines.csv',index=False)
 bclass=[]
 for name,p in [('NeverFraud',np.zeros(len(test))),('AlwaysFraud',np.ones(len(test))),('TrainingRate',np.full(len(test),tr.isFraud.mean()))]:bclass.append(dict(model=name,**cls_metrics(test.isFraud,p,.5)))
 pd.DataFrame(bclass).to_csv(ROOT/'results/classification_baselines.csv',index=False)
 figures(d,cm,rm,cp,rp,cwin,rwin,fin,det,cl,cmodels)
 # Diagnósticos explicativos reproduzem campeões; não mudam escolhas nem filas.
 from diagnosticos_apresentacao import run as diagnose_frozen_models
 diagnose_frozen_models()
 save(dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,duration_seconds=time.time()-start,
 classification_winner=cwin,regression_winner=rwin,checks=checks,techniques=15),'execution.json')
 print('DONE',cwin,rwin,checks,flush=True)
 return d
if __name__=='__main__':run()
