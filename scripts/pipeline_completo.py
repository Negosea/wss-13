#!/usr/bin/env python3
"""Pipeline completo de análise de plantas"""

import subprocess
import json
import sys
from pathlib import Path

def executar_pipeline(arquivo_planta):
    """Executa o pipeline completo de análise"""
    
    print(f"🚀 Iniciando análise de: {arquivo_planta}")
    print("="*50)
    
    # 1. Executar analisador
    print("\n📸 Etapa 1: Analisando planta...")
    subprocess.run([sys.executable, "scripts/analisador_plantas.py", arquivo_planta])
    
    # 2. Corrigir formato
    print("\n�� Etapa 2: Ajustando formato...")
    subprocess.run([sys.executable, "scripts/corrige_formato_json.py"])
    
    # 3. Calcular áreas
    print("\n📐 Etapa 3: Calculando áreas...")
    subprocess.run([sys.executable, "scripts/calcula_area_total.py"])
    
    # 4. Exibir resumo
    print("\n📊 RESUMO FINAL:")
    print("-"*50)
    
    with open('plantas_teste/resultado_analisador_com_area.json', 'r') as f:
        dados = json.load(f)
        
    print(f"Projeto: {dados['projeto']['nome']}")
    print(f"Data: {dados['projeto']['data']}")
    print(f"Responsável: {dados['projeto']['responsavel']}")
    print(f"\nÁrea Total: {dados['geometria']['area_total']:.2f} m²")
    print("\nDetalhamento por ambiente:")
    
    for medida in dados['geometria']['medidas']:
        area = medida['largura'] * medida['comprimento']
        print(f"  • {medida['ambiente']:.<20} {area:>6.2f} m²")
    
    print("\n✅ Análise concluída com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        executar_pipeline(sys.argv[1])
    else:
        # Usar arquivo padrão se não especificado
        executar_pipeline("plantas_teste/planta_construcode_pagina1.png")
