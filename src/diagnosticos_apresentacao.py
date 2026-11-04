"""Diagnóstico posterior dos campeões congelados, sem nova seleção.

Reproduz o ajuste final para comparar ajuste e teste. Os rótulos do teste não
escolhem configurações. As previsões precisam coincidir com as já publicadas.
Executar na raiz: python src/diagnosticos_apresentacao.py
"""
from pathlib import Path
import json
from experiment import (budget_sample, specs, Pipeline, preprocess, clone,
                        NUM, CAT, cls_metrics, reg_metrics, np, pd, plt)
from sklearn.inspection import permutation_importance
ROOT = Path(__file__).resolve().parents[1]

def run():
    dados = pd.read_parquet(ROOT / 'data/processed/transactions.parquet')
    ajuste = budget_sample(dados[dados.split.isin(['train', 'validation'])])
    teste = dados[dados.split == 'test']
    linhas = []
    for tarefa in ['classification', 'regression']:
        selecao = json.loads((ROOT / f'results/{tarefa}_selection.json').read_text())
        nome = selecao['winner']
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
    # O modelo da última tarefa é o regressor congelado. Usa apenas calibração
    # para explicar entradas, sem seleção de atributos ou ajuste pelo teste.
    calibracao = dados[dados.split == 'calibration'].sample(1200, random_state=42)
    importancia = permutation_importance(
        modelo, calibracao[NUM + CAT], calibracao.exposure,
        scoring='neg_root_mean_squared_error', n_repeats=3,
        random_state=42, n_jobs=1)
    tabela = pd.DataFrame({'feature': NUM + CAT,
        'increase_RMSE_USD': importancia.importances_mean,
        'std': importancia.importances_std}).sort_values('increase_RMSE_USD', ascending=False)
    assert np.isfinite(tabela[['increase_RMSE_USD', 'std']]).all().all()
    tabela.to_csv(ROOT / 'results/regression_permutation_importance.csv', index=False)
    topo = tabela.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 4), dpi=140)
    ax.barh(topo.feature, topo.increase_RMSE_USD, color='#176B72')
    ax.set(xlabel='Aumento de RMSE ao embaralhar (US$)',
           title='Random Forest: importância na calibração')
    fig.tight_layout(); fig.savefig(ROOT / 'results/figures/regression_importance.png', bbox_inches='tight'); plt.close(fig)
    previsao_teste = np.maximum(0, modelo.predict(teste[NUM + CAT]))
    fig, axs = plt.subplots(1, 2, figsize=(11, 4), dpi=140)
    axs[0].scatter(teste.exposure, previsao_teste, s=6, alpha=.25, color='#176B72')
    limite = max(teste.exposure.max(), previsao_teste.max())
    axs[0].plot([0, limite], [0, limite], '--', color='#B57832')
    axs[0].set(xlabel='Exposição observada (US$)', ylabel='Prevista (US$)', title='Observado e previsto no teste')
    axs[1].scatter(previsao_teste, teste.exposure-previsao_teste, s=6, alpha=.25, color='#176B72')
    axs[1].axhline(0, ls='--', color='#B57832')
    axs[1].set(xlabel='Prevista (US$)', ylabel='Observado menos previsto (US$)', title='Resíduos no teste')
    fig.tight_layout(); fig.savefig(ROOT / 'results/figures/regression_residuals.png', bbox_inches='tight'); plt.close(fig)
    saida = {'note': 'Post hoc descriptive diagnostic. Frozen parameters and original final training sample. Test predictions match saved predictions. No reselection.', 'rows': linhas}
    (ROOT / 'results/training_diagnostics.json').write_text(json.dumps(saida, indent=2, ensure_ascii=False))
    print(pd.DataFrame(linhas).to_string(index=False))

if __name__ == '__main__':
    run()
