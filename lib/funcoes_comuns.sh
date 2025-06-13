#!/usr/bin/env bash
# Biblioteca de funções comuns

# Função para logging
log() {
    local nivel="$1"
    local mensagem="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$nivel] $mensagem"
}

# Verificar se diretório existe
verificar_diretorio() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        log "ERRO" "Diretório não encontrado: $dir"
        return 1
    fi
    return 0
}

# Criar diretório com verificação
criar_diretorio_seguro() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        log "INFO" "Criando diretório: $dir"
        mkdir -p "$dir"
    else
        log "INFO" "Diretório já existe: $dir"
    fi
}
