#!/usr/bin/env python3
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

def preprocessar_imagem(caminho_imagem):
    """Pré-processa imagem para melhorar OCR"""
    # Ler imagem
    img = cv2.imread(caminho_imagem)
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar threshold para binarizar
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Remover ruído
    denoised = cv2.medianBlur(thresh, 3)
    
    # Salvar imagem processada
    processed_path = caminho_imagem.replace('.png', '_processed.png')
    cv2.imwrite(processed_path, denoised)
    
    return processed_path

def extrair_texto_planta(caminho_imagem):
    """Extrai texto da planta usando OCR"""
    print(f"🔍 Processando: {caminho_imagem}")
    
    # Pré-processar imagem
    img_processada = preprocessar_imagem(caminho_imagem)
    
    # Configurar Tesseract para português
    custom_config = r'--oem 3 --psm 11 -l por'
    
    # Extrair texto
    texto = pytesseract.image_to_string(Image.open(img_processada), config=custom_config)
    
    # Salvar resultado
    output_path = 'dados/pipeline_output/planta_principal_ocr.txt'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    print(f"✅ Texto extraído salvo em: {output_path}")
    print(f"📊 Total de caracteres: {len(texto)}")
    print(f"📝 Primeiras linhas:")
    print("-" * 50)
    print(texto[:500])
    
    return texto

if __name__ == "__main__":
    imagem = "dados/plantas_baixadas/planta_principal.png"
    if os.path.exists(imagem):
        extrair_texto_planta(imagem)
    else:
        print(f"❌ Arquivo não encontrado: {imagem}")
