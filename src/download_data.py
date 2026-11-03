"""Baixa o espelho público documentado, sem credenciais e sem alterar arquivo existente."""
from pathlib import Path
import urllib.request,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
URL='https://data.openml.org/datasets/0004/46858/dataset_46858.pq'
p=ROOT/'data/raw/ieee_cis.parquet';p.parent.mkdir(parents=True,exist_ok=True)
if not p.exists():
    temp=p.with_suffix('.download')
    with urllib.request.urlopen(URL,timeout=180) as response,temp.open('wb') as f:
        for chunk in iter(lambda:response.read(1024*1024),b''):f.write(chunk)
    temp.rename(p)
sha=hashlib.sha256(p.read_bytes()).hexdigest()
manifest=ROOT/'results/provenance.json'
if manifest.exists():
    expected=json.loads(manifest.read_text())['sha256']
    assert sha==expected,'O arquivo difere da versão usada neste estudo. Não sobrescreva resultados sem investigar.'
print(p.name,p.stat().st_size,'bytes',sha)
