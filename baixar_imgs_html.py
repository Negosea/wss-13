import os
import requests
from bs4 import BeautifulSoup

# Caminho do HTML salvo localmente (ajuste se necessário)
CAMINHO_HTML = "/home/sea/Área de Trabalho/Nova guia_files/ConstruCode - Simplifique a rotina de quem constrói.html"

# Pasta destino das imagens
PASTA_DESTINO = "/home/sea/projetos/framework-construcao/dados/tiles_salvos_html"
os.makedirs(PASTA_DESTINO, exist_ok=True)

# Lê o HTML local
with open(CAMINHO_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# Faz o parse do HTML
soup = BeautifulSoup(html, "html.parser")

# Busca todos os <img>
imagens = soup.find_all("img")
print(f"Total de imagens encontradas: {len(imagens)}")

baixadas = 0

for i, img in enumerate(imagens, start=1):
    src = img.get("src")
    if not src or src.startswith("file"):
        # Imagens armazenadas como file:// ou relativas ao PC são ignoradas
        continue
    nome_arquivo = os.path.basename(src).split("?")[0]  # Evita query string no nome
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
