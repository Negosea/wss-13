#!/usr/bin/env python3
# verificar_gemma.py

import os
from pathlib import Path
import json

def verificar_instalacao():
    """Verifica se o Gemma foi baixado corretamente"""
    
    modelo_path = Path("models/gemma-2b")
    
    print("🔍 Verificando instalação do Gemma-2B...\n")
    
    # Arquivos necessários
    arquivos_necessarios = [
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "model.safetensors"  # ou pytorch_model.bin
    ]
    
    arquivos_encontrados = []
    arquivos_faltando = []
    
    for arquivo in arquivos_necessarios:
        caminho = modelo_path / arquivo
        if caminho.exists():
            tamanho = caminho.stat().st_size / (1024**2)  # MB
            arquivos_encontrados.append(f"✅ {arquivo} ({tamanho:.1f} MB)")
        else:
            # Verificar alternativas
            if arquivo == "model.safetensors":
                alt_path = modelo_path / "pytorch_model.bin"
                if alt_path.exists():
                    tamanho = alt_path.stat().st_size / (1024**2)
                    arquivos_encontrados.append(f"✅ pytorch_model.bin ({tamanho:.1f} MB)")
                    continue
            arquivos_faltando.append(f"❌ {arquivo}")
    
    # Mostrar resultados
    print("📁 Arquivos encontrados:")
    for arquivo in arquivos_encontrados:
        print(f"  {arquivo}")
    
    if arquivos_faltando:
        print("\n⚠️  Arquivos faltando:")
        for arquivo in arquivos_faltando:
            print(f"  {arquivo}")
        return False
    
    # Verificar config
    try:
        with open(modelo_path / "config.json", 'r') as f:
            config = json.load(f)
            print(f"\n📊 Modelo: {config.get('model_type', 'Unknown')}")
            print(f"📏 Parâmetros: {config.get('num_parameters', 'Unknown')}")
    except:
        pass
    
    print("\n✅ Gemma-2B está pronto para uso!")
    return True

if __name__ == "__main__":
    if verificar_instalacao():
        print("\n🚀 Próximo passo: python src/analise/gemma/gemma_integration.py")
    else:
        print("\n❌ Complete o download antes de continuar")