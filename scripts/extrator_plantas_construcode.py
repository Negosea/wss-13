#!/usr/bin/env python3
"""
extrator_plantas_construcode.py
Extrai todos os links de plantas do HTML do ConstruCode
"""

import re
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
from datetime import datetime
import os

class ExtratorPlantasConstruCode:
    def __init__(self, arquivo_html):
        self.arquivo_html = arquivo_html
        self.base_url = "https://www.construcode.com.br"
        self.plantas = []
        
    def extrair_plantas(self):
        """Extrai todas as plantas do HTML"""
        print(f"🔍 Analisando arquivo: {self.arquivo_html}")
        
        with open(self.arquivo_html, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Encontrar todos os cards de plantas
        cards = soup.find_all('div', class_='card')
        
        for idx, card in enumerate(cards, 1):
            try:
                # Extrair onclick
                onclick = card.get('onclick', '')
                match = re.search(r"window\.location='(/Track/Planta/\?m=([^&]+)&o=cc&area=(\d+)&tp=)'", onclick)
                
                if match:
                    # Dados básicos
                    url_relativa = match.group(1)
                    planta_id = unquote(match.group(2))
                    area_id = match.group(3)
                    
                    # Extrair título e detalhes
                    titulo_elem = card.find('h2', class_='card__title')
                    titulo = titulo_elem.text.strip() if titulo_elem else "Sem título"
                    
                    detalhes_elem = card.find('p', class_='card__text')
                    detalhes = detalhes_elem.text.strip() if detalhes_elem else "Sem detalhes"
                    
                    # Extrair revisão
                    revisao_match = re.search(r'Revis[ãa]o:\s*(\d+)', detalhes)
                    revisao = revisao_match.group(1) if revisao_match else "00"
                    
                    # Classificar tipo de planta
                    tipo_planta = self.classificar_tipo(titulo, detalhes)
                    
                    # Gerar nome do arquivo
                    nome_arquivo = self.gerar_nome_arquivo(titulo, revisao, idx)
                    
                    planta_info = {
                        'id': idx,
                        'planta_id': planta_id,
                        'area_id': area_id,
                        'titulo': titulo,
                        'detalhes': detalhes,
                        'revisao': revisao,
                        'tipo': tipo_planta,
                        'url_completa': f"{self.base_url}{url_relativa}",
                        'url_relativa': url_relativa,
                        'nome_arquivo': nome_arquivo
                    }
                    
                    self.plantas.append(planta_info)
                    print(f"✅ [{idx:03d}] {tipo_planta}: {titulo[:60]}...")
                    
            except Exception as e:
                print(f"❌ Erro no card {idx}: {str(e)}")
    
    def classificar_tipo(self, titulo, detalhes):
        """Classifica o tipo de planta baseado no título e detalhes"""
        texto = f"{titulo} {detalhes}".upper()
        
        tipos = {
            'ARQUITETÔNICA': ['ARQUITET', 'PLANTA BAIXA', 'FACHADA', 'CORTE', 'COBERTURA'],
            'ESTRUTURAL': ['ESTRUTUR', 'ESTC', 'ARMAÇÃO', 'PILAR', 'VIGA', 'LAJE', 'FUNDAÇÃO'],
            'ELÉTRICA': ['ELÉTRIC', 'ELET', 'FIAÇÃO', 'QUADRO', 'ILUMINAÇÃO'],
            'HIDRÁULICA': ['HIDRÁULIC', 'HIDR', 'ÁGUA', 'ESGOTO', 'PLUVIAL'],
            'INCÊNDIO': ['INCÊNDIO', 'SPRINKLER', 'ALARME', 'HIDRANTE'],
            'AR_CONDICIONADO': ['AR CONDICIONADO', 'CLIMATIZAÇÃO', 'HVAC'],
            'GÁS': ['GÁS', 'GLP', 'TUBULAÇÃO DE GÁS'],
            'DETALHAMENTO': ['DETALHE', 'DETALHAMENTO', 'AMPLIAÇÃO']
        }
        
        for tipo, palavras in tipos.items():
            if any(palavra in texto for palavra in palavras):
                return tipo
        
        return 'OUTROS'
    
    def gerar_nome_arquivo(self, titulo, revisao, idx):
        """Gera nome padronizado para o arquivo"""
        # Limpar título
        nome_limpo = re.sub(r'[^\w\s-]', '', titulo)
        nome_limpo = re.sub(r'\s+', '_', nome_limpo)
        nome_limpo = nome_limpo[:80]  # Limitar tamanho
        
        return f"{idx:04d}_{nome_limpo}_REV{revisao}.pdf"
    
    def salvar_resultados(self):
        """Salva os resultados em diferentes formatos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Criar diretório de saída
        os.makedirs('extrações', exist_ok=True)
        
        # Salvar JSON completo
        arquivo_json = f'extrações/plantas_construcode_{timestamp}.json'
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(self.plantas, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON salvo: {arquivo_json}")
        
        # Salvar lista de URLs
        arquivo_urls = f'extrações/urls_plantas_{timestamp}.txt'
        with open(arquivo_urls, 'w', encoding='utf-8') as f:
            for planta in self.plantas:
                f.write(f"{planta['url_completa']}\n")
        print(f"🔗 URLs salvas: {arquivo_urls}")
        
        # Salvar script de download
        self.gerar_script_download(timestamp)
        
        # Estatísticas
        self.exibir_estatisticas()
    
    def gerar_script_download(self, timestamp):
        """Gera script bash para download das plantas"""
        arquivo_script = f'extrações/download_plantas_{timestamp}.sh'
        
        with open(arquivo_script, 'w', encoding='utf-8') as f:
            f.write("""#!/bin/bash
# Script de Download de Plantas - ConstruCode
# Gerado em: {}

# Configurações
COOKIE="seu_cookie_aqui"  # Adicione seu cookie de sessão
OUTPUT_DIR="plantas_baixadas"
DELAY=2  # Delay entre downloads (segundos)

# Criar diretórios
mkdir -p "$OUTPUT_DIR"
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            # Organizar por tipo
            for tipo in set(p['tipo'] for p in self.plantas):
                f.write(f'\nmkdir -p "$OUTPUT_DIR/{tipo}"\n')
            
            f.write('\n# Downloads\n')
            for planta in self.plantas:
                f.write(f"""
echo "[{planta['id']:03d}/{len(self.plantas)}] Baixando: {planta['titulo'][:50]}..."
curl -L -o "$OUTPUT_DIR/{planta['tipo']}/{planta['nome_arquivo']}" \
     -H "Cookie: $COOKIE" \
     "{planta['url_completa']}"
sleep $DELAY
""")
        
        os.chmod(arquivo_script, 0o755)
        print(f"📥 Script de download: {arquivo_script}")
    
    def exibir_estatisticas(self):
        """Exibe estatísticas da extração"""
        print("\n📊 ESTATÍSTICAS DA EXTRAÇÃO:")
        print(f"Total de plantas encontradas: {len(self.plantas)}")
        
        # Por tipo
        tipos_count = {}
        for planta in self.plantas:
            tipos_count[planta['tipo']] = tipos_count.get(planta['tipo'], 0) + 1
        
        print("\nPor tipo:")
        for tipo, count in sorted(tipos_count.items()):
            print(f"  - {tipo}: {count} plantas")

# Executar extração
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python extrator_plantas_construcode.py arquivo.html")
        sys.exit(1)
    
    extrator = ExtratorPlantasConstruCode(sys.argv[1])
    extrator.extrair_plantas()
    extrator.salvar_resultados()