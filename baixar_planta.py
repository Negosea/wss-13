import requests
import os

url = "https://eu2.contabostorage.com/21ee0bc011104d38817cb2e2e95a3bbe:s3files/S_8940_O_2221_638096366993048374_C_1-0.png"
destino = "/home/sea/projetos/framework-construcao/dados/plantas_baixadas/planta_principal.png"
os.makedirs(os.path.dirname(destino), exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

print(f"Baixando {url}")
resp = requests.get(url, headers=headers, timeout=60)
if resp.status_code == 200:
    with open(destino, "wb") as f:
        f.write(resp.content)
    print(f"✅ Imagem salva em: {destino}")
else:
    print(f"⚠️ Erro ao baixar! Status code: {resp.status_code}")