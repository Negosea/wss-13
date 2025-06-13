import cv2
import numpy as np
from PIL import Image
import pytesseract

IMAGEM = "planta_principal.png"

# --- PRÉ-PROCESSAMENTO PARA OCR --- #
# Carregar e converter para tons de cinza
img_cv = cv2.imread(IMAGEM)
if img_cv is None:
    print(f"❌ Não foi possível abrir {IMAGEM}")
    exit(1)
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# Binarização adaptativa (melhora texto claro/escuro)
bin_img = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 15
)
cv2.imwrite("para_ocr.png", bin_img)  # só para visualizar/debug se quiser

# OCR com imagem binarizada
img_pil = Image.fromarray(bin_img)
texto = pytesseract.image_to_string(img_pil, lang="por")
print("\nTexto OCR da planta (imagem binarizada):")
print('='*40)
print(texto)
with open("ocr_resultado.txt", "w", encoding="utf-8") as f:
    f.write(texto)

# --- ANÁLISE VISUAL DE PAREDES E CÔMODOS --- #
# Deteção de bordas
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Deteção de linhas (paredes)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
num_linhas = len(lines) if lines is not None else 0
print(f"Linhas (possíveis paredes): {num_linhas}")

# Deteção de contornos (potenciais cômodos)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
num_contornos = len(contours)
print(f"Contornos (potenciais cômodos): {num_contornos}")

# Desenhar as detecções para visualização
img_draw = img_cv.copy()
if lines is not None:
    for l in lines:
        x1, y1, x2, y2 = l[0]
        cv2.line(img_draw, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.drawContours(img_draw, contours, -1, (0, 255, 0), 2)

# Salvar resultado visual
saida = "planta_destacada.png"
cv2.imwrite(saida, img_draw)
print(f"✅ Imagem destacada salva como {saida}")
