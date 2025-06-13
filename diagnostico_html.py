#!/usr/bin/env python3
import chardet
from bs4 import BeautifulSoup
import sys

arquivo = sys.argv[1]

# Detectar encoding
with open(arquivo, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

print(f"📊 Encoding detectado: {encoding}")
print(f"📏 Tamanho do arquivo: {len(raw_data)} bytes")

# Ler e analisar
with open(arquivo, 'r', encoding=encoding) as f:
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

# Estatísticas
print(f"\n📈 Estatísticas do HTML:")
print(f"- Total de links <a>: {len(soup.find_all('a'))}")
print(f"- Links com class='tile': {len(soup.find_all('a', class_='tile'))}")
print(f"- Divs com class='tile': {len(soup.find_all('div', class_='tile'))}")
print(f"- Links com '/planta/': {len([a for a in soup.find_all('a', href=True) if '/planta/' in a['href']])}")

# Mostrar primeiros links
print(f"\n🔗 Primeiros 5 links encontrados:")
for i, link in enumerate(soup.find_all('a', href=True)[:5]):
    print(f"{i+1}. href='{link.get('href')}' | class='{link.get('class')}'")

# Buscar estruturas com "planta"
print(f"\n🌱 Elementos com 'planta' no href:")
plantas = soup.find_all('a', href=lambda x: x and 'planta' in x.lower())
for i, p in enumerate(plantas[:3]):
    print(f"{i+1}. {p}")
