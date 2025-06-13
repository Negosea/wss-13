#!/usr/bin/env python3
"""
Captura focada da planta do ConstruCode (área do Leaflet)
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

PLANTA_URL = "https://www.construcode.com.br/Track/Planta/?m=68uTY2frNHg%3d&o=cc&area=37589&tp=114#"
OUTPUT_DIR = "data/raw_plantas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def screenshot_leaflet_area():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        print(f"🌐 Acessando: {PLANTA_URL}")
        driver.get(PLANTA_URL)
        time.sleep(10)  # tempo maior para o Leaflet renderizar todos os tiles

        # Tenta capturar o container principal do mapa
        container = driver.find_element(By.CSS_SELECTOR, ".leaflet-pane.leaflet-map-pane.leaflet-pan-anim")
        location = container.location
        size = container.size

        # Captura um screenshot geral da janela
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_screenshot = os.path.join(OUTPUT_DIR, f"planta_{ts}_leaflet_full.png")
        driver.save_screenshot(full_screenshot)
        print(f"✅ Screenshot geral salva: {full_screenshot}")

        # Recorta só a área da planta
        from PIL import Image
        img = Image.open(full_screenshot)
        left = int(location['x'])
        top = int(location['y'])
        right = int(location['x'] + size['width'])
        bottom = int(location['y'] + size['height'])
        planta_cropped = img.crop((left, top, right, bottom))
        cropped_file = os.path.join(OUTPUT_DIR, f"planta_{ts}_leaflet_crop.png")
        planta_cropped.save(cropped_file)
        print(f"✅ Screenshot recortada salva: {cropped_file}")

        # Alternativamente, tente também o 'viewport' inteiro, se precisar:
        try:
            viewport = driver.find_element(By.CSS_SELECTOR, ".viewport.leaflet-container")
            loc2 = viewport.location
            size2 = viewport.size
            left2 = int(loc2['x'])
            top2 = int(loc2['y'])
            right2 = int(loc2['x'] + size2['width'])
            bottom2 = int(loc2['y'] + size2['height'])
            cropped_viewport = img.crop((left2, top2, right2, bottom2))
            viewport_file = os.path.join(OUTPUT_DIR, f"planta_{ts}_viewport_crop.png")
            cropped_viewport.save(viewport_file)
            print(f"✅ Screenshot do viewport do mapa salva: {viewport_file}")
        except Exception as e:
            print(f"⚠️ Não foi possível capturar o viewport: {e}")

    except Exception as e:
        print(f"❌ Erro: {e}")

    finally:
        driver.quit()
        print("✅ Processo finalizado.")

if __name__ == "__main__":
    screenshot_leaflet_area()