#!/usr/bin/env python3


import os
from bs4 import BeautifulSoup
import re

def analyze_planta_html():
    # Encontrar o arquivo HTML mais recente
    html_files = [f for f in os.listdir('data/raw_plantas') if f.endswith('_debug.html')]
    if not html_files:
        print("❌ Nenhum arquivo HTML de debug encontrado!")
        return
    
    latest_html = sorted(html_files)[-1]
    html_path = os.path.join('data/raw_plantas', latest_html)
    
    print(f"📄 Analisando: {latest_html}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    print("\n🔍 Procurando elementos que podem conter a planta:\n")
    
    # 1. Procurar por divs com IDs ou classes relacionadas a planta
    planta_keywords = ['planta', 'plant', 'floor', 'map', 'blueprint', 'canvas', 
                       'drawing', 'diagram', 'layout', 'viewer', 'render']
    
    found_elements = []
    
    # Buscar por IDs
    for element in soup.find_all(id=True):
        element_id = element.get('id', '').lower()
        if any(keyword in element_id for keyword in planta_keywords):
            found_elements.append(('ID', element_id, element.name))
    
    # Buscar por classes
    for element in soup.find_all(class_=True):
        classes = ' '.join(element.get('class', [])).lower()
        if any(keyword in classes for keyword in planta_keywords):
            found_elements.append(('CLASS', classes, element.name))
    
    # Buscar por data attributes
    for element in soup.find_all():
        for attr, value in element.attrs.items():
            if attr.startswith('data-') and isinstance(value, str):
                if any(keyword in value.lower() for keyword in planta_keywords):
                    found_elements.append(('DATA', f"{attr}={value}", element.name))
    
    # Mostrar resultados
    if found_elements:
        print("✅ Elementos potenciais encontrados:")
        for tipo, valor, tag in set(found_elements):
            print(f"   - {tipo}: <{tag}> com '{valor}'")
    else:
        print("⚠️ Nenhum elemento óbvio de planta encontrado")
    
    # 2. Procurar por iframes
    iframes = soup.find_all('iframe')
    if iframes:
        print(f"\n📦 {len(iframes)} iframe(s) encontrado(s):")
        for i, iframe in enumerate(iframes):
            src = iframe.get('src', 'sem src')
            print(f"   - iframe {i+1}: {src}")
    
    # 3. Procurar por scripts que podem gerar a planta
    scripts = soup.find_all('script')
    planta_scripts = []
    for script in scripts:
        if script.string and any(keyword in script.string.lower() for keyword in planta_keywords):
            planta_scripts.append(script)
    
    if planta_scripts:
        print(f"\n📜 {len(planta_scripts)} script(s) relacionado(s) à planta encontrado(s)")
    
    # 4. Procurar por elementos com background-image
    style_elements = soup.find_all(style=True)
    bg_images = []
    for element in style_elements:
        style = element.get('style', '')
        if 'background-image' in style or 'background:' in style:
            bg_images.append((element.name, element.get('id', 'sem-id'), style[:100]))
    
    if bg_images:
        print(f"\n🖼️ {len(bg_images)} elemento(s) com background-image:")
        for tag, elem_id, style in bg_images[:5]:  # Mostrar apenas os 5 primeiros
            print(f"   - <{tag}> id='{elem_id}': {style}...")
    
    # 5. Salvar um resumo estruturado
    print("\n📊 Estrutura principal da página:")
    main_containers = soup.find_all(['main', 'section', 'article', 'div'], class_=True)[:10]
    for container in main_containers:
        classes = ' '.join(container.get('class', []))
        elem_id = container.get('id', '')
        if classes or elem_id:
            print(f"   - <{container.name}> id='{elem_id}' class='{classes}'")

if __name__ == "__main__":
    analyze_planta_html()