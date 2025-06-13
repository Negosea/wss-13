import cv2

CAMINHO = 'dados/plantas_baixadas/planta_construcode.png'
IMG = cv2.imread(CAMINHO, 0)
# 1. Equalizar histograma (melhora contraste)
IMG_EQ = cv2.equalizeHist(IMG)
# 2. Suavizar ruído
IMG_DENOISED = cv2.fastNlMeansDenoising(IMG_EQ, None, 30, 7, 21)
# 3. Binarizar (adaptativo ajuda para papel/planta)
IMG_BIN = cv2.adaptiveThreshold(IMG_DENOISED,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,7)
# 4. Sharpening
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
IMG_SHARP = cv2.filter2D(IMG_BIN, -1, kernel)
# 5. Salvar resultado
cv2.imwrite('dados/plantas_baixadas/planta_construcode_PREPROC.png', IMG_SHARP)
print("Imagem pré-processada salva como: dados/plantas_baixadas/planta_construcode_PREPROC.png")
