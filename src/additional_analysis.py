"""Diagnóstico adicional sem mudar campeão ou política principal pelo teste."""
from experiment import *

def evaluate_classifiers(d,cp):
 z=d[d.split=='test'];rows=[];daily={}
 for model in cp.model.unique():
  p=cp[(cp.model==model)&(cp.split=='test')].set_index('row').loc[z.index,'prediction'].to_numpy()
  mask=review_mask(z,p*z.TransactionAmt)
  rows.append(dict(model=model,**financial(z,mask)))
  a=z[['day','exposure']].copy();a['net']=mask*(.8*a.exposure-2.)
  daily[model]=a.groupby('day').net.sum()
 pd.DataFrame(rows).to_csv(ROOT/'results/financial_all_classifiers.csv',index=False)
 winner=json.loads((ROOT/'results/classification_selection.json').read_text())['winner']
 delta=(daily[winner]-daily['Logistic']).to_numpy();n=len(delta)
 rng=np.random.default_rng(SEED);boot=[]
 for _ in range(5000):
  starts=rng.integers(0,n,size=int(np.ceil(n/7)));idx=np.concatenate([(s+np.arange(7))%n for s in starts])[:n]
  boot.append(delta[idx].sum())
 save(dict(candidate=winner,reference='Logistic',incremental_benefit=float(delta.sum()),
 ci95_low=float(np.quantile(boot,.025)),ci95_high=float(np.quantile(boot,.975)),
 note='Additional diagnostic after primary evaluation; does not replace original comparator or winner'),'logistic_comparator_bootstrap.json')
if __name__=='__main__':
 d=pd.read_parquet(ROOT/'data/processed/transactions.parquet');cp=pd.read_csv(ROOT/'results/classification_predictions.csv');evaluate_classifiers(d,cp)
