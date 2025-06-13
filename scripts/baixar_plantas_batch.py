#!/usr/bin/env python3
"""
Baixa vários PDFs de plantas via links da ConstruCode em lote.
Salva relatórios simples de sucesso/falha.
"""

import requests
from pathlib import Path
from datetime import datetime
import re

def baixar_planta_construcode(url, destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    resultado = {
        "url": url,
        "status": None,
        "arquivo": "",
        "erro": ""
    }
    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
        if response.status_code == 200 and b"%PDF" in response.content[:1024]:
            id_proj = re.search(r"idProjeto=(\d+)", url)
            id_obra = re.search(r"idObra=(\d+)", url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = (
                f"planta_idProjeto{ id_proj.group(1) if id_proj else 'desconhecido' }"
                f"_idObra{ id_obra.group(1) if id_obra else 'desconhecido' }_{timestamp}.pdf"
            )
            filepath = destino / filename
            with open(filepath, "wb") as f:
                f.write(response.content)
            resultado["status"] = "OK"
            resultado["arquivo"] = str(filepath)
        else:
            falha_nome = destino / f"falha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
            with open(falha_nome, "wb") as f:
                f.write(response.content)
            resultado["status"] = "FALHA"
            resultado["erro"] = f"HTTP {response.status_code} ou conteúdo não é PDF"
    except Exception as e:
        resultado["status"] = "ERRO"
        resultado["erro"] = str(e)
    return resultado

def processar_lote(links, destino):
    relatorio = []
    for url in links:
        print(f"\nBaixando: {url}")
        resultado = baixar_planta_construcode(url, destino)
        if resultado["status"] == "OK":
            print(f"✔️ Sucesso: {resultado['arquivo']}")
        else:
            print(f"❌ Falha: {resultado['erro']}")
        relatorio.append(resultado)
    return relatorio

if __name__ == "__main__":
    # Lista de links das plantas
    lista_links = [
        "https://www.construcode.com.br/Track/PlantasMob?idProjeto=37589&idObra=2221&tp=016",
        "https://www.construcode.com.br/Track/PlantasMob?idProjeto=37589&idObra=2221&tp=325",
        # Adicione mais links aqui...
    ]
    destino = Path("/home/sea/projetos/framework-construcao/dados/temp/")
    relatorio = processar_lote(lista_links, destino)

    print("\nRELATÓRIO GERAL:")
    for r in relatorio:
        print(f"- URL: {r['url']}")
        print(f"  Status: {r['status']}")
        print(f"  Arquivo: {r['arquivo']}")
        print(f"  Erro: {r['erro']}\n")