#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Pasta onde estão os arquivos splitados
DIR_SAIDA = os.path.join(os.path.dirname(__file__), '../dados/saidas_split')
# Defina o nome do arquivo de saída final
ARQUIVO_MERGE = os.path.join(os.path.dirname(__file__), '../dados/memorial_unificado.txt')

def merge_files():
    arquivos = sorted(
        [arq for arq in os.listdir(DIR_SAIDA) if arq.endswith('.txt')],
        key=lambda x: x  # Ordenação alfanumérica padrão (funciona se seus splits começam por número)
    )
    if not arquivos:
        print('[ERRO] Nenhum arquivo de saída encontrado para juntar.')
        return

    with open(ARQUIVO_MERGE, 'w', encoding='utf-8') as fout:
        for arq in arquivos:
            caminho = os.path.join(DIR_SAIDA, arq)
            fout.write(f'===== {arq} =====\n\n')  # Cabeçalho para separação visual
            with open(caminho, 'r', encoding='utf-8') as fin:
                fout.write(fin.read())
                fout.write('\n\n')

    print(f'[OK] Memorial unificado salvo em: {ARQUIVO_MERGE}')
    print(f'Total de seções incluídas: {len(arquivos)}')

if __name__ == "__main__":
    merge_files()