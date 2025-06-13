#!/usr/bin/env python3
"""
Extrator de Plantas do ConstruCode
Extrai informações de plantas de arquivos HTML salvos localmente
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import chardet  # Para detectar encoding

class ExtratorPlantasConstruCode:
    def __init__(self, arquivo_html):
        self.arquivo_html = arquivo_html
        self.plantas = []
        
    def detectar_encoding(self):
        """Detecta o encoding do arquivo HTML"""
        with open(self.arquivo_html, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    def extrair_plantas(self):
        """Extrai informações das plantas do HTML"""
        # Detectar encoding
        encoding = self.detectar_encoding()
        print(f"🔍 Encoding detectado: {encoding}")
        
        # Ler arquivo com encoding correto
        with open(self.arquivo_html, 'r', encoding=encoding) as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar todos os tiles (elementos <a> com classe "tile")
        tiles = soup.find_all('a', class_='tile')
        
        for tile in tiles:
            planta_info = self.extrair_info_tile(tile)
            if planta_info:
                self.plantas.append(planta_info)
        
        return self.plantas
    
    def extrair_info_tile(self, tile):
        """Extrai informações de um tile específico"""
        try:
            # Extrair href
            href = tile.get('href', '')
            
            # Extrair ID da planta do href
            id_match = re.search(r'/planta/(\d+)', href)
            planta_id = id_match.group(1) if id_match else None
            
            # Buscar imagem dentro do tile
            img = tile.find('img')
            if img:
                url_imagem = img.get('src', '')
                nome_planta = img.get('alt', '').strip()
            else:
                url_imagem = ''
                nome_planta = ''
            
            # Se não encontrou nome no alt, tentar no texto
            if not nome_planta:
                nome_planta = tile.get_text(strip=True)
            
            # Construir URL completa da planta
            url_planta = f"https://app.construcode.com.br{href}" if href else ""
            
            # Garantir que a URL da imagem seja completa
            if url_imagem and not url_imagem.startswith('http'):
                if url_imagem.startswith('//'):
                    url_imagem = f"https:{url_imagem}"
                elif url_imagem.startswith('/'):
                    url_imagem = f"https://app.construcode.com.br{url_imagem}"
            
            return {
                'id': planta_id,
                'nome': nome_planta,
                'url_planta': url_planta,
                'url_imagem': url_imagem,
                'href_original': href
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar tile: {e}")
            return None
    
    def criar_scripts_download(self, diretorio_saida):
        """Cria scripts para download das imagens"""
        # Criar diretório se não existir
        Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
        
        # Script wget
        script_wget = os.path.join(diretorio_saida, 'download_plantas_wget.sh')
        with open(script_wget, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n\n")
            f.write("# Script para download de plantas usando wget\n")
            f.write("# Gerado em: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write("# Criar diretório para as imagens\n")
            f.write("mkdir -p plantas_imagens\n\n")
            
            for planta in self.plantas:
                if planta['url_imagem']:
                    nome_arquivo = f"planta_{planta['id']}_{planta['nome'].replace(' ', '_').replace('/', '_')}.jpg"
                    f.write(f"echo 'Baixando: {planta['nome']}...'\n")
                    f.write(f"wget -O 'plantas_imagens/{nome_arquivo}' '{planta['url_imagem']}'\n\n")
        
        # Script curl
        script_curl = os.path.join(diretorio_saida, 'download_plantas_curl.sh')
        with open(script_curl, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n\n")
            f.write("# Script para download de plantas usando curl\n")
            f.write("# Gerado em: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write("# Criar diretório para as imagens\n")
            f.write("mkdir -p plantas_imagens\n\n")
            
            for planta in self.plantas:
                if planta['url_imagem']:
                    nome_arquivo = f"planta_{planta['id']}_{planta['nome'].replace(' ', '_').replace('/', '_')}.jpg"
                    f.write(f"echo 'Baixando: {planta['nome']}...'\n")
                    f.write(f"curl -o 'plantas_imagens/{nome_arquivo}' '{planta['url_imagem']}'\n\n")
        
        # Tornar scripts executáveis
        os.chmod(script_wget, 0o755)
        os.chmod(script_curl, 0o755)
        
        # Salvar JSON com informações
        json_file = os.path.join(diretorio_saida, 'plantas_info.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.plantas, f, ensure_ascii=False, indent=2)
        
        print(f"\n📝 Scripts de download criados em {diretorio_saida}/")
        print(f"   - {os.path.basename(script_wget)}")
        print(f"   - {os.path.basename(script_curl)}")
        print(f"   - {os.path.basename(json_file)}")

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python extrator_plantas_construcode.py <arquivo_html>")
        sys.exit(1)
    
    arquivo_html = sys.argv[1]
    
    if not os.path.exists(arquivo_html):
        print(f"❌ Erro: Arquivo '{arquivo_html}' não encontrado!")
        sys.exit(1)
    
    print(f"📄 Lendo arquivo: {arquivo_html}")
    
    extrator = ExtratorPlantasConstruCode(arquivo_html)
    plantas = extrator.extrair_plantas()
    
    print(f"🔍 Encontrados {len(plantas)} tiles de plantas")
    
    if plantas:
        # Mostrar preview
        print("\n📋 Preview das primeiras 3 plantas:")
        for i, planta in enumerate(plantas[:3]):
            print(f"\n{i+1}. {planta['nome']}")
            print(f"   ID: {planta['id']}")
            print