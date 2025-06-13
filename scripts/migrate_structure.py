# scripts/migrate_structure.py
import os
import shutil
from pathlib import Path

def reorganize_project():
    """Reorganiza projeto para estrutura profissional"""
    
    # Criar nova estrutura
    dirs = [
        'app/core',
        'app/models',
        'app/api',
        'app/utils',
        'tests/unit',
        'tests/integration',
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Criar __init__.py
        (Path(dir_path) / '__init__.py').touch()
    
    # Mapeamento de arquivos
    file_mapping = {
        # OCR e processamento
        'scripts/melhorar_imagem_ocr.py': 'app/core/ocr_processor.py',
        'scripts/image_processor.py': 'app/utils/image_utils.py',
        
        # Geração de PDFs
        'scripts/gera_relatorio_pdf_completo.py': 'app/core/pdf_generator.py',
        
        # Análise de plantas
        'src/parser_planta_arquitetonica.py': 'app/core/plant_analyzer.py',
        
        # Validação
        'scripts/validador_wsf13.py': 'app/core/validator.py',
        
        # Pipeline principal
        'scripts/pipeline_completo.py': 'app/main.py',
    }
    
    # Mover arquivos
    for old_path, new_path in file_mapping.items():
        if os.path.exists(old_path):
            shutil.copy2(old_path, new_path)
            print(f"✓ Movido: {old_path} → {new_path}")

if __name__ == "__main__":
    reorganize_project()