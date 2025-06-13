import os
import requests
from bs4 import BeautifulSoup

CAMINHO_HTML = "/home/sea/Área de Trabalho/Nova guia_files/ConstruCode - Simplifique a rotina de quem constrói.html"
PASTA_DESTINO = "/home/sea/projetos/framework-construcao/dados/tiles_salvos_html"
os.makedirs(PASTA_DESTINO, exist_ok=True)

def ler_html_seguro(caminho):
    # Tenta latin-1 com ignore
    try:
        with open(caminho, "r", encoding="latin-1", errors="ignore") as f:
            return f.read()
    except Exception:
        pass
    # Tenta utf-8 com ignore
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        pass
    # Modo binário e decode manual como último recurso
    with open(caminho, "rb") as f:
        return f.read().decode("latin-1", errors="ignore")

# Lê o HTML local
html = ler_html_seguro(CAMINHO_HTML)

# Faz o parse do HTML
soup = BeautifulSoup(html, "html.parser")

# Busca todos os <img>
imagens = soup.find_all("img")
print(f"Total de imagens encontradas: {len(imagens)}")

baixadas = 0

import urllib.parse

for i, img in enumerate(imagens, start=1):
    src = img.get("src")
    if not src or src.startswith("file"):
        continue
    # Se o src for relativo, tente obter o base href do HTML ou ignore
    if not urllib.parse.urlparse(src).scheme:
        # Tenta obter <base href="..."> se existir
        base_tag = soup.find("base", href=True)
        if base_tag:
            src = urllib.parse.urljoin(base_tag["href"], src)
        else:
            print(f"  ⚠️ Ignorado (src relativo sem base): {src}")
            continue
    # Só baixa se for http ou https
    if not src.startswith("http"):
        print(f"  ⚠️ Ignorado (src não http): {src}")
        continue
    nome_arquivo = os.path.basename(src).split("?")[0]
    nome_arquivo = f"tile_{i:03d}_" + nome_arquivo
    destino = os.path.join(PASTA_DESTINO, nome_arquivo)
    try:
        print(f"Baixando: {src} -> {destino}")
        resp = requests.get(src, timeout=30)
        if resp.status_code == 200:
            with open(destino, "wb") as fimg:
                fimg.write(resp.content)
            baixadas += 1
            print(f"  ✅ Salvo: {destino}")
        else:
            print(f"  ⚠️ Não baixado (status {resp.status_code})")
    except Exception as e:
        print(f"  ❌ Erro: {e}")

print(f"\nDownload concluído: {baixadas} imagens salvas em '{PASTA_DESTINO}'")