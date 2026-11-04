# Conferência do template do professor e da preparação para a defesa

**Autores: João Pedro Castro e Vitor Neves.**

O conjunto de materiais cobre os temas acadêmicos solicitados no template enviado, no relato do ex-aluno e nas orientações da dupla. A conferência cruzou o texto dos dez slides do template com slides, relatório, células do notebook, código e resultados. O relato do ex-aluno foi tratado como orientação de preparação, não como uma nova rubrica oficial.

A apresentação tem dez slides e plano de 900 segundos, incluindo demonstração. O relatório tem nove páginas. O roteiro de estudo tem trinta páginas e é separado do relatório limitado a dez páginas. A fala precisa ser ensaiada pela dupla; o cronograma planejado não certifica o tempo real de apresentação.

## Template do professor

| Tema do template | Evidência no trabalho | Resultado da conferência |
|---|---|---|
| Capa e autoria completa | Slide 1; capa do relatório e roteiro | Coberto. João Pedro Castro e Vitor Neves identificados |
| Problema, contexto, objetivo, decisão e valor esperado | Slide 2; notebook 1, 13–15; relatório 1 e 6 | Coberto. Priorização de uma fila de revisão com capacidade fixa |
| Aplicabilidade, vantagens e limitações de ML | Slides 2, 4 e 9; notebook 7, 17–18 | Coberto. Hipóteses distintas, limites de dados, custos, interpretação e implantação |
| Origem, licença, período, registros e unidade de análise | Slide 3 e suas notas; notebook 2–3; relatório 2; metadados e proveniência | Coberto com limite explícito. Campo licence do OpenML: Kaggle and IEEE CIS; não interpretado como licença aberta. Tempo é relativo, não data civil |
| Faltantes, duplicatas, extremos, codificação, escala e engenharia | Slide 3 e notas; notebook 4–5; audit.json e missing_features.csv | Coberto. Medianas e indicadores, one-hot, escala, ciclo horário, presença de informação; zero duplicatas no critério auditado, sem apagar extremos automaticamente |
| Treino/teste, proporções, semente e prevenção de vazamento | Slides 3–4; notebook 6; experiment.py | Coberto. Blocos temporais por dias inteiros, semente 42, transformações aprendidas dentro dos folds |
| Validação cruzada e hiperparâmetros | Slide 4 e notas; notebook 6–7; classification_cv.csv e regression_cv.csv | Coberto e executado. Três folds temporais, busca pequena, AP na classificação e MSE na regressão |
| Aproximadamente 15 técnicas nas três frentes | Slide 4; notebook 7; relatório 8; QUADRO_SINTESE.md | Coberto como 15 aplicações: seis regressões, cinco classificações, três agrupamentos e PCA. HistGB conta por tarefa; PCA é redução |
| Regressão: alvo contínuo, modelos, referências, parâmetros e métricas | Slide 5; notebook 11; relatório 4; regression_metrics.csv e regression_baselines.csv | Coberto. Seis regressores; MAE, MSE, RMSE e R²; exposição derivada explicitamente identificada |
| Regressão: ajuste versus teste, sobreajuste, importância e resíduos | Slide 5 e notas; notebook 11; training_diagnostics.json; regression_permutation_importance.csv e figuras | Coberto. Diagnóstico reproduz previsões congeladas. Importância por aumento de RMSE na calibração, com três repetições |
| Classificação: classes, desbalanceamento, métricas, matriz, curva e limiar | Slide 6; notebook 8–10; relatório 3 | Coberto. Acurácia, precisão, recall, F1, ROC-AUC, AP e Brier; matriz e precisão–recall; limiar validado separado da fila financeira |
| Custo de falsos positivos e negativos | Slides 8–9 e notas; notebook 9, 14–15; financial_policies.csv | Coberto por cenários. Custo de revisão, exposição não capturada, eficácia e penalidade ilustrativa por revisão legítima |
| Agrupamento: K-means, DBSCAN, hierárquico, k/eps, escala e distância | Slide 7; notebook 12; relatório 5; clustering_metrics.csv | Coberto. Grades, silhouette, Davies–Bouldin, tamanho dos grupos, ruído e estabilidade |
| PCA: componentes, variância, pesos e perfis | Slide 7; notebook 12; pca_variance.csv, pca_coefficients.csv e cluster_profiles.csv | Coberto. Duas componentes na projeção, variância acumulada e loadings. Sem usar fraude para formar grupos |
| Quadro síntese: configuração, métrica, vantagem e limite das técnicas | Relatório 8; notebook 7; QUADRO_SINTESE.md e techniques_summary.csv | Coberto em quadro completo. Nos slides, inventário e critérios ficam no 4, resultados nos 5–7 e valor de negócio no 8. O slide 4 indica a página do quadro completo |
| Principal achado e valor prático | Slides 8–9; notebook 13–18; relatório 6 e 9 | Coberto. Maior valor rotulado identificado com 333 revisões e benefício incremental condicionado às hipóteses |
| Ética, viés, privacidade, explicabilidade, LGPD e impactos | Slide 9 e notas; notebook 17; relatório 7 | Coberto como discussão. Não alegamos conformidade jurídica ou equidade comprovada; não há auditoria quantitativa de grupos protegidos |
| Conclusão, limitações e próximos passos | Slide 9; notebook 17–18; relatório 7 e 9 | Coberto. Outros períodos, eficácia real, custos completos, monitoramento e piloto |
| Demonstração: leitura, tratamento, split, treino, teste e métricas | Slide 10; notebook 20 e 24; código executado | Coberto. Pipeline didático de logística, métricas e fila. Não apresentado como reprodução do vencedor completo |
| PPT até 10 slides e DOC até 10 páginas | Dez slides; relatório de nove páginas; renders conferidos | Atendido. O roteiro extenso é material de estudo adicional, não o DOC limitado |
| Base e código, identificação da dupla nos arquivos | prepare_submission.py; pasta entrega_sala | Preparação automatizada com nomes completos em ASCII nos arquivos de apresentação, relatório, base e código/notebook |
| Entrega no Sala de Aula e prazo | Regra preservada no roteiro e no LEIA_ME da submissão | Ação externa pendente. Conferir a data no sistema e enviar até 23h59 do dia anterior. Nenhuma submissão foi realizada |

## Pontos relatados pelo ex-aluno

| Orientação | Como está atendida |
|---|---|
| Descrever de onde veio a base e o que cada linha significa | Origem IEEE-CIS/Vesta no Kaggle, acesso por espelho OpenML, 590.540 linhas originais e 116.533 na amostra; transação, não pessoa |
| Pegar a base e treinar vários modelos | Onze aplicações supervisionadas realmente ajustadas, com resultados salvos; quatro técnicas exploratórias adicionais |
| Comparar modelos e métricas de performance | Tabelas por bloco e tarefa, referências simples, matriz, curvas e erros. Não comparamos índices de tarefas distintas como se fossem iguais |
| Justificar o vencedor e por que os outros não foram escolhidos | Captura monetária na validação para classificação e MSE de validação na regressão; ranking completo, parâmetros e hipóteses dos concorrentes |
| Fazer validação cruzada para escolher hiperparâmetros | Três folds temporais. KNN: k=15 com AP média 0,2355, k=45 com 0,2674; escolhemos 45. Justificamos por que KFold aleatório misturaria passado e futuro |
| Limitações das técnicas | Quadro completo das 15 aplicações e explicações individuais no roteiro: linearidade, correlação, independência, distância, escala, complexidade e cobertura de ruído |
| Questões éticas e descrição dos dados | Anonimização, rótulo histórico, efeito sobre legítimos, privacidade, governança e ausência de comprovação de equidade |
| Benefícios, custos e valor financeiro | Comparação com regras e logística, mesmo orçamento diário, cenários de custo/eficácia, benefício incremental e intervalo exploratório |
| Dominar os termos e explicar treinamento | Roteiro de trinta páginas com 54 termos, explicações de cada método, perguntas e respostas, divisão de ensaio e notebook passo a passo |

## Pedidos específicos da dupla

- Trabalho de fraude separado do M5, mantendo comparação sem misturar unidades ou premissas.
- Pergunta de negócio explícita e valor incremental mensurável sob hipóteses.
- Conteúdo do curso: Ridge e Lasso preservados, HistGradientBoosting em regressão e classificação. A revisão deixa de usar Extra Trees e ElasticNet e inclui LDA.
- Notebook executado, com explicações, exemplos e cálculos reconciliados com os arquivos de resultados.
- Mesmos dez slides para apresentação e entrega, com notas de fala e plano de quinze minutos.
- Roteiro separado, aprofundado, disponível em Word, HTML e no GitHub privado.
- Autoria de João Pedro Castro e Vitor Neves e instruções de acesso e uso no VS Code.

## Ajustes realizados nesta conferência

1. A tabela dos slides passou a mostrar os seis regressores, preservando a referência zero.
2. Acurácia ficou explícita nas tabelas de classificação dos slides e do relatório.
3. Incluímos quadro completo das quinze aplicações, com configuração, métrica, ponto forte e limitação, na página 8 do relatório e no notebook.
4. Acrescentamos importância por permutação do regressor na calibração, gráfico observado–previsto, resíduos e diagnóstico ajuste–teste ao notebook.
5. A demonstração didática passou a mostrar métricas de classificação além da fila e da conta econômica.
6. Registramos literalmente a informação de licença do cadastro e o limite da discussão de equidade.
7. Preparamos o script que gera arquivos com os nomes da dupla para submissão.

## Limites que permanecem e precisam ser defendidos

**Resultado financeiro:** US$ 38.044,57 é valor rotulado identificado. O incremento de US$ 18.699,66 e a redução de 27,59% da perda da referência são simulações sob 80% de eficácia e US$ 2 por revisão. Não medimos dinheiro efetivamente recuperado.

**Regressão:** exposure = TransactionAmt × isFraud é um alvo contínuo derivado do mesmo risco da classificação. Não representa uma segunda base ou um fenômeno independente. É uma formulação monetária pedagogicamente útil, explicitamente explicada.

**Validação:** o período de teste já foi consultado na versão anterior. Esta revisão curricular é retrospectiva, não uma nova confirmação em holdout inédito. O conjunto e os critérios atuais não foram ajustados para maximizar esse teste.

**Interpretação:** atributos anônimos restringem semântica e auditoria da sua construção original. Agrupamentos não provam tipos de fraudadores. Importância preditiva não demonstra causa.

**Entrega administrativa e defesa oral:** faltam a confirmação da data no sistema, o envio dos arquivos pela dupla e um ensaio cronometrado real. Esses itens não são substituídos por código, roteiro ou verificações automáticas.
