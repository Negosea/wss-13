# ~/projetos/framework-construcao/integrar_dashboard.py
import os
import shutil
import json

def integrar_projetos():
    # Paths
    dashboard_path = os.path.expanduser("~/Downloads/construction_dashboard")
    framework_path = os.path.expanduser("~/projetos/framework-construcao")
    
    # 1. Copiar dashboard
    dashboard_dest = os.path.join(framework_path, "dashboard")
    if not os.path.exists(dashboard_dest):
        shutil.copytree(dashboard_path, dashboard_dest)
        print("✅ Dashboard copiado")
    
    # 2. Modificar data_processor.py para usar seus dados
    processor_path = os.path.join(dashboard_dest, "data_processor.py")
    
    # Adicionar imports do seu framework
    with open(processor_path, 'r') as f:
        content = f.read()
    
    # Inserir imports no início
    new_imports = """
import sys
sys.path.append('..')
from scripts.ocr_plantas import processar_planta
from scripts.parser_memorial import extrair_dados_memorial
from src.parser_planta_arquitetonica import analisar_planta
"""
    
    content = new_imports + content
    
    with open(processor_path, 'w') as f:
        f.write(content)
    
    print("✅ Data processor modificado")
    
    # 3. Criar arquivo de configuração unificada
    config = {
        "dados_path": "../dados",
        "plantas_path": "../dados/plantas_baixadas",
        "memoriais_path": "../dados/memoriais",
        "saidas_path": "../dados/saidas_split"
    }
    
    with open(os.path.join(dashboard_dest, "config.json"), 'w') as f:
        json.dump(config, f, indent=4)
    
    print("✅ Configuração criada")

if __name__ == "__main__":
    integrar_projetos()