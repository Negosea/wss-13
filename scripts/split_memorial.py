#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from unidecode import unidecode

# Caminho atualizado do arquivo de entrada (ajuste caso use 'dados' ou 'data')
ARQUIVO_ENTRADA = os.path.join(os.path.dirname(__file__), '../dados/memorial_estrutural.txt')

def split_sections(text):
    padrao = re.compile(r'\n?(\d{1,3}\.\s*[A-Z][^\n]+)\n', re.UNICODE)
    blocos = padrao.split(text)
    resultado = {}
    if blocos[0].strip():
        resultado['INTRO'] = blocos[0].strip()
    for i in range(1, len(blocos), 2):
        titulo = blocos[i].strip()
        corpo = blocos[i + 1].strip() if (i + 1) < len(blocos) else ""
        resultado[titulo] = corpo
    return resultado

def gerar_tag(titulo, idx):
    # Limita para NO MÁXIMO 8 palavras e remove caracteres perigosos
    palavras = unidecode(titulo.lower()).replace('.', '').replace('-', ' ').split()
    tag_curta = "_".join(palavras[:8])
    return f"{idx:02d}_{tag_curta}"

def main():
    with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f:
        texto = f.read()

    blocos = split_sections(texto)

    DIR_SAIDA = os.path.join(os.path.dirname(__file__), '../dados/saidas_split')
    os.makedirs(DIR_SAIDA, exist_ok=True)
    for idx, (tag, conteudo) in enumerate(blocos.items(), start=1):
        tag_arquivo = gerar_tag(tag, idx)
        arq_saida = os.path.join(DIR_SAIDA, f'{tag_arquivo}.txt')
        with open(arq_saida, 'w', encoding='utf-8') as fout:
            fout.write(conteudo)
        print(f'[OK] Seção salva: {arq_saida}')

    print(f'\nTotal de seções extraídas: {len(blocos)} (veja em dados/saidas_split/)')

if __name__ == "__main__":
    main()