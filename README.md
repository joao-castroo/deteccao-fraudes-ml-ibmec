# Projeto Fraude — IEEE-CIS

Projeto separado do M5, criado em `ProjML/Projeto_Fraude`. O projeto anterior permanece na raiz de ProjML. A comparação está em `ProjML/Comparacao`.

## Repositório privado

Este repositório contém o projeto de fraude, separado do M5. A base bruta é obtida pelo script de download e não integra o Git. A amostra processada e os resultados estão incluídos para facilitar a execução do notebook. A comparação com o M5 pertence ao pacote local e não é necessária para executar este projeto.

## Comece aqui

1. `deliverables/notebook_leitura.html`: versão autônoma do notebook, com navegação, tabelas e figuras incorporadas.
2. `notebooks/01_projeto_fraude_completo.ipynb`: notebook executado, com 25 seções numeradas (0–24), 81 células, explicações passo a passo e cinco exercícios didáticos adicionais.
3. `deliverables/guia_defesa.html`: perguntas respondidas e glossário.
4. `deliverables/apresentacao_Fraude.pptx`: dez slides com notas de fala.
5. `deliverables/relatorio_Fraude.docx`: relatório de oito páginas.

Antes da submissão, preencher os nomes completos dos autores nos materiais e adequar os nomes de arquivo à exigência do professor. A data e o prazo devem ser conferidos no sistema da instituição. Nada foi publicado ou submetido.

## Resultado principal

Com as mesmas 333 revisões diárias acumuladas no teste de 28 dias, a fila principal identifica US$ 35.111,12 em valor rotulado de fraude, contra US$ 14.670,00 da regra de maiores transações. A diferença de valor identificado é observável neste recorte, mas não equivale a valor evitado ou recuperado.

Com eficácia assumida de 80% e custo de US$ 2 por revisão, o benefício incremental simulado é US$ 16.352,90, com intervalo exploratório de US$ 11.865,42 a US$ 21.326,99. A redução de perda simulada da referência é 24,13%. O mesmo tipo de resultado no M5 foi 0,87%, mas as tarefas e premissas são diferentes.

Contra uma regressão logística simples, a vantagem adicional do campeão é US$ 4.785,62 (8,51% de redução da perda simulada da logística). Essa avaliação é um diagnóstico adicional e não substitui a referência principal escolhida antes do teste. Outros modelos tiveram algumas métricas melhores no teste; não trocamos o campeão retrospectivamente.

## Escopo e hipóteses

- Origem: IEEE-CIS/Vesta, competição Kaggle; espelho OpenML 46858.
- Original recebido: 590.540 transações, 20.663 fraudes, 456 campos no parquet.
- Amostra sistemática: uma em cada cinco linhas; removidos dias extremos, sem seleção por rótulo ou valor.
- Amostra final: 116.533 transações, 4.046 fraudes e 71 atributos de entrada predefinidos.
- Treino dias relativos 1–107; validação 108–134; calibração 135–152; teste 153–180.
- Cada ajuste recebe no máximo 30 mil linhas do bloco autorizado; todos os estimadores usam a mesma semente e orçamento.
- Regressores estimam `TransactionAmt*isFraud`, uma exposição derivada; não são perdas líquidas observadas.
- Fila principal: probabilidade calibrada × valor, com teto de 2% por dia. O arredondamento diário gera 333 revisões, ligeiramente acima de 2% no agregado.
- Revisar não é bloquear. Eficácia, atraso e custo da investigação não foram observados.
- Dezenove técnicas: sete classificadores, oito regressores, três agrupamentos e PCA, além de baselines.

## Execução

A execução foi verificada em Python 3.9.6. Dependências fixadas em `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/download_data.py
python src/experiment.py
```

O script completo reproduz preparação, seleção, previsões, políticas, agrupamentos, figuras, diagnósticos adicionais e 125 verificações. O notebook carrega os resultados por padrão; `REEXECUTAR=True` repete o experimento. Depois, salve o notebook no Jupyter/VS Code para preservar saídas atualizadas.

Abra o notebook na pasta Projeto_Fraude ou notebooks. O detector de raiz procura os metadados OpenML, evitando confundir este projeto com o M5. A demonstração em sala não exige internet nem repetir a busca inteira.

A dependência pyarrow foi instalada localmente em work no ambiente de construção, sem modificar o Python do sistema. No seu ambiente virtual, basta instalar requirements. A pasta work não integra o pacote de entrega. Avisos numéricos do ambiente foram preservados nos logs; previsões não finitas não foram aceitas.

## Estrutura

- `data/raw/ieee_cis.parquet`: arquivo recebido, sem alteração.
- `data/processed`: recorte e metadados de decisão.
- `src/experiment.py`: pipeline comentado completo.
- `src/additional_analysis.py`: comparação adicional com logística, sem mudar a seleção.
- `src/download_data.py`: download reprodutível do espelho.
- `results`: métricas, parâmetros, previsões, políticas, cenários, bootstrap, hashes e verificações.
- `references`: metadados de origem e template do professor.
- `notebooks` e `deliverables`: materiais de estudo e apresentação.

## Limitações que precisam aparecer na defesa

O teste tem 28 dias. Há poucos blocos temporais independentes. Não há uma chave completa de cliente para impedir repetição por pessoa entre períodos. Muitas features são anônimas e sua construção original não é completamente auditável. Os resultados são do recorte, não de toda a empresa. Não existe experimento contrafactual de investigação nem demonstração de lucro realizado. A regressão reformula o mesmo risco em moeda, não uma tarefa independente. Clusters são descritivos e não recebem ganho econômico sem uma ação avaliada.

## Fontes e direitos

- https://www.kaggle.com/competitions/ieee-fraud-detection/data
- https://www.openml.org/d/46858
- https://data.openml.org/datasets/0004/46858/dataset_46858.pq
- https://empulse.readthedocs.io/en/latest/guide/datasets/ieee_fraud_detection.html

O hash SHA-256 local está em results/provenance.json. O MD5 OpenML se refere ao ARFF; não foi comparado ao parquet. O uso segue as regras da competição. Espelho público não equivale a licença irrestrita de redistribuição. Os arquivos ficam locais e no pacote solicitado para uso acadêmico.

## Apresentação ampliada de 15 minutos

- `deliverables/apresentacao_Fraude_completa_15min.pptx`: 16 slides principais com 15 minutos planejados, incluindo demonstração, e 10 slides de apoio para perguntas. As notas contêm fala sugerida, perguntas e fontes.
- `deliverables/roteiro_apresentacao_15min.html`: roteiro de estudo com cronograma e respostas.
- O template do professor limita a submissão a 10 slides. A versão `apresentacao_Fraude.pptx`, com 10 slides, permanece preservada. A versão ampliada atende ao pedido de ensaio e exposição detalhada.
- `src/diagnosticos_apresentacao.py`: refaz os dois campeões congelados, confirma as previsões de teste e compara ajuste com teste. Trata-se de diagnóstico posterior, sem alterar seleção ou política.
- Extra Trees: AP no ajuste 0,895 e no teste 0,379. Random Forest regressor: RMSE no ajuste US$ 30,54 e no teste US$ 39,96. O ajuste é otimista e a diferença não isola sobreajuste de mudança temporal.
