# Revisão curricular: 15 aplicações de técnicas

Ridge, Lasso e HistGradientBoosting foram mantidos conforme o conteúdo estudado. São seis regressões, cinco classificações, três agrupamentos e PCA. HistGradientBoosting aparece nas duas tarefas supervisionadas; PCA é redução de dimensionalidade. A contagem é por aplicação e tarefa, e não por família distinta.

Regressão: Linear, Ridge, Lasso, Árvore, Random Forest e HistGradientBoosting.

Classificação: Logística, LDA, HistGradientBoosting, KNN e GaussianNB.

Agrupamento: K-means, Hierárquico e DBSCAN. Redução: PCA.

A revisão retirou Extra Trees e ElasticNet e concentrou Árvore e Random Forest na regressão. Acrescentou LDA, presente no quadro enviado. A lista segue o escopo discutido; não pretende treinar todos os algoritmos citados no quadro. As versões anteriores permanecem no histórico do Git.

## Seleção sem usar o desempenho do teste como critério

A grade de cada algoritmo usa três folds temporais dentro do treino, por AP na classificação e MSE na regressão. A validação externa escolhe o classificador pelo valor rotulado capturado com score bruto × montante e capacidade diária de 2%. Depois, Platt usa um bloco próprio e a fila final usa probabilidade calibrada × montante. Esta sequência não garante o ótimo monetário global.

### Captura na validação por classificador

| Modelo | Valor rotulado capturado (US$) |
|---|---:|
| HistGradientBoosting | 60822.713 |
| Logistic | 56719.291 |
| KNN | 49513.148 |
| LDA | 37045.073 |
| GaussianNB | 27402.476 |

O HistGradientBoosting vence esta comparação. Random Forest vence a regressão pelo MSE de validação. As configurações, previsões e diagnósticos estão em results. O notebook explica a diferença entre seleção de hiperparâmetros, seleção de algoritmo, calibração e avaliação.

## Como interpretar a mudança financeira

A política atual captura US$ 38.044,57 de fraude rotulada em 333 revisões. Sob eficácia de 80% e custo de US$ 2 por revisão, o incremento sobre maiores valores é US$ 18.699,66, equivalente a 27,59% da perda simulada da referência. O incremento sobre logística é US$ 7.132,38, diagnóstico adicional.

O HistGradientBoosting já era um candidato na versão anterior. Reduzir a lista não melhorou automaticamente o algoritmo; mudou o vencedor elegível pelo critério de validação. O período de teste já havia sido consultado: esta revisão constitui avaliação retrospectiva, não confirmação em uma nova amostra inédita. As premissas econômicas são cenários acadêmicos, não lucro observado.

## Evidência de execução

- Notebook: 81 células, 25 de código executadas, sem saída de erro.
- Dados e políticas: 125 verificações aprovadas.
- Diagnóstico dos dois vencedores: novo ajuste com a mesma amostra e parâmetros reproduz as previsões salvas.
- Entrega: mesmo PPT de dez slides para apresentação e entrega, relatório de nove páginas, roteiro de estudo separado em Word e HTML.

O ambiente emitiu avisos numéricos preservados nos logs. As previsões aceitas são finitas; os avisos não foram tratados como resultados válidos por si mesmos.
