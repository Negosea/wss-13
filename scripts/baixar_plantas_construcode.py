import requests
from pathlib import Path

# Parâmetros ajuste conforme sua planta:
LINK_BASE = "https://eu2.contabostorage.com/21ee0bc011104d38817cb2e2e95a3bbe:s3files/S_8940_O_2221_638096366993048374_C_1-{}.png"
PASTA_SAIDA = "plantas_teste"
QTDE_PAGINAS_MAX = 10  # Troque para o número máximo de páginas estimado

Path(PASTA_SAIDA).mkdir(exist_ok=True)

for i in range(QTDE_PAGINAS_MAX):
    url = LINK_BASE.format(i)
    arquivo_saida = f"{PASTA_SAIDA}/planta_construcode_pagina{i+1}.png"
    print(f"[{i+1}] Baixando: {url}")
    resp = requests.get(url)
    if resp.status_code == 200 and resp.content and len(resp.content) > 10000:
        with open(arquivo_saida, "wb") as out:
            out.write(resp.content)
        print(f"   ✔️ Salvo em: {arquivo_saida}")
    else:
        print(f"   🚩 Página {i+1} não existe ou terminou o lote. Parando.")
        break

print("\nDownload completo!")