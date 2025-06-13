#!/usr/bin/env python3
"""
Baixa vários PDFs de plantas via links ConstruCode em lote.
Salva relatórios simples de sucesso/falha e imprime debug do conteúdo recebido.
"""

import requests
from pathlib import Path
from datetime import datetime

def baixar_planta_construcode(url, destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    resultado = {
        'url': url,
        'status': None,
        'arquivo': '',
        'erro': ''
    }
    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
        ## DEBUG: Exibir cabeçalho da resposta
        print(f"-> Resposta HTTP: {response.status_code} | Tipo de conteúdo: {response.headers.get('Content-Type','desconhecido')}")
        if response.status_code == 200 and b'%PDF' in response.content[:1024]:
            # Extrai idProjeto e idObra da url para nomear
            import re
            id_proj = re.search(r'idProjeto=(\d+)', url)
            id_obra = re.search(r'idObra=(\d+)', url)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"planta_idProjeto{id_proj.group(1) if id_proj else 'X'}_idObra{id_obra.group(1) if id_obra else 'X'}_{timestamp}.pdf"
            filepath = destino / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            resultado['status'] = "OK"
            resultado['arquivo'] = str(filepath)
        else:
            # Mostra o início do conteúdo recebido
            print("-" * 40)
            print("INÍCIO DO CONTEÚDO RECEBIDO (debug):")
            try:
                print(response.content[:800].decode('utf8'))
            except Exception:
                print(response.content[:800])
            print("FIM DO CONTEÚDO RECEBIDO (debug)")
            print("-" * 40)
            resultado['status'] = "FALHA"
            resultado['erro'] = f"HTTP {response.status_code} ou conteúdo não é PDF"
    except Exception as e:
        resultado['status'] = "ERRO"
        resultado['erro'] = str(e)
    return resultado

def processar_lote(links, destino):
    relatorio = []
    for url in links:
        print(f"\nBaixando: {url}")
        resultado = baixar_planta_construcode(url, destino)
        if resultado['status'] == "OK":
            print(f"✔️ Sucesso: {resultado['arquivo']}")
        else:
            print(f"❌ Falha: {resultado['erro']}")
        relatorio.append(resultado)
    return relatorio

if __name__ == "__main__":
    # Lista de links (adicione quantos quiser)
    lista_links = [
        "https://www.construcode.com.br/Track/PlantasMob?idProjeto=37589&idObra=2221&tp=007",
        "https://www.construcode.com.br/Track/Planta/?m=xgoVn%2f7JbbU%3d&o=cc&area=37589&tp=301",
        # etc.
    ]
    destino = "/home/sea/projetos/framework-construcao/dados/temp/"
    relatorio = processar_lote(lista_links, destino)

    print("\nRELÁTORIO GERAL:")
    for r in relatorio:
        print(f"- URL: {r['url']}\n  Status: {r['status']}\n  Arquivo: {r['arquivo']}\n  Erro: {r['erro']}\n")

# ==========================================
#