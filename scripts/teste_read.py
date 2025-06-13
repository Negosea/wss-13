import requests
import os

url = "https://www.construcode.com.br/Track/Planta/Images/xpto123.png"  # <-- COLE aqui a URL real!

destino = "/home/sea/projetos/framework-construcao/dados/plantas_baixadas/planta_principal.png"
os.makedirs(os.path.dirname(destino), exist_ok=True)

print(f"Baixando {url}")
resp = requests.get(url, timeout=60)
if resp.status_code == 200:
    with open(destino, "wb") as f:
        f.write(resp.content)
    print(f"✅ Imagem salva em: {destino}")
else:
    print(f"⚠️ Erro ao baixar! Status code: {resp.status_code}")