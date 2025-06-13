#!/usr/bin/env python3
# adicionar_tipo_planta.py
from config_loader import ConfigLoader

def adicionar_novo_tipo():
    """Interface para adicionar novo tipo de planta"""
    config = ConfigLoader()
    
    print("🏗️ ADICIONAR NOVO TIPO DE PLANTA")
    print("-" * 40)
    
    # Coleta informações
    tipo_id = input("ID do tipo (ex: 'incendio'): ").lower()
    nome = input("Nome completo: ")
    descricao = input("Descrição: ")
    
    # Palavras-chave
    print("\nPalavras-chave (uma por linha, linha vazia para terminar):")
    palavras_chave = []
    while True:
        palavra = input("  > ")
        if not palavra:
            break
        palavras_chave.append(palavra)
    
    # Normas técnicas
    print("\nNormas técnicas (uma por linha, linha vazia para terminar):")
    normas = []
    while True:
        norma = input("  > ")
        if not norma:
            break
        normas.append(norma)
    
    # Monta configuração
    novo_tipo = {
        "nome": nome,
        "descricao": descricao,
        "palavras_chave": palavras_chave,
        "padroes_regex": {},
        "validacoes": {},
        "normas_tecnicas": normas
    }
    
    # Adiciona e salva
    if config.adicionar_tipo_planta(tipo_id, novo_tipo):
        print(f"\n✅ Tipo '{nome}' adicionado com sucesso!")
    else:
        print("\n❌ Erro ao adicionar tipo.")

if __name__ == "__main__":
    adicionar_novo_tipo()