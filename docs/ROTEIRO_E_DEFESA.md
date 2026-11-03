# Roteiro completo de apresentação e defesa

**Autores: João Pedro Castro e Vitor Neves.**

A apresentação e a entrega usam o mesmo arquivo: [apresentacao_Fraude.pptx](../deliverables/apresentacao_Fraude.pptx), com **10 slides**. O tempo planejado soma **15 minutos, incluindo demonstração**. Este roteiro concentra os detalhes que não cabem nos slides.

Não leia todo o roteiro durante a fala. Use a sequência cronometrada para ensaiar e as seções técnicas para estudar. Ambos os integrantes devem conseguir explicar os números centrais.

## Navegação

1. [Fala por slide](#fala-por-slide)
2. [Termos: significado, finalidade e uso](#termos-significado-finalidade-e-uso)
3. [As 19 técnicas e os resultados](#as-19-técnicas-e-os-resultados)
4. [A conta financeira e as comparações](#a-conta-financeira-e-as-comparações)
5. [Explicações passo a passo](#explicações-passo-a-passo)
6. [Perguntas do professor](#perguntas-do-professor)
7. [Ensaio e demonstração em dupla](#ensaio-e-demonstração-em-dupla)

## Fala por slide


### Slide 01 — Fraude e priorização econômica

**Tempo: 00:00–00:35 (35 segundos).**

**Fala sugerida:** Nossa pergunta é como gerar mais valor com a mesma capacidade de investigação. Estudamos transações reais IEEE-CIS/Vesta e conectamos modelos de risco à escolha de uma fila diária. Comparamos dezenove técnicas. A apresentação e a entrega usam estes mesmos dez slides. O roteiro e o notebook concentram os detalhes de defesa.

**Pergunta e resposta:** O estudo mede dinheiro recuperado? Mede valor de fraude identificado e simula benefício com hipóteses explícitas.

**Evidência para conferir:** `README.md; results/config.json`


### Slide 02 — A decisão é priorizar uma fila limitada de análises

**Tempo: 00:35–02:00 (85 segundos).**

**Fala sugerida:** Uma equipe limitada precisa escolher o que investigar. Comparamos risco e exposição monetária. No exemplo A, oitenta por cento de risco vezes dez dólares gera oito dólares esperados. Em B, vinte por cento vezes mil gera duzentos. A política principal usa probabilidade calibrada vezes valor e capacidade de dois por cento por dia. A validação escolhe maiores valores como referência entre três regras simples. A pergunta mensurável é identificar mais valor de fraude com a mesma quantidade de análises. Não estamos avaliando bloqueio automático nem intervenção causal.

**Pergunta e resposta:** Por que machine learning? Para explorar combinações de atributos de risco que uma regra baseada somente no montante não utiliza.

**Evidência para conferir:** `results/baseline_selection.json; src/experiment.py: review_mask e financial`


### Slide 03 — Dados, preparação e avaliação respeitam a cronologia

**Tempo: 02:00–03:50 (110 segundos).**

**Fala sugerida:** A fonte original é IEEE-CIS/Vesta, no Kaggle, acessada por espelho OpenML documentado pelo Empulse. O arquivo tem 590.540 transações, 20.663 fraudes e 456 campos. Uma linha é transação, não cliente. Escolhemos uma em cada cinco linhas e removemos dias extremos parciais. A amostra final tem 116.533 transações e 71 entradas predefinidas. Ausências numéricas recebem mediana e indicadores, categorias recebem one-hot, e escalas são ajustadas no pipeline. Não eliminamos automaticamente montantes altos nem vetores semelhantes sem uma chave confiável. Os blocos preservam o tempo. O teste contém 15.915 transações, 530 fraudes e prevalência de 3,33%. Fonte e regras de uso estão nas referências. O espelho não demonstra licença irrestrita de redistribuição.

**Pergunta e resposta:** Como prevenimos vazamento? Transformações aprendem no treino de cada fold. Rótulo, exposição derivada e identificadores ficam fora das entradas. Features anônimas limitam a auditoria da construção original.

**Evidência para conferir:** `results/audit.json; results/provenance.json; results/missing_features.csv; data/processed/data_dictionary.csv; src/experiment.py`


### Slide 04 — Dezenove técnicas com critérios de seleção definidos

**Tempo: 03:50–05:20 (90 segundos).**

**Fala sugerida:** São sete classificadores, oito regressores e quatro métodos não supervisionados. Logística oferece referência de risco simples. Árvores e ensembles capturam relações não lineares. Regularização compara estabilidade nos regressores. KNN e GaussianNB usam hipóteses diferentes. Três folds temporais escolhem pequenas grades por AP na classificação e MSE na regressão. Depois a validação escolhe Extra Trees pelo valor capturado com score bruto vezes montante, e Random Forest regressor por MSE. O ajuste final recebe treino mais validação, até trinta mil linhas por ajuste, semente 42. Platt ajusta probabilidades num bloco separado. Mantemos o campeão mesmo se outro vencer alguma métrica no teste.

**Pergunta e resposta:** O que conta como técnica? Cada algoritmo ou método listado. Configurações, baselines e cenários não aumentam a contagem.

**Evidência para conferir:** `src/experiment.py: specs, train e unsupervised; results/classification_selection.json; results/regression_selection.json`


### Slide 05 — Regressão: exposição rotulada e erros no teste

**Tempo: 05:20–07:00 (100 segundos).**

**Fala sugerida:** O alvo é montante vezes rótulo: zero para legítimas e valor da transação para fraude. Trata-se de exposição rotulada, não prejuízo líquido realizado. A média condicional desse alvo se relaciona à probabilidade de fraude vezes o montante conhecido. Os muitos zeros explicam o bom MAE da previsão zero. MSE pune erros grandes e orientou nossa escolha. Random Forest venceu na validação e obteve RMSE 39,96 e R quadrado 0,247 no teste. HistGradientBoosting teve resultado de teste um pouco melhor, sem troca posterior. O RMSE do ajuste final foi 30,54. Há otimismo no ajuste e possível mudança temporal, que não podemos separar. Os gráficos mostram subestimação de casos extremos e erros na cauda.

**Pergunta e resposta:** O R² deveria ser muito alto? Não. O evento é raro e a informação é incompleta. R² mede erro quadrático relativo, não porcentagem de fraudes encontradas.

**Evidência para conferir:** `results/regression_metrics.csv; results/regression_baselines.csv; results/training_diagnostics.json; results/figures/apresentacao_residuos.png`


### Slide 06 — Classificação: comparação e diagnóstico no teste

**Tempo: 07:00–08:55 (115 segundos).**

**Fala sugerida:** Acurácia pode enganar: sempre prever legítima daria 96,67 por cento e recall zero. A tabela compara todos os sete classificadores. Extra Trees venceu a captura monetária na validação. Random Forest e HistGradientBoosting têm métricas de teste melhores em aspectos distintos, o que relatamos. O limiar de Extra Trees é 0,16, escolhido por F1 na validação. Ele gera 231 verdadeiros positivos, 390 falsos positivos, 299 falsos negativos e 14.995 verdadeiros negativos. A curva precisão-recall ajuda com classe rara. AP no ajuste é 0,895, no teste 0,379. Após Platt, Brier cai de 0,025902 para 0,025697. A matriz usa limiar fixo e não corresponde à fila de 333 análises.

**Pergunta e resposta:** Por que não usar limiar 0,5? O limiar depende do objetivo e da prevalência. Aqui o diagnóstico usa F1 de validação e a operação usa ranking diário.

**Evidência para conferir:** `results/classification_metrics.csv; results/confusion_matrix.csv; results/training_diagnostics.json; results/permutation_importance.csv`


### Slide 07 — Agrupamento e PCA exploram perfis sem usar o rótulo

**Tempo: 08:55–10:15 (80 segundos).**

**Fala sugerida:** Utilizamos duas mil transações de treino e nove indicadores numéricos com mediana, logaritmo e escala. K-means e hierárquico testam de dois a seis grupos. DBSCAN testa quatro eps e precisa mostrar quanto considera ruído. A projeção usa duas componentes e preserva 56,53 por cento da variância, enquanto cinco preservam 89,02. No K-means com dois grupos, os tamanhos são 1.880 e 120 e as taxas de fraude posteriores são 4,52 e 6,67 por cento. O hierárquico com dois grupos teve silhouette 0,580 e Davies–Bouldin 0,756. O PCA tem maiores pesos da primeira componente em C13, C1 e C2. Grupos não provam tipos de fraude, e variância explicada não é R quadrado nem acurácia.

**Pergunta e resposta:** Como escolhemos e interpretamos grupos? Índices internos, tamanho, ruído e estabilidade apoiam a escolha. O rótulo serve apenas à descrição posterior.

**Evidência para conferir:** `results/clustering_metrics.csv; results/cluster_profiles.csv; results/pca_variance.csv; results/pca_coefficients.csv; results/cluster_stability.csv`


### Slide 08 — A fila identifica mais valor com as mesmas 333 análises

**Tempo: 10:15–12:35 (140 segundos).**

**Fala sugerida:** No teste de 28 dias há 78.851,255 dólares de exposição rotulada. A capacidade nominal de dois por cento, arredondada em cada dia, gera 333 análises. A regra de maiores valores encontra 17 fraudes e 14.670 dólares. A probabilidade isolada encontra 168 fraudes e 18.896 dólares. Probabilidade vezes valor encontra 96 fraudes e 35.111 dólares: menos fraudes em quantidade, mais dinheiro identificado. Assumindo eficácia de oitenta por cento e custo de dois dólares por análise, o benefício líquido é 27.422,90, contra 11.070. A diferença é 16.352,90. Dividimos pela perda simulada remanescente da referência, 67.781,26, para obter 24,13 por cento. Contra logística simples, o ganho adicional é 4.785,62 e redução de 8,51 por cento. Isso mostra que uma referência simples já oferece valor. A regressão de exposição é uma política secundária e não substitui retrospectivamente a principal.

**Pergunta e resposta:** Por que custos maiores não mudam o ganho incremental em dólares? Com quantidade igual de análises e sem penalidade adicional, o custo unitário se cancela na diferença.

**Evidência para conferir:** `results/financial_policies.csv; results/financial_all_classifiers.csv; results/financial_bootstrap.json; results/logistic_comparator_bootstrap.json`


### Slide 09 — A evidência é positiva neste recorte e tem limites claros

**Tempo: 12:35–14:00 (85 segundos).**

**Fala sugerida:** O bootstrap pareado em blocos de sete dias produz intervalo exploratório de 11.865 a 21.327 dólares para o ganho principal. São cinco mil réplicas, mas apenas 28 dias de teste. Reduzir eficácia para cinquenta por cento mantém ganho simulado de 10.220,56. Não anualizamos. Features anônimas, possível repetição de cliente e rótulos históricos limitam a generalização. As revisões legítimas podem gerar atrito ou tratamento desigual. Uma implantação demandaria governança, finalidade e avaliação de privacidade, sem alegar conformidade jurídica a partir de dados públicos. A resposta à pergunta inicial é positiva neste teste sob hipóteses. Recomendamos outros períodos, custos completos e eficácia real antes de qualquer implantação.

**Pergunta e resposta:** O intervalo é garantia futura? Não. É exploratório, condicionado às hipóteses e ao curto período observado.

**Evidência para conferir:** `results/financial_bootstrap.json; results/financial_policies.csv; README.md; notebook seções 16–18`


### Slide 10 — Demonstração e materiais reproduzem o projeto

**Tempo: 14:00–15:00 (60 segundos).**

**Fala sugerida:** No notebook, mostrar a leitura, o pipeline, o split temporal e a célula de fit/predict da seção vinte. A busca inteira não roda durante a fala. Em seguida, a seção 24 reconcilia o ganho lendo o CSV. Usar os resultados já executados se o tempo de treinamento ultrapassar o ensaiado. O pacote contém PPT de dez slides, relatório de oito páginas, base processada, download da base original, código, notebook e roteiro detalhado. Os slides são os mesmos para entrega e apresentação. Conferir nomes completos dos dois integrantes, identificação dos arquivos e prazo no sistema antes da submissão.

**Pergunta e resposta:** Como outro integrante executa? Clona o repo privado após aceitar o convite, instala requirements numa venv e escolhe o kernel no notebook. A amostra processada já está incluída.

**Evidência para conferir:** `notebook seções 20 e 24; requirements.txt; src/download_data.py; references/template_professor.pptx`


## Termos: significado, finalidade e uso

| Termo | O que significa | Para que serve | Como usamos e o que encontramos |
|---|---|---|---|
| Unidade de análise | O objeto descrito por uma linha. | Define o que pode ser previsto e comparado. | Uma transação. Não supomos que cada linha seja uma pessoa diferente. |
| Feature / atributo | Informação de entrada usada na previsão. | Representar o evento antes da decisão. | 71 entradas predefinidas, 50 numéricas e 21 categóricas. isFraud e exposure não entram. |
| Alvo / target | Resultado que o modelo aprende a estimar. | Distinguir entradas da resposta. | isFraud para classificar. TransactionAmt × isFraud para regressão. |
| Amostra sistemática | Seleção por intervalo fixo na ordem das linhas. | Reduzir custo computacional com regra independente do rótulo. | source_row % 5 == 0. Não é amostra aleatória simples e pode sofrer viés de periodicidade. |
| Semente | Valor inicial do gerador pseudoaleatório. | Repetir sorteios e configurações. | 42 no protocolo principal. Não garante estabilidade em outras amostras. |
| Prevalência | Fração de exemplos positivos. | Contextualizar métricas em classe rara. | 3,47% na amostra e 3,33% no teste. Um sempre-legítima tem 96,67% de acurácia. |
| Desbalanceamento | Uma classe tem muito menos exemplos. | Escolher métricas e decisões adequadas. | Fraude é minoria. Não usamos oversampling, e o teste mantém a prevalência observada. |
| Imputação | Substituição de valores ausentes por regra. | Permitir ajuste sem apagar automaticamente registros. | Mediana numérica aprendida no treino de cada fold, mais indicadores de ausência. |
| One-hot encoding | Colunas indicadoras para categorias. | Evitar inventar ordem entre códigos. | Códigos de produto, cartão e outras categorias. Raros se agrupam e novos recebem tratamento do encoder. |
| Padronização | Subtrair média e dividir pelo desvio. | Equilibrar escalas para distância e regularização. | StandardScaler dentro do pipeline. Árvores não exigem escala, mas compartilham preparação. |
| Pipeline | Sequência ajustável de preparação e modelo. | Evitar divergência e vazamento no pré-processamento. | Cada fold ajusta imputação, escala e codificação somente no passado autorizado. |
| Vazamento / leakage | Informação indisponível na decisão entra no aprendizado. | Explicar resultados artificialmente bons. | Alvo, exposure e identificadores ficam fora de X. Não auditamos integralmente o cálculo original de features anônimas. |
| Split temporal | Separação por ordem de ocorrência. | Avaliar um futuro posterior ao desenvolvimento. | Treino 1–107, validação 108–134, calibração 135–152, teste 153–180. |
| Fold | Uma rodada interna de ajuste e avaliação. | Comparar configurações sem usar o teste final. | Três folds temporais dentro do treino, com blocos futuros de dez dias. |
| Parâmetro | Quantidade que o ajuste aprende. | Formar a função preditiva. | Coeficientes da logística ou regras aprendidas por árvores. |
| Hiperparâmetro | Configuração escolhida antes de ajustar um estimador. | Controlar complexidade e aprendizado. | Profundidade, tamanho mínimo de folha, regularização e número de vizinhos. Grades pequenas no código. |
| Regularização | Penalização da complexidade do ajuste. | Reduzir variabilidade e sensibilidade a particularidades. | Ridge, Lasso e ElasticNet. Não garante automaticamente melhor desempenho. |
| Sobreajuste | Modelo aprende particularidades do ajuste que generalizam mal. | Interpretar diferenças entre ajuste e teste. | AP Extra Trees 0,895 no ajuste e 0,379 no teste. Mudança temporal também pode contribuir; não a isolamos. |
| Score | Número que ordena casos. | Construir classificação ou priorização. | Probabilidade bruta ou calibrada. Na política principal usamos probabilidade calibrada × montante. |
| Limiar / threshold | Corte que converte score em classe. | Gerar decisão binária e matriz de confusão. | 0,16 para Extra Trees, escolhido por F1 na validação. Não define a fila monetária. |
| Precisão | TP dividido por TP+FP. | Avaliar qualidade dos alertas. | Matriz do campeão: 231/621 = 37,2%. Fila monetária: 96/333 = 28,8%. São seleções diferentes. |
| Recall / sensibilidade | TP dividido por TP+FN. | Medir quantas fraudes encontramos. | Matriz: 231/530 = 43,6%. Fila: 96/530 = 18,1%. Não equivale à cobertura em dólares. |
| F1 | Média harmônica de precisão e recall. | Equilibrar essas duas métricas para limiar. | 0,401 no teste do campeão com limiar fixo. Não usa montante. |
| Acurácia | Fração de todas as classes corretas. | Resumo global, com risco de mascarar minoria. | Sempre-legítima já atinge 96,67% no teste e perde todas as fraudes. |
| ROC-AUC | Área da curva recall versus taxa de falsos positivos. | Avaliar discriminação ao variar limiares. | Extra Trees 0,859 no teste. Não é porcentagem de fraudes encontradas. |
| Average precision / AP | Resumo da precisão ao aumentar o recall. | Avaliar ranking com classe rara. | Extra Trees 0,379. HistGB 0,454 no teste. AP não é necessariamente a integral trapezoidal chamada PR-AUC. |
| Brier | Média de (probabilidade − rótulo)². | Avaliar erro probabilístico. | Extra Trees: 0,025902 bruto e 0,025697 calibrado no teste. Menor é melhor, mas um valor isolado não prova calibração perfeita. |
| Calibração | Aproximar probabilidade prevista da frequência observada. | Tornar valores probabilísticos mais coerentes. | Platt em bloco separado. A correção é pequena no Brier do campeão. |
| Logit e Platt | Logit é log(p/(1−p)); Platt ajusta transformação logística. | Recalibrar scores sem reajustar o classificador. | Probabilidades limitadas antes do logit. C=1 no ajuste de calibração. |
| Discriminação | Capacidade de ordenar positivos acima de negativos. | Distinguir ranking de calibração. | Uma transformação monotônica preserva ordem de p, mas pode mudar ordem de p × valor. |
| MAE | Média dos erros absolutos. | Medir erro em unidade monetária. | RF regressor: US$ 8,30. Zero tem MAE menor porque o alvo tem muitos zeros. |
| MSE | Média dos erros ao quadrado. | Penalizar erros grandes e buscar média condicional. | Critério de escolha da regressão. RF no teste: cerca de 1.597,10 US$². |
| RMSE | Raiz do MSE. | Ler erro quadrático na unidade original. | RF: US$ 39,96 no teste, contra US$ 30,54 no ajuste final. |
| R² | 1 menos a razão entre erro quadrático e variação em torno da média. | Comparar regressão com referência constante no conjunto avaliado. | RF: 0,247 no teste. Pode ser negativo. Não é métrica de classificação nem cobertura de fraude. |
| Exposição rotulada | Montante multiplicado pelo indicador de fraude. | Construir alvo contínuo e medir valor na seleção. | Zero para legítima, montante para fraude. Não é prejuízo líquido registrado. |
| Valor esperado | Média ponderada pelos possíveis resultados. | Ligar probabilidade ao dinheiro em risco. | Para montante conhecido A, exposição esperada ideal = A × P(fraude | X). |
| Baseline / referência | Regra ou modelo usado para comparação. | Medir contribuição incremental. | Maiores valores é referência primária escolhida na validação. Logística é diagnóstico adicional. |
| Capacidade | Quantidade disponível de revisões. | Comparar decisões com trabalho equivalente. | ceil(0,02 × n_dia). São 333 análises no teste pelo arredondamento diário. |
| Recall monetário | Valor de fraude selecionado / valor de fraude total. | Medir cobertura financeira. | 44,53% no modelo principal, apesar de recall em quantidade de 18,11%. |
| Eficácia | Fração do valor identificado que se assume evitar ou recuperar. | Converter captura em benefício simulado. | 80% no cenário central, 50% na sensibilidade. Não estimada na base. |
| Benefício incremental | Benefício do modelo menos o da referência. | Isolar o acréscimo da nova política. | US$ 16.352,90 contra maiores valores. US$ 4.785,62 contra logística, em comparação adicional. |
| Perda simulada | Exposição total rotulada menos benefício líquido simulado. | Definir denominador financeiro coerente. | Na referência: US$ 67.781,26. A redução de 24,13% usa esse denominador. |
| Bootstrap pareado em blocos | Reamostragem que conserva blocos temporais iguais nas políticas. | Explorar variação da diferença de resultado. | 5.000 réplicas, blocos circulares de sete dias. Intervalo principal: US$ 11,87 mil–21,33 mil. |
| Intervalo exploratório | Faixa gerada pelo procedimento de reamostragem. | Mostrar incerteza do recorte. | Não cobre automaticamente hipóteses de eficácia nem garante ganhos futuros; só há 28 dias de teste. |
| Clustering | Agrupamento sem fornecer alvo. | Explorar estrutura e perfis. | 2.000 transações de treino e nove indicadores. Rótulo consultado após agrupar. |
| Silhouette | Compara proximidade no grupo e separação entre grupos. | Avaliar estrutura interna do agrupamento. | K-means k=2: 0,552. Hierárquico k=2: 0,580. Valores maiores tendem a ser melhores. |
| Davies–Bouldin / DB | Relaciona dispersão interna e separação entre grupos. | Complementar avaliação de compactação e separação. | K-means 0,833 e hierárquico 0,756 em k=2. Menor tende a ser melhor. |
| Ruído em DBSCAN | Pontos fora das regiões densas definidas pelo método. | Avaliar quanto da amostra fica sem grupo. | eps=1,5: 9% de ruído. Não equivale a fraude e afeta comparação de índices. |
| PCA / componente | Nova coordenada linear que concentra variância dos atributos. | Projetar e resumir estrutura. | 2 componentes: 56,53% de variância acumulada; 5: 89,02%. |
| Loading / peso | Coeficiente do atributo numa componente de PCA. | Interpretar como a projeção se forma. | PC1 dá maiores pesos a C13, C1 e C2. Códigos anônimos limitam significado de negócio. |
| ARI | Concordância entre agrupamentos, ajustada pelo acaso. | Avaliar estabilidade na mesma amostra. | ARI=1 nas três sementes adicionais do K-means. Não garante estabilidade em outra amostra. |
| Importância por permutação | Piora ao embaralhar um atributo. | Avaliar dependência preditiva da entrada. | Calculada na calibração por queda de AP. V200, V70, D2, M4 e card6 lideram. Correlação pode dividir importância. |
| Drift / mudança temporal | Distribuições ou relações mudam com o tempo. | Explicar instabilidade e planejar monitoramento. | Prevalências variam entre blocos. Diferença de ajuste e teste não separa drift de sobreajuste. |
| Causalidade e contrafactual | Efeito da ação e resultado alternativo que não observamos. | Distinguir avaliação de ranking de impacto real da investigação. | Não houve experimento de intervenção. Benefício depende da eficácia assumida. |

## As 19 técnicas e os resultados

Baselines, limiares e cenários não contam como técnicas adicionais. A tabela completa é material de defesa, não texto para ler durante os 15 minutos.


### Classificação: sete técnicas

#### Logistic

**Ideia:** Combinação linear e função logística.

**Para que serve:** Referência simples de risco com probabilidades interpretáveis no espaço transformado.

**Uso no projeto:** configuração selecionada `{"C": 1.0}`. C=1. A relação é linear no logit e pode perder interações.

**Resultado no teste:** AP=0.340, F1=0.363, recall=0.340, ROC-AUC=0.832.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### DecisionTree

**Ideia:** Divisões sucessivas por regras.

**Para que serve:** Capturar não linearidades e interações.

**Uso no projeto:** configuração selecionada `{"max_depth": 12, "min_samples_leaf": 15}`. A profundidade e o mínimo de exemplos por folha controlam complexidade.

**Resultado no teste:** AP=0.377, F1=0.429, recall=0.353, ROC-AUC=0.812.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### RandomForest

**Ideia:** Média ou voto de árvores com amostragem e atributos aleatórios.

**Para que serve:** Reduzir variabilidade de uma árvore isolada.

**Uso no projeto:** configuração selecionada `{"max_depth": 18, "min_samples_leaf": 3}`. 60 árvores. A importância não deve ser confundida com causalidade.

**Resultado no teste:** AP=0.448, F1=0.479, recall=0.409, ROC-AUC=0.871.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### ExtraTrees

**Ideia:** Conjunto de árvores com cortes mais aleatórios.

**Para que serve:** Diversificar árvores e modelar interações.

**Uso no projeto:** configuração selecionada `{"max_depth": 20, "min_samples_leaf": 3}`. 60 árvores. Mais aleatoriedade não garante resultado melhor.

**Resultado no teste:** AP=0.379, F1=0.401, recall=0.436, ROC-AUC=0.859. **Campeão escolhido na validação.**

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### HistGradientBoosting

**Ideia:** Árvores sequenciais com cortes acelerados por histogramas.

**Para que serve:** Corrigir erros sucessivamente.

**Uso no projeto:** configuração selecionada `{"max_leaf_nodes": 31, "l2_regularization": 20.0}`. 120 iterações fixas. Número de folhas e penalização L2 passam pela grade.

**Resultado no teste:** AP=0.454, F1=0.459, recall=0.455, ROC-AUC=0.876.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### KNN

**Ideia:** Vizinhos no espaço transformado.

**Para que serve:** Comparar uma hipótese baseada em proximidade.

**Uso no projeto:** configuração selecionada `{"n_neighbors": 45}`. 45 vizinhos escolhidos. Distância pode perder qualidade em muitas dimensões.

**Resultado no teste:** AP=0.304, F1=0.358, recall=0.275, ROC-AUC=0.797.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### GaussianNB

**Ideia:** Bayes com distribuições gaussianas e independência condicional.

**Para que serve:** Referência probabilística rápida com outra hipótese.

**Uso no projeto:** configuração selecionada `{"var_smoothing": 0.001}`. Hipóteses podem ser inadequadas com atributos correlacionados.

**Resultado no teste:** AP=0.086, F1=0.144, recall=0.602, ROC-AUC=0.742.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


### Regressão: oito técnicas

#### Linear

**Ideia:** Soma ponderada das entradas para alvo contínuo.

**Para que serve:** Referência linear de exposição.

**Uso no projeto:** configuração selecionada `{}`. Sem penalização. Entradas transformadas e previsões negativas truncadas em zero.

**Resultado no teste:** MAE=US$ 11.23, MSE=2056.46 US$², RMSE=US$ 45.35, R²=0.030.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### Ridge

**Ideia:** Regressão linear com penalização quadrática.

**Para que serve:** Estabilizar coeficientes com correlação.

**Uso no projeto:** configuração selecionada `{"alpha": 100.0}`. alpha=100 escolhido.

**Resultado no teste:** MAE=US$ 11.19, MSE=2053.54 US$², RMSE=US$ 45.32, R²=0.031.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### Lasso

**Ideia:** Regressão linear com penalização de magnitudes.

**Para que serve:** Reduzir complexidade e eventualmente zerar coeficientes.

**Uso no projeto:** configuração selecionada `{"alpha": 0.1}`. alpha=0,1. Não interpretamos seleção como prova causal.

**Resultado no teste:** MAE=US$ 10.87, MSE=2052.23 US$², RMSE=US$ 45.30, R²=0.032.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### ElasticNet

**Ideia:** Mistura de penalizações L1 e L2.

**Para que serve:** Comparar compromisso entre Lasso e Ridge.

**Uso no projeto:** configuração selecionada `{"alpha": 0.1}`. alpha=0,1 e l1_ratio=0,5 fixo.

**Resultado no teste:** MAE=US$ 10.83, MSE=2054.33 US$², RMSE=US$ 45.32, R²=0.031.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### DecisionTree

**Ideia:** Divisões sucessivas por regras.

**Para que serve:** Capturar não linearidades e interações.

**Uso no projeto:** configuração selecionada `{"max_depth": 5, "min_samples_leaf": 50}`. A profundidade e o mínimo de exemplos por folha controlam complexidade.

**Resultado no teste:** MAE=US$ 8.25, MSE=1790.86 US$², RMSE=US$ 42.32, R²=0.155.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### RandomForest

**Ideia:** Média ou voto de árvores com amostragem e atributos aleatórios.

**Para que serve:** Reduzir variabilidade de uma árvore isolada.

**Uso no projeto:** configuração selecionada `{"max_depth": 15, "min_samples_leaf": 5}`. 60 árvores. A importância não deve ser confundida com causalidade.

**Resultado no teste:** MAE=US$ 8.30, MSE=1597.10 US$², RMSE=US$ 39.96, R²=0.247. **Campeão escolhido na validação.**

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### ExtraTrees

**Ideia:** Conjunto de árvores com cortes mais aleatórios.

**Para que serve:** Diversificar árvores e modelar interações.

**Uso no projeto:** configuração selecionada `{"max_depth": 15, "min_samples_leaf": 5}`. 60 árvores. Mais aleatoriedade não garante resultado melhor.

**Resultado no teste:** MAE=US$ 8.67, MSE=1772.34 US$², RMSE=US$ 42.10, R²=0.164.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


#### HistGradientBoosting

**Ideia:** Árvores sequenciais com cortes acelerados por histogramas.

**Para que serve:** Corrigir erros sucessivamente.

**Uso no projeto:** configuração selecionada `{"max_leaf_nodes": 15, "l2_regularization": 50.0}`. 120 iterações fixas. Número de folhas e penalização L2 passam pela grade.

**Resultado no teste:** MAE=US$ 8.06, MSE=1574.02 US$², RMSE=US$ 39.67, R²=0.257.

**Como defender:** a configuração usa folds internos; o resultado do teste avalia a escolha, sem permitir trocá-la retrospectivamente.


### Não supervisionado: quatro técnicas

| Técnica | Ideia e finalidade | Uso e achado | Limite de interpretação |
|---|---|---|---|
| K-means | Centros que reduzem distâncias quadráticas internas | k de 2 a 6. k=2: silhouette 0,552, grupos 1.880 e 120 | Escala e formato dos grupos importam. Taxa de fraude é posterior |
| Hierárquico | Uniões sucessivas, com corte da hierarquia | k de 2 a 6. k=2: silhouette 0,580 e DB 0,756 | Índice interno maior não prova utilidade operacional |
| DBSCAN | Regiões densas e pontos sem grupo | eps 0,7/1/1,5/2, min_samples=10. eps=1,5: 9% de ruído | Índices calculados nos não-ruído. Ruído não é fraude |
| PCA | Projeção linear de variância máxima | 2 componentes: 56,53%, 5: 89,02%. PC1 com maior peso em C13/C1/C2 | Variância explicada não é poder de detecção nem causalidade |


## A conta financeira e as comparações

**Universo do teste:** 15.915 transações, 530 fraudes e US$ 78.851,255 de exposição rotulada.

**Capacidade:** teto por dia, `ceil(0,02 × n_dia)`. São 333 análises, um pouco mais de 2% do total agregado pelo arredondamento.

**Conta central:**

```text
Benefício líquido = eficácia × valor rotulado selecionado − custo × análises
Modelo = 0,8 × 35.111,123 − 2 × 333 = US$ 27.422,8984
Referência = 0,8 × 14.670 − 2 × 333 = US$ 11.070
Incremento = 27.422,8984 − 11.070 = US$ 16.352,8984
Perda da referência = 78.851,255 − 11.070 = US$ 67.781,255
Redução relativa = 16.352,8984 / 67.781,255 = 24,13%
```

A referência primária é maiores valores, escolhida na validação. Contra logística, o ganho adicional é US$ 4.785,62 e a redução da perda simulada da logística é 8,51%. As duas comparações usam denominadores diferentes.

### O que observamos, assumimos e concluímos

| Categoria | Conteúdo |
|---|---|
| Observado na avaliação | Valores, rótulos, filas selecionadas e montantes de fraude nessas filas |
| Assumido | Eficácia de 80%, US$ 2 por análise e penalidade adicional zero por revisão legítima |
| Não medido | Efeito real de investigar, recuperação efetiva, atraso, implantação e manutenção |
| Conclusão | Benefício incremental simulado positivo neste teste, condicionado às hipóteses |

### Comparação de todas as políticas na capacidade principal

| Política | Fraudes selecionadas | Valor identificado (US$) | Benefício simulado (US$) |
|---|---:|---:|---:|

| Random | 11 | 881.03 | 38.82 |

| LargestAmount | 17 | 14670.00 | 11070.00 |

| ProductRateAmount | 16 | 10290.01 | 7566.01 |

| ML_Probability | 168 | 18896.14 | 14450.92 |

| ML_ExpectedAmount | 96 | 35111.12 | 27422.90 |

| RegressionExposure | 105 | 36919.51 | 28869.60 |


**Insight:** probabilidade isolada encontra 168 fraudes e US$ 18.896,14. Probabilidade × valor encontra 96 fraudes e US$ 35.111,12. A segunda política captura mais dinheiro, embora encontre menos casos. A matriz com 231 verdadeiros positivos usa outra decisão, um limiar fixo.

**Resultado secundário:** o regressor captura mais valor que a política primária neste teste. Não mudamos a política principal a partir desse resultado.

**Sensibilidade:** eficácia de 50% produz US$ 10.220,56 de incremento. Custo igual por análise se cancela na diferença de filas de tamanho igual, sem penalidade adicional. A penalidade por legítima pode mudar a diferença. O intervalo exploratório principal é US$ 11.865,42–21.326,99 e mantém as hipóteses fixas. Não anualizamos.


## Explicações passo a passo

Este material aprofunda as decisões da fala. As equações e tabelas executáveis estão no notebook.


### Etapa 2: Origem, arquivos e significado da base
A IEEE-CIS Fraud Detection foi disponibilizada por Vesta e IEEE-CIS no Kaggle. O conjunto público rotulado possui 590.540 transações e 20.663 fraudes. `isFraud` é o rótulo, `TransactionAmt` informa valor e `TransactionDT` é um deslocamento temporal em segundos. Ele não fornece uma data civil conhecida.

Baixamos o espelho OpenML 46858, indicado pelo projeto Empulse. O parquet preserva `TransactionDT`, mas não `TransactionID`. Criamos `source_row`, um identificador de linha sem uso preditivo. O espelho contém 456 campos, incluindo variantes de nomes de atributos de identidade. Utilizamos uma lista predefinida de 71 atributos, não todos os campos nem os identificadores.

Atributos C, D, V e parte de id são anonimizados. Conhecemos famílias gerais, mas não podemos inventar o significado de cada coluna. A disponibilização pública de um atributo não demonstra, sozinha, que seu cálculo original estava livre de informação futura; essa é uma limitação de proveniência.

Fontes: [competição](https://www.kaggle.com/competitions/ieee-fraud-detection/data), [metadados OpenML](https://www.openml.org/d/46858), [documentação Empulse](https://empulse.readthedocs.io/en/latest/guide/datasets/ieee_fraud_detection.html). Os hashes registram os arquivos locais. O MD5 nos metadados se refere ao ARFF, não ao parquet baixado; não alegamos que o verificamos contra o parquet.

#### Passo a passo: conhecer a base antes de modelar
Leia primeiro a origem e depois a unidade de cada campo. `TransactionAmt` é um valor em dólares; `isFraud` é uma variável binária, com 1 para fraude; `TransactionDT` ordena eventos por um deslocamento em segundos. Nenhum desses campos prova o prejuízo líquido da instituição.

Uma base pública de competição é adequada para testar métodos com rótulos conhecidos. Ela não equivale à base operacional completa de uma empresa. O espelho é uma forma de acesso: preservamos sua origem e o hash do arquivo, sem tratar o OpenML como o produtor original dos eventos.

**Como ler a auditoria a seguir:** procure quantidade de linhas, fraudes, colunas originais e linhas usadas. São universos diferentes: arquivo original, amostra de avaliação e amostra usada em cada ajuste. Não use “treinamos com 590 mil transações” para descrever um ajuste limitado a 30 mil.

**Se perguntarem o significado de V130:** “É um atributo anonimizado. Posso explicar seu tratamento e sua importância estatística, mas a documentação disponível não permite dar um significado de negócio específico.”

### Etapa 3: Unidade de análise, amostra e limites
Uma linha é uma transação, não um cliente. Selecionamos uma em cada cinco linhas do arquivo, sem olhar classe ou valor, e excluímos os dois dias extremos para evitar orçamentos em dias parciais. A amostra tem 116.533 transações e 4.046 fraudes.

O orçamento operacional vale para essa amostra e não corresponde automaticamente à capacidade da empresa inteira. O sorteio de treino usa no máximo 30 mil linhas por ajuste, sem reequilibrar artificialmente as classes. Isso torna viável comparar dezenove técnicas. Todos os algoritmos recebem a mesma amostra de cada bloco autorizado. A avaliação usa todas as linhas dos respectivos blocos da amostra sistemática.

Não há chave confiável de cliente para impedir que o mesmo indivíduo apareça em períodos diferentes. O teste temporal avalia um fluxo posterior, não generalização a clientes inéditos. Valores e taxas não podem ser extrapolados para todo o mercado.

#### Passo a passo: por que reduzir a base?
A seleção sistemática conserva aproximadamente um quinto das linhas e torna o estudo executável. Como o critério é a posição da linha, ele não favorece intencionalmente fraude ou valores altos. Contudo, não é uma amostra aleatória simples: se a ordenação tivesse periodicidade relacionada ao risco, poderia introduzir viés. Por isso, não afirmamos representatividade garantida.

Há duas reduções diferentes: a amostra sistemática define o universo deste estudo; o limite de 30 mil reduz o custo de cada treinamento. O teste mantém todas as transações da amostra no seu intervalo, sem escolher apenas os casos fáceis.

**Leia a tabela:** `start` e `end` indicam o intervalo temporal; as quantidades mostram o peso de cada bloco. Compare a prevalência entre blocos: mudança na frequência de fraude pode afetar probabilidades e métricas.

**Resposta de defesa:** “Usamos a mesma regra de amostragem e os mesmos períodos para comparar os modelos. Uma extensão seria repetir o estudo em outras amostras e na base completa.”

### Etapa 4: Limpeza e preparação
Ausências podem ser informativas: dados de dispositivo nem sempre existem. Valores numéricos ausentes recebem mediana aprendida no treino, e indicadores adicionais registram a ausência. Categorias ausentes recebem uma categoria explícita. Categorias raras são agrupadas e categorias novas não interrompem a previsão.

One-hot encoding evita impor ordem a códigos de cartão, região e produto. Padronização reduz diferenças de escala em regressões regularizadas e KNN. Árvores não precisam de escala, mas usamos o mesmo pipeline para comparação consistente. Preços extremos não são apagados apenas por serem grandes: podem representar exposição relevante.

A fração de ausência registrada na auditoria refere-se aos campos efetivamente lidos, e não necessariamente a todos os 456 campos do espelho. Não interpretamos códigos anônimos como variáveis pessoais identificadas.

#### Passo a passo: o que o pré-processamento aprende?
**Imputação:** se os valores de treino são 10, 20 e ausente, a mediana dos observados é 15. O ausente recebe 15. No teste, usamos essa mediana já aprendida; não recalculamos com o futuro.

**Indicador de ausência:** registra que o valor original não estava disponível. Isso diferencia um 15 observado de um 15 imputado, quando o indicador existe no pipeline.

**One-hot:** uma categoria como ProductCD=W vira uma coluna indicadora, não o número ordinal “5”. Cartões e regiões codificados são tratados como categorias quando assim definidos na lista CAT.

**Padronização:** subtrai a média e divide pelo desvio do treino. Em KNN, isso impede que uma variável domine a distância apenas por sua unidade. Em regularização, torna a penalização mais comparável entre variáveis.

**Pipeline:** encadeia as transformações e o estimador. Cada fold executa `fit` apenas no passado e `predict` no bloco posterior. Preencher ausências em toda a base antes da validação contaminaria a comparação.

**Cuidado ao ler:** ausência alta não determina remoção automática. Primeiro verificamos se a informação disponível é útil e coerente com o momento da decisão.

### Etapa 5: Engenharia de atributos e prevenção de vazamento
Usamos valor da transação, distâncias, famílias C/D, quinze atributos V predefinidos, códigos categóricos e presença de dispositivo. `hour_sin` e `hour_cos` representam o ciclo horário extraído do deslocamento; como a origem real é desconhecida, não afirmamos que correspondem à hora local do consumidor. `missing_count` resume ausência nos campos lidos.

O rótulo, a exposição monetária rotulada, o identificador de linha e o dia relativo ficam fora de X. Não construímos agregações futuras por cartão. As transformações são ajustadas dentro de cada fold. O valor da transação é conhecido no momento de triagem e pode entrar no modelo; o fato de a transação ser fraude só aparece como alvo.

A lista de atributos foi definida antes de olhar o teste. A importância por permutação é calculada na calibração para explicar o modelo, sem eliminar atributos depois de avaliar o teste.

#### Passo a passo: reconhecer vazamento
Faça sempre a pergunta: **esse valor existiria antes de eu decidir investigar?** O montante da transação existe; o rótulo confirmado posteriormente não. Uma média por cartão calculada usando transações futuras também não existiria naquele momento.

`exposure` é permitido como **alvo**, mas seria vazamento como **entrada**, pois contém `isFraud`. `source_row` identifica registros e resolve empates; não representa risco aprendido. O dia relativo separa os períodos e controla capacidade, mas não entra no classificador.

As features cíclicas usam seno e cosseno para aproximar horários vizinhos na virada de um ciclo: o começo e o fim ficam próximos. Não afirmamos conhecer a hora civil real.

**Limite da conclusão:** nosso pipeline controla o vazamento que podemos observar no experimento. Não temos a documentação interna necessária para auditar integralmente a produção dos atributos anonimizados.

### Etapa 6: Protocolo temporal e orçamento computacional
Separamos dias inteiros: treino 1–107, validação 108–134, calibração 135–152 e teste 153–180. São dias relativos, sem associação a uma data civil. O teste tem 28 dias, com 15.915 transações e 530 fraudes.

Dentro do treino, três janelas futuras de dez dias comparam pequenas grades. Só o bloco anterior é usado para ajustar o pipeline. O treino de cada estimador recebe até 30 mil linhas sorteadas com semente 42. Depois da escolha, o ajuste final recebe uma amostra de até 30 mil linhas de treino + validação. A regra simples por produto também é reajustada nesses dois blocos para o teste.

A validação escolhe o classificador pelo valor fraudulento identificado ao revisar 2% por dia usando score bruto × valor. Ela escolhe ainda um limiar F1 para diagnóstico. A calibração ajusta probabilidades por Platt. A política principal, sua capacidade de 2% e os custos centrais foram declarados antes do teste.

#### Passo a passo: quem pode olhar quais dados?
| Etapa | Aprende com | Decide o quê? |
|---|---|---|
| Busca de hiperparâmetros | Folds internos do treino | Configuração de cada algoritmo |
| Comparação de algoritmos | Validação posterior | Campeão e referência simples |
| Ajuste final | Treino + validação, respeitando o limite amostral | Parâmetros do modelo escolhido |
| Calibração | Bloco próprio posterior | Conversão do score em probabilidade |
| Teste | Somente avaliação | Resultado final do protocolo congelado |

Um **parâmetro** é aprendido no ajuste, como um coeficiente. Um **hiperparâmetro** é uma configuração escolhida antes desse ajuste, como a profundidade de uma árvore. Um **fold** é uma rodada com seu próprio treino e avaliação interna.

O teste não escolhe o campeão. Se um concorrente ganha no teste, relatamos a informação e mantemos a escolha anterior. Alterar a seleção após ler esse resultado exigiria um novo período intocado para sustentar uma nova avaliação final.

**Pergunta provável: por que não split aleatório?** “Queremos avaliar transações posteriores às usadas para aprender. Um split aleatório misturaria passado e futuro e poderia produzir uma estimativa otimista para esse uso.”

**Ponto crítico:** o classificador é escolhido com probabilidades brutas na validação e a política final utiliza probabilidades calibradas. Mantivemos o protocolo. Não afirmamos que essa sequência garante o melhor modelo monetário possível.

### Etapa 7: Técnicas e hipóteses
São **19 técnicas**: sete classificadores, oito regressores, K-means, hierárquico, DBSCAN e PCA. Baselines e ajustes de política não contam como novas técnicas.

| Família | Técnicas | Por que testar |
|---|---|---|
| Classificação | Logística, Árvore, Random Forest, Extra Trees, HistGradientBoosting, KNN, GaussianNB | Relações lineares, regras, ensembles, vizinhança e Bayes |
| Regressão | Linear, Ridge, Lasso, ElasticNet, Árvore, Random Forest, Extra Trees, HistGradientBoosting | Estimar exposição monetária média e comparar regularização com não linearidade |
| Não supervisionado | K-means, Hierárquico, DBSCAN, PCA | Estrutura, perfis, pontos esparsos e projeção |

Random Forest agrega árvores com amostragem e aleatoriedade de atributos. Extra Trees acrescenta aleatoriedade de cortes. Boosting constrói árvores em sequência. GaussianNB assume independência condicional, improvável em atributos correlacionados. KNN depende da definição de distância e escala. Nenhuma técnica é superior por princípio.

#### Passo a passo: diferenciar as técnicas sem decorar nomes
| Técnica | Ideia para explicar | Principal cuidado |
|---|---|---|
| Logística | Soma ponderada das entradas e função que produz probabilidade | Fronteira linear no espaço transformado |
| Árvore | Perguntas sucessivas dividem as transações | Pode memorizar particularidades do treino |
| Random Forest | Combina árvores diversas para reduzir variabilidade | Complexidade e interpretação |
| Extra Trees | Usa cortes mais aleatórios para diversificar árvores | Mais aleatoriedade não garante maior ganho |
| HistGradientBoosting | Árvores sequenciais corrigem erros; histogramas agilizam cortes | Configuração e sobreajuste |
| KNN | Consulta exemplos próximos | Distância perde qualidade em muitas dimensões |
| GaussianNB | Combina evidências sob hipóteses probabilísticas simples | Independência e distribuição podem ser inadequadas |
| Ridge | Penaliza coeficientes ao quadrado | Intensidade da penalização |
| Lasso | Penaliza magnitudes e pode zerar coeficientes | Seleção instável entre variáveis correlacionadas |
| ElasticNet | Mistura penalizações de Ridge e Lasso | Precisa configurar força e mistura |

**Bagging e boosting:** florestas combinam árvores construídas com diversidade; boosting adiciona modelos em sequência. Não confunda quantidade de árvores com quantidade de técnicas.

**Como justificar o conjunto:** “Incluímos modelos simples e famílias com hipóteses diferentes. Isso permite avaliar se a complexidade acrescenta resultado, em vez de supor que o algoritmo mais sofisticado vencerá.”

### Etapa 8: Classificação e escolha do algoritmo
A classe positiva é fraude. Como ela é rara, acurácia isolada é enganosa: prever tudo como legítimo pode acertar quase todas as linhas e não identificar fraude alguma.

MAE e R² não são métricas da classificação. Usamos precisão, recall, F1, ROC-AUC, average precision e Brier. Average precision resume a curva precisão–recall e deve ser comparada à prevalência; não é a mesma integral trapezoidal frequentemente chamada de PR-AUC.

O campeão é escolhido pela validação e fica congelado. Não mudamos de campeão porque outro teve maior AP no teste. O objetivo de priorização monetária também pode selecionar um modelo diferente do maior F1.

#### Passo a passo: ler as métricas de classificação
Considere TP = fraudes corretamente sinalizadas, FP = legítimas sinalizadas, FN = fraudes não sinalizadas e TN = legítimas não sinalizadas.

- **Precisão = TP/(TP+FP):** dentre os alertas, quantos são fraude?
- **Recall = TP/(TP+FN):** dentre as fraudes, quantas foram encontradas?
- **F1 = 2 × precisão × recall/(precisão+recall):** equilíbrio entre as duas, sem considerar montante.
- **ROC-AUC:** qualidade da ordenação entre positivos e negativos ao variar o limiar.
- **Average precision (AP):** resumo da precisão ao aumentar o recall; especialmente informativa com classe rara. Sua referência depende da prevalência.
- **Brier:** média de `(probabilidade − rótulo)²`; menor é melhor para erro probabilístico.

Uma acurácia alta pode vir de ignorar a minoria. Uma AP alta também não determina qual fila captura mais dólares. Portanto, mostramos métricas preditivas e uma avaliação da decisão econômica.

**Como ler as tabelas:** identifique primeiro `split`; depois a coluna usada para escolher o campeão; só então compare os resultados de teste. AP e ROC-AUC são números entre 0 e 1, não percentuais de transações corretamente identificadas.

**Resposta de defesa:** “Extra Trees não foi escolhido por ter todas as melhores métricas no teste. Foi o escolhido pelo critério monetário na validação.”

### Etapa 9: Limiar e matriz de confusão
O limiar F1 foi escolhido na validação e aplicado ao score bruto. Ele produz uma decisão binária que serve ao diagnóstico. A fila econômica é outra decisão: ordena probabilidade calibrada × valor e preenche a capacidade diária. Ela não utiliza automaticamente o limiar F1.

Falso negativo é uma fraude fora da seleção. Falso positivo é uma transação legítima revisada. Revisar não é bloquear: o projeto representa triagem para investigação, com atraso e eficácia assumidos. Não demonstramos prevenção em tempo real ou recuperação garantida.

#### Passo a passo: dois critérios produzem duas matrizes diferentes
O limiar F1 compara cada score com um valor fixo. A fila econômica escolhe os melhores scores monetários dentro de cada dia. Os grupos selecionados não precisam ser iguais.

A matriz exibida a seguir refere-se ao diagnóstico do limiar, não aos 333 casos da fila financeira. No teste, os números do diagnóstico são TN=14.995, FP=390, FN=299 e TP=231. Já a fila monetária principal contém 96 fraudes entre 333 análises.

**Por que 231 não é melhor que 96?** O primeiro número utiliza mais alertas e outra regra de seleção. A comparação financeira exige igual capacidade e considera o valor das fraudes. Misturar esses números levaria a uma conclusão errada.

**Resposta de defesa:** “O limiar ajuda a entender a classificação. Nossa decisão operacional principal é um ranking diário com capacidade fixa.”

### Etapa 10: Probabilidade calibrada e valor esperado
Platt ajusta uma regressão logística entre logit do score bruto e o rótulo no bloco de calibração. O modelo preditivo não é reajustado com os rótulos desse bloco. Avaliamos Brier bruto e calibrado no teste.

Multiplicar uma probabilidade por um valor conhecido produz uma estimativa de exposição esperada se a probabilidade for adequada. A calibração pode ser imperfeita, especialmente em subgrupos e em períodos futuros. Ser monotônica preserva a ordem de probabilidade isolada, mas pode mudar a ordem de probabilidade × valor.

#### Passo a passo: probabilidade não é certeza
Dizer “probabilidade de 20%” significa que, em conjuntos comparáveis com esse risco, esperamos algo próximo de 20 fraudes a cada 100 transações se o modelo estiver bem calibrado. Não sabemos quais serão elas.

**Discriminação** é ordenar os casos; **calibração** é aproximar as probabilidades das frequências observadas. Um modelo pode ordenar bem e ser excessivamente confiante.

Platt aprende uma transformação usando um bloco separado. Como `logit(p)=log(p/(1−p))`, os scores são limitados antes da transformação para evitar logaritmos de zero. A transformação não consulta os rótulos de teste.

**Leia o gráfico:** distâncias da diagonal indicam discrepâncias entre risco previsto e frequência. Grupos com poucos exemplos têm estimativas instáveis. Brier menor no período avaliado não garante calibração perfeita em todos os subgrupos.

**Importância por permutação:** embaralha uma entrada e mede a piora. É uma associação com a previsão, não prova de causa. Variáveis correlacionadas podem dividir ou esconder importância.

### Etapa 11: Regressão de exposição monetária
Definimos `exposure = TransactionAmt × isFraud`: zero para transações legítimas, valor da transação para fraudes rotuladas. Esse é um alvo contínuo derivado, em moeda, e não o prejuízo líquido observado pela empresa. Ele reformula o mesmo risco da classificação; não representa um fenômeno independente.

O fato de o valor conhecido aparecer em X não revela o rótulo futuro. O modelo tenta aprender quanto dessa exposição estará associado a fraude. Não fornecemos `isFraud` ou `exposure` como entradas.

A distribuição tem muitos zeros e cauda pesada. MAE tende a favorecer previsões próximas de zero, enquanto erro quadrático procura a média condicional. Selecionamos por MSE de validação, alinhado a uma média esperada, mas avaliamos também MAE, RMSE e R². Um R² baixo ou negativo não invalida uma política de ranking; tampouco deve ser escondido.

#### Passo a passo: por que uma regressão neste problema?
Se uma transação legítima vale US$ 500, seu alvo de exposição rotulada é 0. Se uma fraude vale US$ 500, o alvo é 500. No momento de prever, o rótulo ainda é desconhecido.

Como o montante A é conhecido, a média condicional ideal desse alvo é `E[A × Y | X] = A × P(Y=1 | X)` quando A está contido em X. Isso explica a ligação entre regressão direta e probabilidade vezes valor. Na prática, estimadores, perdas e erros de calibração produzem rankings diferentes.

**MAE** é o erro absoluto médio, em dólares. **MSE** é a média dos erros ao quadrado, em dólares². **RMSE** é a raiz do MSE, volta à unidade monetária e dá mais peso aos erros grandes. **R² = 1 − SSE/SST** compara o erro quadrático com uma referência constante baseada na média do próprio conjunto avaliado; pode ser negativo.

O R² do regressor escolhido fica próximo de 0,25 no teste. Não escondemos esse resultado nem buscamos um R² artificialmente alto. A utilidade de priorização é medida separadamente, com o orçamento fixo.

**Resposta de defesa:** “Não estamos prevendo o montante, que já é conhecido. Estamos estimando quanto desse montante está associado ao evento fraude.”

### Etapa 12: Agrupamento de transações e PCA
Agrupamos duas mil transações sorteadas apenas do treino, sem usar rótulos. Nove indicadores numéricos passam por mediana, log1p após truncamento inferior em zero, e padronização. Essa transformação reduz o domínio de caudas. O truncamento é uma escolha para essa análise exploratória e pode perder informação de sinais negativos.

Comparamos k de 2 a 6 em K-means e hierárquico e quatro eps de DBSCAN. Silhouette favorece separação, Davies–Bouldin favorece grupos compactos e distintos. DBSCAN calcula métricas apenas nos pontos não marcados como ruído, exigindo mostrar a fração excluída. Um único grupo não tem silhouette definido.

PCA maximiza variância e produz uma projeção linear. Os coeficientes das componentes não são efeitos causais. A taxa de fraude dos grupos é calculada somente depois do agrupamento como descrição, não como critério usado para construí-los.

#### Passo a passo: o que os grupos realmente mostram?
**K-means:** procura centros que reduzam a distância quadrática dentro dos grupos. **Hierárquico:** constrói uniões sucessivas; o corte define quantos grupos apresentar. **DBSCAN:** procura regiões densas e pode deixar pontos como ruído. Ruído não significa fraude.

**Silhouette:** combina proximidade ao próprio grupo e separação dos demais; maior costuma ser melhor. **Davies–Bouldin:** relaciona dispersão e separação; menor costuma ser melhor. Compare também tamanho dos grupos e fração de ruído, não apenas um índice.

**PCA:** cria novas coordenadas que concentram variância. Se duas componentes não preservam toda a variância, o gráfico bidimensional omite parte da estrutura. “Variância explicada” no PCA não é o R² da regressão nem porcentagem de fraudes detectadas.

**ARI de estabilidade:** compara agrupamentos de sementes distintas, descontando concordância casual. Estabilidade ajuda a avaliar repetibilidade, mas não demonstra significado de negócio.

**Resposta de defesa:** “Usamos agrupamento para explorar perfis sem fornecer o rótulo. Consultamos a taxa de fraude depois, como descrição. Não chamamos os grupos de tipos comprovados de fraude.”

### Etapa 13: Políticas operacionais comparáveis
Todas as políticas revisam `ceil(capacidade × transações do dia)` casos, mesmo que os scores sejam baixos. Empates são resolvidos por linha de origem, sem olhar o rótulo. Isso mede ganho de priorização com orçamento fixo, não a capacidade ótima da empresa.

| Política | Score usado |
|---|---|
| Random | Sorteio reprodutível independente do rótulo |
| LargestAmount | Valor da transação |
| ProductRateAmount | Taxa histórica suavizada do produto × valor |
| ML_Probability | Probabilidade calibrada |
| ML_ExpectedAmount | Probabilidade calibrada × valor; política principal |
| RegressionExposure | Previsão do regressor de exposição |

A referência é a melhor das três regras simples na validação. Depois do teste, mantemos essa referência mesmo se outra regra simples se destacar. Analisar montantes identifica o que está em jogo; não é necessário inventar o custo de aquisição ou margem de um produto.

#### Passo a passo: construir uma comparação justa
1. Separe as transações por dia relativo.
2. Calcule a capacidade de cada dia com arredondamento para cima.
3. Ordene cada política usando somente informação permitida.
4. Selecione exatamente essa quantidade, inclusive quando os scores forem baixos.
5. Só depois consulte rótulos e calcule quantidades e montantes.

A ordem é decisiva: usar o rótulo para desempatar seria vazamento. `source_row` fornece um desempate determinístico independente do rótulo.

Em 28 dias, a capacidade de 2% resulta em 333 análises, acima de `0,02 × 15.915 = 318,3` porque arredondamos separadamente cada dia. Não apresentamos 333 como 2% exatos do total.

**Por que maiores valores é uma referência forte?** Ela já coloca dinheiro no centro da seleção. Superá-la permite atribuir parte do resultado à informação de risco, além da informação de valor.

### Etapa 14: O que é observado e o que é assumido
**Observado no dataset:** valor da transação, rótulo, fila selecionada e soma do valor rotulado revisado. Não observamos o efeito de investigar uma transação que não teria sido investigada na operação real.

**Hipóteses centrais:** custo de US$ 2 por investigação, eficácia de 80% sobre o valor fraudulento identificado e penalidade adicional zero por revisão legítima. “Eficácia” agrega a possibilidade de evitar ou recuperar uma parte da exposição. Não é uma taxa medida nessa base.

Para cada política:

`benefício líquido simulado = eficácia × valor fraudulento identificado − custo × análises − penalidade × revisões legítimas`.

`perda total simulada = valor fraudulento total − benefício líquido simulado`.

A diferença entre política e referência mede benefício incremental. As duas têm o mesmo número de análises, logo custos fixos por análise se cancelam na diferença quando não há penalidade adicional. O resultado não inclui implantação, manutenção, atrasos, qualidade da investigação ou efeito sobre clientes.

#### Passo a passo: refazer a conta que sustenta o trabalho
No teste, a exposição fraudulenta rotulada total é US$ 78.851,255. A fila principal identifica US$ 35.111,123; a regra de maiores valores identifica US$ 14.670. Ambas usam 333 análises.

Com eficácia de 80% e custo de US$ 2 por análise:

- Modelo: `0,8 × 35.111,123 − 2 × 333 = US$ 27.422,8984` de benefício líquido simulado.
- Referência: `0,8 × 14.670 − 2 × 333 = US$ 11.070`.
- Contribuição incremental: `27.422,8984 − 11.070 = US$ 16.352,8984`.
- Perda simulada da referência: `78.851,255 − 11.070 = US$ 67.781,255`.
- Redução relativa dessa perda: `16.352,8984 / 67.781,255 ≈ 24,13%`.

O denominador de 24,13% é a perda simulada da referência. Não é o valor total de todas as transações, não é o percentual de fraudes encontradas e não é retorno sobre investimento de implantação.

**Resposta pronta:** “Na amostra de teste, com a mesma capacidade, nosso ranking identificou mais valor de fraude. Sob eficácia de 80% e custo de dois dólares por análise, isso equivale a cerca de 16,35 mil dólares adicionais e 24,13% menos perda que a regra de maiores valores.”

### Etapa 15: Capacidade, custos e eficácia
Testamos capacidades de 1%, 2%, 5% e 10% por dia. Maior capacidade pode capturar mais fraude, mas exige mais trabalho e pode aumentar falsos positivos. A capacidade principal permanece 2%, definida antes do teste.

Cenários: central; eficácia reduzida a 50%; custo de US$ 10 por investigação; e penalidade ilustrativa adicional de US$ 10 por transação legítima revisada. Não escolhemos o cenário mais favorável para apresentar como principal. Esses custos não são parâmetros fornecidos pela Vesta.

Comparar apenas com nenhuma análise produziria uma impressão exagerada da contribuição de ML. Exibimos também quanto as regras simples já conseguiriam identificar.

#### Passo a passo: o que faz o ganho mudar?
Com a mesma quantidade de análises e sem penalidade adicional, o custo unitário se cancela na diferença entre políticas. Aumentar esse custo reduz o benefício absoluto de ambas, mas não muda o benefício incremental em dólares. A redução percentual pode mudar porque o denominador muda.

A eficácia multiplica a diferença de valor capturado. Se for zero, não existe benefício monetário da captura neste modelo. Custos adicionais de implantação consumiriam parte do ganho: o estudo não os mediu.

Uma penalidade para revisão legítima não se cancela quando as filas têm quantidades diferentes de legítimas. Essa hipótese representa atrito ou trabalho adicional e precisa ser apresentada como cenário.

**Não anualize automaticamente:** os 28 dias não provam estabilidade por um ano, nem a amostra representa o volume completo de uma empresa. Cenários servem para entender dependência das hipóteses, não para escolher a história mais favorável.

### Etapa 16: Incerteza, estabilidade e verificação
O bootstrap pareado reamostra blocos circulares de sete dias com todas as transações de cada dia juntas. São cinco mil réplicas. Isso preserva parte da dependência temporal, mas 28 dias fornecem poucos blocos independentes. O intervalo é exploratório e não substitui avaliação em outros períodos ou um piloto causal.

As verificações exigem separação de dias, ausência do rótulo nas entradas, identidade da exposição, previsões finitas e igualdade exata dos orçamentos por política e dia. Uma verificação embaralha o rótulo depois dos scores e confirma que as decisões não mudam: a política seleciona sem conhecer a verdade do teste.

#### Passo a passo: entender o intervalo de incerteza
A unidade de reamostragem é um bloco de dias, não uma transação independente. Reamostrar transações isoladas ignoraria choques e dependência temporal compartilhados.

**Pareado** significa que, em cada réplica, modelo e referência recebem os mesmos dias. Calculamos a diferença nas duas políticas dentro da mesma réplica. Isso evita comparar períodos distintos por acidente.

O intervalo exploratório principal é aproximadamente US$ 11,87 mil a US$ 21,33 mil. Ele resume a variação da diferença no procedimento de reamostragem, sob os custos e a eficácia escolhidos. Não é uma garantia de que 95% dos ganhos futuros estarão aí, nem incorpora automaticamente erros nas hipóteses econômicas.

Com apenas quatro semanas de teste, a diversidade temporal é limitada. Um intervalo inteiramente positivo reforça a evidência nesse recorte, sem provar efeito causal.

**Contra logística:** o ganho adicional do campeão é cerca de US$ 4.785,62, ou 8,51% de redução da perda simulada da logística. Esse diagnóstico posterior mostra que um modelo simples já entrega parte importante do resultado; não redefine o campeão.

### Diagnóstico adicional contra um modelo simples de risco
A referência principal continua sendo a regra escolhida antes do teste. Para não atribuir todo o benefício a uma arquitetura complexa, também mostramos todos os classificadores sob o mesmo orçamento. Uma regressão logística simples já identifica valor relevante; a contribuição adicional do campeão deve ser avaliada contra ela. Este diagnóstico não muda o campeão depois de olhar o teste.

### Etapa 17: Limitações e ética
O espelho e as features anonimizadas limitam a auditoria de como cada atributo foi calculado. A partição temporal não garante independência por cliente. O orçamento se refere à amostra sistemática, e o teste cobre apenas 28 dias. O custo e a eficácia de investigação não são observados. Uma investigação pode ocorrer tarde demais para impedir uma perda, e o rótulo histórico pode refletir processos operacionais existentes.

O projeto não autoriza bloqueio automático de cartões. Transações legítimas revisadas podem causar atrito e tratamento desigual. Não tentamos reidentificar pessoas. Dados públicos e anonimizados não substituem uma análise de finalidade, proteção de dados, LGPD e governança numa implantação real. Não declaramos conformidade jurídica a partir deste estudo.

A classificação e a regressão reformulam o mesmo risco. Clusters são exploratórios. Não atribuímos economia a segmentação ou explicações sem avaliar uma ação. O benefício simulado deve ser descontado de implantação e manutenção antes de discutir retorno de investimento.

#### Passo a passo: responder limitações sem desvalorizar o estudo
Use a sequência **limite → consequência → próxima verificação**. Exemplo: “Temos apenas 28 dias de teste; isso limita a estabilidade temporal; repetiríamos em outros períodos antes de implantação”.

Outros exemplos: atributos mascarados limitam a tradução causal; custos assumidos exigem sensibilidade; falta de identificador confiável impede validar clientes inéditos; rótulos históricos podem refletir o processo de confirmação de fraude.

O caráter acadêmico permite estudar essas decisões com hipóteses explícitas. Uma boa defesa sabe delimitar a evidência, sem transformar cada limitação em uma afirmação de que o modelo não serve.

### Etapa 18: Insights e decisão de implantação
A análise deve separar três coisas: reconhecer padrões de fraude, ordenar casos pelo valor em risco e transformar a fila em uma intervenção eficaz. Um classificador com bom F1 pode não maximizar o valor capturado. Revisar somente os maiores valores já é um baseline relevante.

Uma vantagem grande no teste é uma razão para investigar um piloto, não prova de lucro futuro. O piloto precisaria medir capacidade, tempo de resposta, eficácia, custo, atrito de clientes e estabilidade temporal. Os resultados abaixo são calculados dos arquivos, sem números escolhidos para produzir uma narrativa favorável.

#### Passo a passo: interpretar o conjunto, não apenas a melhor tabela
Ao apresentar os resultados, mantenha quatro perguntas: o modelo prevê melhor? a fila seleciona melhor? a diferença tem relevância financeira sob as hipóteses? o desenho permite sustentar essa conclusão?

Não compare diretamente R² da regressão, AP da classificação e silhouette do agrupamento. Medem tarefas diferentes. O vínculo entre as frentes é o problema de negócio e a análise dos dados, não uma escala única de desempenho.

**Frase central:** “O estudo mostra como converter uma previsão de risco em uma política de priorização e medir sua contribuição incremental em condições comparáveis.”

## Perguntas do professor


### Base e problema
**O que é a base?** Transações reais de comércio eletrônico disponibilizadas por Vesta e IEEE-CIS, com rótulos históricos de fraude. Baixamos um espelho OpenML documentado e preservamos a origem.

**Por que não usar o arquivo direto do Kaggle?** O espelho é público e permite reproduzir o download. A fonte original e os direitos continuam os da competição; o arquivo não se torna de domínio público.

**Uma linha é um cliente?** Não, é uma transação. Não possuímos uma chave confiável que identifique clientes de forma completa.

**O que significa cada V ou C?** Muitas definições são ocultadas pelo provedor. Podemos explicar a família geral e o comportamento estatístico, mas não inventar uma interpretação específica.

**Por que 456 campos no espelho?** Há atributos de identidade com variantes de nomes. Lemos uma lista predefinida e auditamos o esquema recebido, sem assumir identidade perfeita com todas as versões da competição.

**Por que uma em cada cinco linhas?** Para limitar processamento sem selecionar pelo rótulo ou por resultado futuro. A amostra é sistemática e não representa automaticamente todo o fluxo de produção.

**Por que só 30 mil linhas para treinar?** É um orçamento comum a todos os algoritmos que permite comparação reproduzível. O teste usa todas as linhas de seu bloco da amostra. Mais dados é uma extensão possível, sem promessa de melhora.

**Por que não retirar valores altos?** O valor é parte do risco econômico. Apagar montantes extremos só por serem extremos poderia esconder o problema real.

### Metodologia
**Por que separar por tempo?** O uso real recebe transações futuras. Dividir aleatoriamente poderia misturar padrões posteriores no treino.

**O teste tem clientes inéditos?** Não sabemos. A avaliação mede um fluxo posterior; não comprova generalização para novos clientes.

**Onde poderia haver vazamento?** Em rótulos ou valores derivados entrando em X, agregações futuras, transformações ajustadas fora do treino e escolha retrospectiva de políticas. A origem de features ocultas também limita a auditoria.

**Por que TransactionDT não entra diretamente?** É um deslocamento temporal com origem civil desconhecida e pode incentivar extrapolações frágeis. Usamos o tempo para separar blocos e extraímos um ciclo horário, sem afirmar hora local.

**Por que o valor entra no modelo?** Ele está disponível na transação. Não revela por si só se a operação é fraude.

**A regressão não é uma classificação disfarçada?** Ela é outra formulação do mesmo risco: estima uma média monetária em vez de uma probabilidade. Não a apresentamos como problema independente ou prejuízo líquido observado.

**Por que não usar SMOTE?** Preservamos a prevalência nos dados e exploramos métricas e ranking. Amostragem sintética exigiria ocorrer apenas dentro do treino e poderia distorcer probabilidades sem correção.

**Como foram escolhidos hiperparâmetros?** Pequenas grades em três folds temporais no treino. A escolha é documentada e não é busca exaustiva.

**O que faz a calibração Platt?** Ajusta uma transformação logística do score bruto com rótulos de um bloco separado, buscando probabilidades mais consistentes. Não garante calibração futura ou por subgrupo.

### Métricas e algoritmos
**Por que não destacar acurácia?** A classe legítima domina. Um modelo que nunca detecta fraude pode ter acurácia alta e ser inútil para a decisão.

**Qual é a diferença entre precisão e recall?** Precisão mede quantas revisões selecionadas eram fraude; recall mede quantas fraudes existentes foram selecionadas.

**O que é AP?** Average precision, um resumo da curva precisão–recall. Não é percentual de fraude nem a integral trapezoidal da curva.

**Por que o limiar F1 não é usado na fila econômica?** O limiar decide uma classe; a fila precisa respeitar capacidade e priorizar valor. São objetivos distintos.

**Por que multiplicar probabilidade por valor?** Isso estima exposição esperada, se a probabilidade for adequada e o valor representar o que está em risco. A eficácia da investigação vem depois.

**Por que um modelo com maior F1 pode identificar menos dinheiro?** Ele pode reconhecer muitas fraudes pequenas e perder poucas operações de alto valor.

**Por que R² pode ser baixo?** A exposição tem muitos zeros e eventos monetários extremos. Estimar a média exata é difícil. Avaliamos ranking e decisão separadamente, sem esconder o R².

**Por que um baseline zero pode ter bom MAE?** Porque a mediana de um alvo com mais de metade de zeros é zero. Isso não o torna útil para ordenar exposição positiva.

**Qual é a diferença entre parâmetro e hiperparâmetro?** Parâmetro é aprendido no ajuste; hiperparâmetro configura o algoritmo antes do ajuste, como profundidade ou regularização.

**Por que one-hot e escala?** Códigos não têm uma ordem numérica natural, e escalas distintas podem dominar distâncias e regularização.

**O que é regularização?** Penalização de complexidade para reduzir ajustes frágeis. L1 pode zerar coeficientes; L2 os contrai; ElasticNet combina as duas.

**Por que permutação não mostra causa?** Embaralhar mede dependência preditiva no modelo. Atributos correlacionados e fatores não observados impedem interpretação causal direta.

### Agrupamento e PCA
**Os clusters são tipos de fraude?** Não. Foram construídos sem rótulo. A taxa de fraude posterior só descreve cada grupo histórico.

**O que é ruído no DBSCAN?** Ponto sem densidade suficiente segundo eps e min_samples, não necessariamente dado errado ou fraude.

**Silhouette mais alta prova melhor grupo?** Não. Pode excluir muitos pontos ou representar grupos pouco úteis. É preciso avaliar cobertura, tamanho e interpretação.

**PCA melhora automaticamente a previsão?** Não. Aqui é ferramenta de exploração e visualização, não uma etapa obrigatória do classificador.

### Dinheiro e conclusão
**Quanto foi realmente economizado?** Não observamos economia realizada. Medimos valor fraudulento rotulado identificado e calculamos benefício sob eficácia e custos assumidos. As cifras concretas estão na seção 14.

**O valor de uma fraude é igual à perda da empresa?** Não necessariamente. Pode haver recuperação, responsabilidade compartilhada, tarifas e outros mecanismos não observados.

**Por que custo de dois dólares e eficácia de 80%?** São hipóteses ilustrativas declaradas antes do teste, não dados da Vesta. Outros cenários mostram sensibilidade.

**A referência é não investigar ninguém?** Essa é uma referência secundária. A principal é a melhor regra simples na validação, com o mesmo orçamento diário de análises.

**Maior benefício significa que devemos implantar?** Não sozinho. Precisamos validar eficácia, atraso, custo, estabilidade, atrito e despesas de implantação com um piloto.

**Revisar significa bloquear?** Não. A política representa uma fila de investigação. Bloqueio automático exigiria outro desenho operacional e avaliação de consequências.

**Como sabemos que o teste não escolheu a referência?** A referência foi avaliada e congelada no bloco de validação; o arquivo baseline_selection registra seus resultados.

**Por que comparar os dois projetos sem comparar dólares absolutos?** Os recortes, escalas, períodos e premissas são diferentes. Comparamos evidência incremental, incerteza e adequação acadêmica.

**Fraude resolve a fragilidade econômica do M5?** Pode fornecer uma vantagem mais clara na triagem, mas ainda depende de eficácia da ação. A decisão deve seguir os resultados e não uma promessa anterior.

## Ensaio e demonstração em dupla

**Sugestão de divisão para ensaiar:** João apresenta slides 1–4 (5min20s). Vitor apresenta 5–7 (4min55s). João apresenta 8 (2min20s). Vitor apresenta 9–10 (2min25s). É uma sugestão, não uma divisão obrigatória. Ambos devem dominar o projeto inteiro.

1. Cada integrante explica em voz alta origem, split, campeão, fila e conta financeira sem consultar o texto.
2. O outro faz as perguntas da seção anterior e pede a evidência no notebook.
3. Ensaiem com cronômetro. Cortem detalhes da fala, mantendo-os no roteiro para perguntas.
4. Antes da apresentação, abram o notebook e executem o modo de leitura. Confiram kernel, caminhos e dependências.
5. Durante a demonstração, mostrem leitura, preparação, split e a célula didática da seção 20. O treinamento completo fica fora da fala. A seção 24.4 reconcilia o resultado com o CSV.
6. Se a célula didática demorar além do tempo ensaiado, mostrem as saídas executadas e expliquem as operações. Não atribuam ao exemplo pequeno o resultado do campeão completo.

### Frases que precisam sair corretas

- “Uma linha é uma transação, não um cliente.”
- “Extra Trees foi escolhido pela captura monetária na validação.”
- “O teste mede o protocolo congelado.”
- “O ranking principal usa probabilidade calibrada vezes valor, com a mesma capacidade diária.”
- “24,13% é redução da perda simulada da regra de maiores valores.”
- “O valor identificado é medido na avaliação, e o benefício depende das hipóteses.”
- “Um resultado melhor no teste sugere investigação futura, sem troca retrospectiva do campeão.”

### Antes da submissão

Conferir os nomes João Pedro Castro e Vitor Neves em PPT e relatório, adequar a identificação dos arquivos e conferir a data no sistema da instituição. O professor pede PPT com até 10 slides, DOC com até 10 páginas, base e código. Esta documentação não substitui a submissão pelo sistema da disciplina.

## Fontes e rastreabilidade

- [Competição IEEE-CIS / Vesta no Kaggle](https://www.kaggle.com/competitions/ieee-fraud-detection/data).
- [Espelho OpenML 46858](https://www.openml.org/d/46858).
- [Documentação Empulse](https://empulse.readthedocs.io/en/latest/guide/datasets/ieee_fraud_detection.html).
- `references/template_professor.pptx`: requisitos do trabalho.
- `results/*_metrics.csv`: desempenho por algoritmo e bloco.
- `results/financial_policies.csv`: resultado por política, capacidade e cenário.
- `results/training_diagnostics.json`: comparação posterior entre ajuste e teste.
- `src/experiment.py`: decisões, configurações e cálculos.
- `src/diagnosticos_apresentacao.py`: reprodução do diagnóstico sem nova seleção.

Os arquivos têm origem identificada e hash local. O MD5 do OpenML refere-se ao ARFF, não ao parquet recebido. Não afirmamos licença irrestrita a partir da existência do espelho. O repositório permanece privado.
