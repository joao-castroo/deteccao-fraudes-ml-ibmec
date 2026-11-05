# Escolha dos modelos e histórico de experimentação

Escolhemos técnicas com hipóteses diferentes para verificar se a complexidade acrescenta valor. Ridge, Lasso e HistGradientBoosting foram mantidos conforme o conteúdo estudado. As tarefas de classificação, regressão e exploração recebem métodos com pressupostos diferentes. HistGradientBoosting aparece nas duas tarefas supervisionadas; PCA é redução de dimensionalidade. A comparação distingue as tarefas e não usa quantidade como argumento de adequação.

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

## Motivação e rastreabilidade

**Critério de escolha:** confrontamos hipóteses distintas para verificar se a complexidade traz ganho sobre referências simples. A fraude é rara (3,33% no teste), as 71 entradas incluem várias variáveis anônimas e correlacionadas, as transações têm ordem temporal e o alvo monetário tem muitos zeros.

| Família | Hipótese confrontada com os dados | Adequação e limite |
|---|---|---|
| Logística e LDA | Uma fronteira linear pode separar o risco? | Referências para verificar se interações são necessárias; LDA usa covariância compartilhada com shrinkage |
| Árvore, Random Forest e HistGradientBoosting | Não linearidades e interações acrescentam valor? | Testam maior flexibilidade, com controle de complexidade e risco de sobreajuste |
| Linear, Ridge e Lasso | Uma relação linear basta para a exposição monetária? | Referências e penalização sob correlação; muitos zeros e cauda pesada exigem diferentes métricas |
| KNN | Proximidade entre transações ajuda a prever fraude? | Escala e muitas dimensões podem reduzir a qualidade das distâncias |
| GaussianNB | Uma aproximação bayesiana simples é competitiva? | Independência condicional é uma hipótese exigente; não fizemos teste formal para comprová-la ou rejeitá-la |
| K-means, Hierárquico, DBSCAN e PCA | Há perfis, regiões densas e projeções úteis? | Exploração sem rótulo; estrutura e variância não demonstram retorno financeiro |

**Como decidimos:** as pequenas grades usam folds temporais. O critério de validação escolhe o algoritmo; o teste descreve o desempenho posterior. AP e captura monetária respondem a objetivos distintos. A quantidade de métodos não é evidência de adequação.

**Tentativas anteriores:** Extra Trees e ElasticNet foram efetivamente treinados e têm resultados preservados no histórico do repositório. A retirada ocorreu pela revisão do escopo curricular. Não afirmamos que perderam por desempenho, nem que todos os algoritmos estudados foram testados. Árvore e Random Forest continuaram na regressão. LDA foi incluído como outra hipótese linear de classificação.

A indicação docente de algo em torno de 15 técnicas foi uma referência aproximada de diversidade, sem impor uma meta. A justificativa do trabalho é a adequação dos métodos aos dados e à decisão. Os resultados da versão inicial podem ser conferidos em [classification_metrics.csv](https://github.com/joao-castroo/deteccao-fraudes-ml-ibmec/blob/1ca4a6b/results/classification_metrics.csv), [regression_metrics.csv](https://github.com/joao-castroo/deteccao-fraudes-ml-ibmec/blob/1ca4a6b/results/regression_metrics.csv) e nos respectivos arquivos de seleção do mesmo commit. Nenhum novo treinamento foi necessário para esta correção de narrativa.
