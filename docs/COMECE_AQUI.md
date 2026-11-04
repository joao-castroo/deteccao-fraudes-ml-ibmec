# Comece aqui João e Vitor

Autores: **João Pedro Castro e Vitor Neves**. O repositório é privado. Vitor usa o GitHub **vnevesl**. O convite foi enviado e precisa ser aceito para liberar o acesso. Neste repositório pessoal, o GitHub oferece colaboração com permissão de edição, sem administração do repositório.

## Qual material usar

| Material | Uso |
|---|---|
| [Apresentação oficial](../deliverables/apresentacao_Fraude.pptx) | **Os mesmos 10 slides para apresentação e entrega**, sem apêndice adicional |
| [Roteiro completo em Word](../deliverables/roteiro_completo_apresentacao_e_defesa.docx) | Baixar, editar e enviar o material de estudo |
| [Roteiro completo](ROTEIRO_E_DEFESA.md) | Estudo no próprio GitHub: termos, finalidade, uso, achados, perguntas e tempos |
| [Roteiro em HTML](../deliverables/roteiro_apresentacao_15min.html) | Baixar e abrir no navegador, com navegação e tabelas |
| [Notebook](../notebooks/01_projeto_fraude_completo.ipynb) | Código executado, resultados e exercícios |
| [Notebook em HTML](../deliverables/notebook_leitura.html) | Leitura sem instalar Python: baixar e abrir no navegador |
| [Relatório](../deliverables/relatorio_Fraude.docx) | Texto da entrega, com 9 páginas |
| [Código principal](../src/experiment.py) | Protocolo e 15 técnicas |
| [Diagnóstico de ajuste e teste](../src/diagnosticos_apresentacao.py) | Refaz somente os campeões, sem mudar seleção |
| [Resultados](../results) | Métricas, políticas, parâmetros e verificações |

A versão longa de 26 slides não é a apresentação oficial. Ela foi retirada dos arquivos atuais para manter uma única versão de entrega. O histórico do Git preserva versões anteriores.

## Como acessar pelo VS Code

1. Aceitar o convite do repositório na conta correta do GitHub.
2. No VS Code, abrir a paleta de comandos e executar `Git: Clone`.
3. Colar `https://github.com/joao-castroo/deteccao-fraudes-ml-ibmec.git` e escolher uma pasta.
4. Abrir a pasta clonada. Instalar as extensões Python e Jupyter da Microsoft.
5. Criar o ambiente e instalar dependências no terminal.

Mac ou Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No notebook, selecionar o kernel Python da `.venv`. A amostra processada e os resultados já estão no repositório. Não é preciso baixar a base bruta para estudar ou executar o modo de leitura.

Para atualizar uma cópia existente sem sobrescrever alterações locais:

```bash
git status
git pull --ff-only
```

Se o Git apontar alterações locais, verificar os arquivos antes de continuar. Não usar reset destrutivo para atualizar o trabalho.

## Como reproduzir o estudo completo

Na raiz do repositório, com as dependências instaladas:

```bash
python src/download_data.py
python src/experiment.py
```

O treinamento completo é mais demorado que a demonstração. O notebook usa os resultados salvos por padrão. `REEXECUTAR=True` repete o experimento. A demonstração didática da seção 20 não substitui o campeão do experimento.

Diagnóstico posterior, mantendo parâmetros e campeões:

```bash
python src/diagnosticos_apresentacao.py
```

## Como estudar em dupla

1. Ler o roteiro cronometrado, os termos e a conta financeira.
2. Cada um explicar os mesmos conceitos sem consultar o texto.
3. Um apresentar e o outro fazer as perguntas de defesa.
4. Ensaiar os 15 minutos, já incluindo a demonstração.
5. Conferir nomes, arquivos e prazo no sistema antes de enviar o trabalho.

A conclusão central é **mais valor de fraude identificado com a mesma capacidade**. A economia é simulada com eficácia e custo assumidos. A documentação explica os limites para que a defesa seja consistente.
