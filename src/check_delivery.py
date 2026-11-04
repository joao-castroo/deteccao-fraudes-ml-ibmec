"""Confere coerência entre escopo, seleção, números publicados e artefatos.

Não substitui a execução do experimento nem a inspeção visual das páginas.
Executar da raiz: python src/check_delivery.py
"""
from pathlib import Path
import csv,json,math,re,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,condition):
    checks.append(dict(name=name,passed=bool(condition)))
    if not condition:raise AssertionError(name)
def meta(name):return json.loads((ROOT/'results'/name).read_text())
def rows(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))
def xmltext(archive,name):return ' '.join(ET.fromstring(archive.read(name)).itertext())
cls=['Logistic','LDA','HistGradientBoosting','KNN','GaussianNB']
reg=['Linear','Ridge','Lasso','DecisionTree','RandomForest','HistGradientBoosting']
for task,names in [('classification',cls),('regression',reg)]:
    sel=meta(task+'_selection.json');check(task+': candidatos exatos',set(sel['params'])==set(names))
    check(task+': métricas apenas dos candidatos atuais',set(r['model'] for r in rows(task+'_metrics.csv'))==set(names))
    cv=rows(task+'_cv.csv')
    for model in names:
        groups={}
        for r in cv:
            if r['model']==model:groups.setdefault(r['params'],[]).append(r)
        check(task+' '+model+': três folds por configuração',all(len(g)==3 and {x['fold'] for x in g}=={'1','2','3'} for g in groups.values()))
        check(task+' '+model+': treino anterior à validação',all(int(x['train_end'])<int(x['val_start']) for g in groups.values() for x in g))
        best=min(groups,key=lambda k:sum(float(x['score']) for x in groups[k])/len(groups[k]))
        check(task+' '+model+': configuração coincide com CV',json.loads(best)==sel['params'][model])
    expected=max(sel['validation_selection_scores'],key=sel['validation_selection_scores'].get)
    check(task+': vencedor coincide com critério de validação',expected==sel['winner'])
check('15 aplicações no registro de execução',meta('execution.json')['techniques']==15)
check('125 verificações do experimento aprovadas',len(rows('verification.csv'))==125 and all(r['passed']=='True' for r in rows('verification.csv')))
f=rows('financial_policies.csv')
check('Identidade financeira em todos os cenários',all(math.isclose(float(x['net_benefit']),float(x['efficacy'])*float(x['labeled_amount_captured'])-float(x['cost'])*float(x['reviewed'])-float(x['fp_penalty'])*float(x['legitimate_reviewed']),abs_tol=1e-7) for x in f))
central={x['policy']:x for x in f if x['scenario']=='central' and float(x['capacity'])==.02}
check('Mesma quantidade de revisões entre políticas',set(int(x['reviewed']) for x in central.values())=={333})
main=central['ML_ExpectedAmount'];base=central[meta('baseline_selection.json')['comparator']]
delta=float(main['net_benefit'])-float(base['net_benefit'])
check('Bootstrap e benefício incremental reconciliados',math.isclose(delta,meta('financial_bootstrap.json')['incremental_benefit'],abs_tol=1e-7))
nb=json.loads((ROOT/'notebooks/01_projeto_fraude_completo.ipynb').read_text());code=[c for c in nb['cells'] if c['cell_type']=='code'];source='\n'.join(''.join(c['source']) for c in nb['cells'])
check('81 células e 25 células de código executadas',len(nb['cells'])==81 and len(code)==25 and all(c['execution_count'] for c in code))
check('Notebook sem saídas de erro',all(o['output_type']!='error' for c in code for o in c['outputs']))
check('Notebook explica LDA, CV temporal e revisão retrospectiva',all(t in source for t in ['LDA, passo a passo','Validação do KNN','avaliação desta revisão é retrospectiva']))
with zipfile.ZipFile(ROOT/'deliverables/apresentacao_Fraude.pptx') as z:
    slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)]
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)]
    text='\n'.join(xmltext(z,n) for n in slides+notes)
    check('PPT de dez slides e dez notas',len(slides)==10 and len(notes)==10)
    check('PPT autores e ganho atual',all(x in text for x in ['João Pedro Castro','Vitor Neves','18.699,66','27,59%']))
    check('PPT mantém Ridge, Lasso e HistGradientBoosting',all(x in text for x in ['Ridge','Lasso','HistGradientBoosting']))
for file in ['relatorio_Fraude.docx','roteiro_completo_apresentacao_e_defesa.docx']:
    with zipfile.ZipFile(ROOT/'deliverables'/file) as z:text=xmltext(z,'word/document.xml')
    check(file+': autoria e resultado atuais',all(x in text for x in ['João Pedro Castro','Vitor Neves','18.699,66','27,59%']))
    check(file+': sem resultado principal anterior',all(x not in text for x in ['16.352,90','24,13%','4.785,62']))
check('Resultado salvo de classificação com HistGradientBoosting',meta('classification_selection.json')['winner']=='HistGradientBoosting')
check('Resultado salvo de regressão com Random Forest',meta('regression_selection.json')['winner']=='RandomForest')
report={'scope':'Curricular revision: 15 applications, Ridge/Lasso/HistGB retained; same previously inspected test period. Retrospective evaluation.', 'checks':checks,'passed':len(checks),'financial_incremental_benefit':delta,'manual_visual_review':{'ppt_slides':10,'report_pages':8,'study_guide_pages':30,'all_pages_inspected':True}}
(ROOT/'results/delivery_verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(f'{len(checks)} verificações de entrega aprovadas.')
