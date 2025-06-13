#!/usr/bin/env python3
"""
Automatiza a navegação e captura das N páginas da planta do ConstruCode
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
from datetime import datetime

PLANTA_URL = "https://www.construcode.com.br/Track/Planta/?m=68uTY2frNHg%3d&o=cc&area=37589&tp=114#"
OUTPUT_DIR = "data/raw_plantas"
os.makedirs(OUTPUT_DIR, exist_ok=True)
NUM_PAGINAS = 42  # Ajuste conforme o número real no menu

def capture_all_pages():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        print(f"🌐 Acessando: {PLANTA_URL}")
        driver.get(PLANTA_URL)
        time.sleep(8)  # Ajuste para garantir carregamento inicial

        for pagina in range(NUM_PAGINAS):
            print(f"📄 Capturando página {pagina + 1}/{NUM_PAGINAS}")

            # Aguarda o carregamento do Leaflet/mapa/tela
            time.sleep(2.0)
            nome_base = datetime.now().strftime(f"planta_%Y%m%d_%H%M%S_p{pagina+1:02d}")
            
            # Screenshot geral
            screenshot_path = os.path.join(OUTPUT_DIR, f"{nome_base}_full.png")
            driver.save_screenshot(screenshot_path)

            # Recorta área do mapa
            try:
                container = driver.find_element(By.CSS_SELECTOR, ".leaflet-pane.leaflet-map-pane.leaflet-pan-anim")
                location = container.location
                size = container.size

                with Image.open(screenshot_path) as img:
                    left = int(location['x'])
                    top = int(location['y'])
                    right = int(location['x'] + size['width'])
                    bottom = int(location['y'] + size['height'])
                    cropped = img.crop((left, top, right, bottom))
                    cropped_path = os.path.join(OUTPUT_DIR, f"{nome_base}_crop.png")
                    cropped.save(cropped_path)
                    print(f"✅ Página {pagina + 1}: imagem salva em {cropped_path}")
            except Exception as e:
                print(f"⚠️ Erro ao recortar screenshot da página {pagina + 1}: {e}")

            # Avança para a próxima página, exceto na última iteração
            if pagina < NUM_PAGINAS - 1:
                try:
                    btn_next = driver.find_element(By.ID, "nextpageplanta")
                    driver.execute_script("arguments[0].click();", btn_next)
                except Exception as e:
                    print(f"❌ Não foi possível acessar o botão de próxima página na página {pagina+1}: {e}")
                    break
                # Aqui pode ser útil aguardar até que o DOM indique nova página carregada

        print("🎉 Todas as páginas capturadas!")

    except Exception as e:
        print(f"❌ Erro geral: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_all_pages()