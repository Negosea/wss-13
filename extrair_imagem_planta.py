import requests
from bs4 import BeautifulSoup
import re

# URL da página
url_pagina = "https://www.construcode.com.br/Track/Planta/?m=xgoVn%2f7JbbU%3d&o=cc&area=37589&tp=301"

print(f"Acessando página: {url_pagina}")

# Fazer requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
resp = requests.get(url_pagina, headers=headers)

if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Procurar por imagens
    imagens = soup.find_all('img')
    
    print(f"\n✅ Encontradas {len(imagens)} imagens na página:\n")
    
    for i, img in enumerate(imagens):
        src = img.get('src', '')
        if src:
            # Completar URL se for relativa
            if src.startswith('/'):
                src = f"https://www.construcode.com.br{src}"
            elif not src.startswith('http'):
                src = f"https://www.construcode.com.br/Track/Planta/{src}"
                
            print(f"{i+1}. {src}")
            
            # Se parecer ser uma planta (geralmente tem palavras-chave)
            if any(palavra in src.lower() for palavra in ['planta', 'projeto', 'area', '37589']):
                print(f"   👆 Esta parece ser a planta principal!")
    
else:
    print(f"❌ Erro ao acessar página: {resp.status_code}")
