"""Prepara arquivos identificados para o Sala de Aula, sem realizar submissão.

Executar da raiz após baixar os dados: python src/prepare_submission.py
Extraia os ZIPs de base e código no mesmo diretório para reconstruir Projeto_Fraude.
"""
from pathlib import Path
import shutil,zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entrega_sala'
PREFIX='Joao_Pedro_Castro_Vitor_Neves'

def run():
    raw=ROOT/'data/raw/ieee_cis.parquet'
    if not raw.exists():raise FileNotFoundError('Primeiro execute python src/download_data.py para incluir a base original na entrega.')
    OUT.mkdir(exist_ok=True)
    for source,suffix in [('apresentacao_Fraude.pptx','Apresentacao.pptx'),('relatorio_Fraude.docx','Relatorio.docx')]:
        shutil.copy2(ROOT/'deliverables'/source,OUT/f'{PREFIX}_{suffix}')
    for suffix,folders,files in [
        ('Base_de_Dados.zip',['data/raw','data/processed'],[]),
        ('Codigo_e_Notebook.zip',['src','notebooks','results','references','docs'],['README.md','requirements.txt'])]:
        target=OUT/f'{PREFIX}_{suffix}'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            paths=[p for folder in folders for p in (ROOT/folder).rglob('*')]+[ROOT/f for f in files]
            for p in paths:
                if p.is_file() and '__pycache__' not in p.parts and p.name!='.DS_Store':z.write(p,'Projeto_Fraude/'+str(p.relative_to(ROOT)))
        with zipfile.ZipFile(target) as z:assert z.testzip() is None
    readme='''Arquivos de João Pedro Castro e Vitor Neves para submissão acadêmica.
1. Apresentação: os mesmos dez slides para entrega e fala.
2. Relatório: nove páginas, dentro do limite de dez.
3. Base_de_Dados.zip: arquivo original e amostra processada.
4. Codigo_e_Notebook.zip: código, notebook executado, resultados e documentação.
Extraia os dois ZIPs no mesmo diretório para reconstruir Projeto_Fraude. Instale requirements.txt e abra notebooks/01_projeto_fraude_completo.ipynb. O notebook lê os resultados por padrão.
O roteiro extenso em Word fica na pasta deliverables do pacote completo de estudo e no GitHub. Ele é material de preparação, separado do relatório acadêmico.
Conferir no sistema a data da apresentação. O template determina entrega até 23h59 do dia anterior. Nenhuma submissão é realizada por este script.
'''
    (OUT/f'{PREFIX}_LEIA_ME.txt').write_text(readme)
    manifest={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.suffix!='.json'}
    (OUT/f'{PREFIX}_Manifesto.json').write_text(json.dumps(manifest,indent=2))
    print('Arquivos identificados preparados em',OUT)

if __name__=='__main__':run()
