#!/bin/bash

# ===================================================
# PROCESSADOR EM LOTE DE PDFS
# Autor: Marcos Sea
# Data: 09/06/2025
# ===================================================

PIPELINE="$HOME/projetos/framework-construcao/run_pipeline.sh"
DOWNLOADS="/home/sea/Downloads"
LOGS="$HOME/projetos/framework-construcao/dados/logs"
PROCESSADOS="$DOWNLOADS/PROCESSADOS_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$LOGS"
mkdir -p "$PROCESSADOS"

echo ""
echo "====================================================="
echo "      LOTE DE PDFS - FRAMEWORK CONSTRUÇÃO CIVIL"
echo "              Início: $(date '+%d/%m/%Y %H:%M:%S')"
echo "====================================================="
echo ""

COUNT_OK=0
COUNT_ERR=0

# Loop pelos arquivos PDF na pasta Downloads
for pdf in "$DOWNLOADS"/*.pdf; do
    if [ -f "$pdf" ]; then
        echo "---------------------------------------------"
        echo "Processando: $(basename "$pdf")"
        START_TIME=$(date '+%H:%M:%S')

        # Rodar o pipeline e salvar saída completa em LOG
        LOG="$LOGS/$(basename "$pdf" .pdf)_$(date +%H%M%S).log"
        "$PIPELINE" "$pdf" > "$LOG" 2>&1

        if grep -q "PIPELINE CONCLUÍDO COM SUCESSO" "$LOG"; then
            echo -e "\033[0;32m[S U C E S S O]\033[0m ($START_TIME)"
            COUNT_OK=$((COUNT_OK+1))
            # Move PDF para pasta de processados
            mv "$pdf" "$PROCESSADOS/"
        else
            echo -e "\033[0;31m[ F A L H O U ]\033[0m ($START_TIME)"
            COUNT_ERR=$((COUNT_ERR+1))
            echo "Veja os detalhes em: $LOG"
        fi
        echo ""
    fi
done

echo "====================================================="
echo -e "\033[0;32mPDFs processados com sucesso: $COUNT_OK\033[0m"
echo -e "\033[0;31mFalhas: $COUNT_ERR\033[0m"
echo "Logs detalhados em: $LOGS/"
echo "PDFs processados movidos para: $PROCESSADOS/"
echo "====================================================="
echo ""
