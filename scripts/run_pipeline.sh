#!/bin/bash

# ===================================================
# PIPELINE FRAMEWORK CONSTRUÇÃO CIVIL
# Autor: Marcos Sea
# Data: 09/06/2025
# ===================================================

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretórios base
BASE_DIR="$HOME/projetos/framework-construcao"
SCRIPTS_DIR="$BASE_DIR/scripts"
DADOS_DIR="$BASE_DIR/dados"
ENTRADA_DIR="$DADOS_DIR/entrada"
SAIDA_SPLIT_DIR="$DADOS_DIR/saidas_split"
TEMP_DIR="$DADOS_DIR/temp"

# Criar diretórios se não existirem
mkdir -p "$ENTRADA_DIR" "$SAIDA_SPLIT_DIR" "$TEMP_DIR"

# Função para exibir mensagens
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Função para verificar se comando existe
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "Comando '$1' não encontrado. Por favor, instale-o."
        if [ "$1" = "pdftotext" ]; then
            log_info "Instale com: sudo apt-get install poppler-utils"
        fi
        exit 1
    fi
}

# Banner inicial
clear
echo "====================================================="
echo "   FRAMEWORK CONSTRUÇÃO CIVIL - PIPELINE v1.0"
echo "====================================================="
echo ""

# Verificar argumentos
if [ $# -eq 0 ]; then
    log_error "Uso: ./run_pipeline.sh <arquivo.pdf|arquivo.txt>"
    echo ""
    echo "Exemplos:"
    echo "  ./run_pipeline.sh memorial.pdf"
    echo "  ./run_pipeline.sh memorial.txt"
    echo "  ./run_pipeline.sh ~/Downloads/documento.pdf"
    exit 1
fi

INPUT_FILE="$1"

# Verificar se arquivo existe
if [ ! -f "$INPUT_FILE" ]; then
    log_error "Arquivo não encontrado: $INPUT_FILE"
    exit 1
fi

# Detectar tipo de arquivo
FILE_EXT="${INPUT_FILE##*.}"
FILE_EXT_LOWER=$(echo "$FILE_EXT" | tr '[:upper:]' '[:lower:]')
BASENAME=$(basename "$INPUT_FILE" ".$FILE_EXT")

log_info "Processando arquivo: $INPUT_FILE"
log_info "Tipo detectado: .$FILE_EXT_LOWER"

# Definir arquivo de trabalho
WORK_FILE=""

# Processar de acordo com o tipo
case "$FILE_EXT_LOWER" in
    pdf)
        log_info "Convertendo PDF para TXT..."
        check_command pdftotext
        
        WORK_FILE="$TEMP_DIR/${BASENAME}.txt"
        
        # Converter PDF para TXT
        if pdftotext "$INPUT_FILE" "$WORK_FILE"; then
            log_info "Conversão concluída: $WORK_FILE"
            
            # Mostrar preview do conteúdo
            echo ""
            echo "--- Preview do conteúdo (primeiras 5 linhas) ---"
            head -n 5 "$WORK_FILE"
            echo "..."
            echo ""
        else
            log_error "Falha na conversão do PDF"
            exit 1
        fi
        ;;
        
    txt)
        log_info "Arquivo TXT detectado, copiando para área de trabalho..."
        WORK_FILE="$TEMP_DIR/${BASENAME}.txt"
        cp "$INPUT_FILE" "$WORK_FILE"
        ;;
        
    *)
        log_error "Formato não suportado: .$FILE_EXT_LOWER"
        log_info "Formatos aceitos: .pdf, .txt"
        exit 1
        ;;
esac

# Copiar arquivo para entrada do pipeline
log_info "Preparando arquivo para processamento..."
cp "$WORK_FILE" "$ENTRADA_DIR/memorial_descritivo.txt"

# Executar split
echo ""
log_info "Executando SPLIT do memorial..."
cd "$SCRIPTS_DIR"

if python3 split_memorial.py; then
    log_info "Split concluído com sucesso!"
    
    # Contar arquivos gerados
    NUM_SPLITS=$(ls -1 "$SAIDA_SPLIT_DIR"/*.txt 2>/dev/null | wc -l)
    log_info "Arquivos gerados no split: $NUM_SPLITS"
else
    log_error "Falha no split"
    exit 1
fi

# Executar merge
echo ""
log_info "Executando MERGE dos arquivos..."

if python3 merge_saidas_split.py; then
    log_info "Merge concluído com sucesso!"
    
    # Verificar arquivo final
    if [ -f "$DADOS_DIR/memorial_unificado.txt" ]; then
        FINAL_SIZE=$(wc -l < "$DADOS_DIR/memorial_unificado.txt")
        log_info "Arquivo unificado criado com $FINAL_SIZE linhas"
    fi
else
    log_error "Falha no merge"
    exit 1
fi

# Resumo final
echo ""
echo "====================================================="
echo -e "${GREEN}PIPELINE CONCLUÍDO COM SUCESSO!${NC}"
echo "====================================================="
echo ""
echo "📁 Arquivos gerados:"
echo "   - Split: $SAIDA_SPLIT_DIR/"
echo "   - Unificado: $DADOS_DIR/memorial_unificado.txt"
echo ""
echo "📊 Estatísticas:"
echo "   - Arquivo original: $(basename "$INPUT_FILE")"
echo "   - Partes geradas: $NUM_SPLITS"
echo "   - Linhas no arquivo final: $FINAL_SIZE"
echo ""

# Limpar temporários (opcional)
read -p "Deseja limpar arquivos temporários? (s/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    rm -f "$TEMP_DIR"/*.txt
    log_info "Arquivos temporários removidos"
fi

echo "✅ Processo finalizado!"