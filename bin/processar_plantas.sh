#!/usr/bin/env bash
# Script: processar_plantas.sh
# Descrição: Processa plantas baixadas do framework
# Uso: ./processar_plantas.sh [-d diretorio] [-o output]

set -euo pipefail
trap 'echo "❌ Erro na linha $LINENO"; exit 1' ERR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Incluir funções (se existir biblioteca, mantenha. Se não, comente a próxima linha)
# source "$PROJECT_ROOT/lib/funcoes_comuns.sh"

# Valores padrão
INPUT_DIR="$PROJECT_ROOT/plantas_baixadas"
OUTPUT_DIR="$PROJECT_ROOT/plantas_raspadas"

# Função de ajuda
mostrar_ajuda() {
cat << EOF
Uso: $0 [-d diretorio_entrada] [-o diretorio_saida] [-h]
Opções:
  -d DIR    Diretório de entrada (padrão: $INPUT_DIR)
  -o DIR    Diretório de saída (padrão: $OUTPUT_DIR)
  -h        Mostra esta ajuda
EOF
}

# Parse de argumentos
while getopts "d:o:h" opt; do
    case $opt in
        d) INPUT_DIR="$OPTARG" ;;
        o) OUTPUT_DIR="$OPTARG" ;;
        h) mostrar_ajuda; exit 0 ;;
        *) mostrar_ajuda; exit 1 ;;
    esac
done

# Verificar diretórios
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "❌ Erro: Diretório de entrada não existe: $INPUT_DIR"
    exit 1
fi

# Criar diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

# Processamento simulado: percorre todos PDFs do diretório de entrada
echo "🔄 Processando plantas de $INPUT_DIR para $OUTPUT_DIR..."

for arquivo in "$INPUT_DIR"/*.pdf; do
    if [[ -f "$arquivo" ]]; then
        nome_base=$(basename "$arquivo" .pdf)
        echo "  📄 Processando: $nome_base"
        # Exemplo: simulando um processamento
        touch "$OUTPUT_DIR/${nome_base}_processado.txt"
    fi
done

echo "✅ Processamento concluído!"