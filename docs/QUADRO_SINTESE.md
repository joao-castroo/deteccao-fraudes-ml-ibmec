# Comparação das técnicas e adequação aos dados

Modelos supervisionados: métricas do teste, com escolhas pela validação. Agrupamentos e PCA: métricas na amostra de treino, não no teste. Os índices de tarefas diferentes não são comparáveis entre si.

| Frente | Técnica | Configuração escolhida | Métrica | Ponto forte | Limitação |
|---|---|---|---|---|---|
| Regressão | Linear | Sem penalização | RMSE=45.35; R²=0.030 | Referência simples | Relação linear e cauda rara |
| Regressão | Ridge | alpha=100.0 | RMSE=45.32; R²=0.031 | Estabiliza coeficientes | Não aprende interações sozinho |
| Regressão | Lasso | alpha=0.1 | RMSE=45.30; R²=0.032 | Pode zerar coeficientes | Instável sob correlação |
| Regressão | Árvore | prof.=5; mín.folha=50 | RMSE=42.32; R²=0.155 | Regras e interações | Sensível à amostra |
| Regressão | Random Forest * | 60 árvores; prof.=15; mín.folha=5 | RMSE=39.96; R²=0.247 | Reduz variância das árvores | Menor transparência |
| Regressão | HistGB | folhas=15; L2=50.0 | RMSE=39.67; R²=0.257 | Corrige erros sequencialmente | Complexidade e sobreajuste |
| Classificação | Logística | C=1.0 | AP=0.340; F1=0.363 | Referência probabilística | Linearidade no logit |
| Classificação | LDA | shrinkage=auto | AP=0.324; F1=0.367 | Considera covariância comum | Hipóteses gaussianas restritivas |
| Classificação | HistGB * | folhas=31; L2=20.0 | AP=0.454; F1=0.459 | Corrige erros sequencialmente | Complexidade e sobreajuste |
| Classificação | KNN | k=45 | AP=0.304; F1=0.358 | Proximidade entre exemplos | Distância em alta dimensão |
| Classificação | GaussianNB | var.smooth=0.001 | AP=0.086; F1=0.144 | Ajuste rápido | Independência e gaussianidade |
| Exploração | KMeans | k=2; n_init=15 | Sil=0.552; DB=0.833 | Perfis compactos | Escala e formato dos grupos |
| Exploração | Hierárquico | Ward; k=2 | Sil=0.580; DB=0.756 | Estrutura de uniões | Corte e custo computacional |
| Exploração | DBSCAN | eps=1.5; mín=10 | Sil=0.369; ruído=9% | Densidade e ruído | Depende de eps e cobertura |
| Exploração | PCA | 9 entradas; projeção 2D | 2 CP=56.53%; 5=89.02% | Resume variância | Não otimiza fraude ou lucro |

* Vencedor da tarefa na validação. PCA é redução de dimensionalidade. HistGB é aplicado à regressão e à classificação. Baselines e configurações integram a comparação e não são argumentos de adequação.
