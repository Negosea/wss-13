import cv2
import numpy as np
from PIL import Image
import os

def processar_imagem_para_ocr(caminho_entrada, caminho_saida):
    print(f"🔍 Processando: {caminho_entrada}")
    
    # Carregar imagem
    img = cv2.imread(caminho_entrada, 0)
    
    # 1. Redimensionar se muito grande (OCR funciona melhor com ~300 DPI)
    altura, largura = img.shape
    if largura > 3000:
        escala = 3000 / largura
        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)
        img = cv2.resize(img, (nova_largura, nova_altura), interpolation=cv2.INTER_CUBIC)
        print(f"�� Redimensionado para: {nova_largura}x{nova_altura}")
    
    # 2. Remover ruído
    img = cv2.medianBlur(img, 3)
    
    # 3. Binarização Otsu (melhor para texto)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 4. Dilatar levemente para conectar caracteres quebrados
    kernel = np.ones((1,1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    # 5. Salvar com DPI correto
    cv2.imwrite(caminho_saida, img)
    
    # Adicionar DPI usando PIL
    img_pil = Image.open(caminho_saida)
    img_pil.save(caminho_saida, dpi=(300, 300))
    
    print(f"✅ Salvo com 300 DPI: {caminho_saida}")
    
    # Estatísticas
    tamanho_mb = os.path.getsize(caminho_saida) / (1024*1024)
    print(f"📊 Tamanho final: {tamanho_mb:.2f} MB")

# Processar
processar_imagem_para_ocr(
    'dados/plantas_baixadas/planta_construcode.png',
    'dados/plantas_baixadas/planta_construcode_OTIMIZADA.png'
)
