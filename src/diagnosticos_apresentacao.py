"""Diagnóstico posterior dos campeões congelados, sem nova seleção.

Reproduz o ajuste final para comparar ajuste e teste. Os rótulos do teste não
escolhem configurações. As previsões precisam coincidir com as já publicadas.
Executar na raiz: python src/diagnosticos_apresentacao.py
"""
from pathlib import Path
import json
from experiment import (budget_sample, specs, Pipeline, preprocess, clone,
                        NUM, CAT, cls_metrics, reg_metrics, np, pd, plt)
ROOT = Path(__file__).resolve().parents[1]

def run():
    dados = pd.read_parquet(ROOT / 'data/processed/transactions.parquet')
    ajuste = budget_sample(dados[dados.split.isin(['train', 'validation'])])
    teste = dados[dados.split == 'test']
    linhas = []
    for tarefa, nome in [('classification', 'ExtraTrees'), ('regression', 'RandomForest')]:
        selecao = json.loads((ROOT / f'results/{tarefa}_selection.json').read_text())
        assert selecao['winner'] == nome, 'O campeão mudou. Reveja o diagnóstico.'
        estimador = clone(specs(tarefa)[nome][0]).set_params(**selecao['params'][nome])
        modelo = Pipeline([('pre', preprocess()), ('model', estimador)])
        alvo = 'isFraud' if tarefa == 'classification' else 'exposure'
        modelo.fit(ajuste[NUM + CAT], ajuste[alvo])
        salvas = pd.read_csv(ROOT / f'results/{tarefa}_predictions.csv')
        salvas = salvas[(salvas.model == nome) & (salvas.split == 'test')].set_index('row').loc[teste.index]
        for bloco, z in [('Ajuste final (30 mil)', ajuste), ('Teste posterior', teste)]:
            if tarefa == 'classification':
                previsao = modelo.predict_proba(z[NUM + CAT])[:, 1]
                metricas = cls_metrics(z.isFraud, previsao, selecao['thresholds'][nome])
            else:
                previsao = np.maximum(0, modelo.predict(z[NUM + CAT]))
                metricas = reg_metrics(z.exposure, previsao)
            if bloco == 'Teste posterior':
                assert np.allclose(previsao, salvas.raw, rtol=1e-8, atol=1e-8)
            linhas.append(dict(task=tarefa, model=nome, split=bloco, **metricas))
    saida = {'note': 'Post hoc descriptive diagnostic. Frozen parameters and original final training sample. Test predictions match saved predictions. No reselection.', 'rows': linhas}
    (ROOT / 'results/training_diagnostics.json').write_text(json.dumps(saida, indent=2, ensure_ascii=False))
    print(pd.DataFrame(linhas).to_string(index=False))

if __name__ == '__main__':
    run()
