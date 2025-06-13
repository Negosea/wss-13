#!/bin/bash
# run_pipeline_ocr.sh
# Uso: ./run_pipeline_ocr.sh "caminho/do/seu.pdf"

set -e

PDF="$1"
BASENAME=$(basename "$PDF" .pdf)
TEMP_DIR="$HOME/projetos/framework-construcao/dados/temp"
TXT="$TEMP_DIR/${BASENAME}.txt"

check_tools() {
    for tool in pdftotext tesseract pdftoppm; do
        if ! command -v $tool &> /dev/null; then
            echo "[ERRO] Ferramenta '$tool' não instalada. Instale com: sudo apt install $tool"
            exit 1
        fi
    done
}

make_temp_dir() {
    mkdir -p "$TEMP_DIR"
}

extract_text_pdf() {
    pdftotext -layout "$PDF" "$TXT"
}

txt_has_content() {
    [[ -s "$TXT" ]]
}

run_ocr_on_pdf() {
    echo "[INFO] PDF parece ser imagem escaneada. Rodando OCR..."
    pdftoppm "$PDF" "$TEMP_DIR/${BASENAME}_page" -png
    > "$TXT"
    for IMG in "$TEMP_DIR"/${BASENAME}_page-*.png; do
        [ -e "$IMG" ] || continue
        tesseract "$IMG" "${IMG%.png}" -l por --psm 1 txt
        cat "${IMG%.png}.txt" >> "$TXT"
        echo -e "\n\n----\n\n" >> "$TXT"
    done
    echo "[INFO] OCR concluído! TXT gerado em $TXT"
}

process_in_pipeline() {
    echo "[INFO] Rodando pipeline no arquivo TXT gerado..."
    python3 /home/sea/projetos/framework-construcao/scripts/split_memorial.py "$TXT"
}

main() {
    check_tools
    make_temp_dir
    extract_text_pdf

    MIN_LINES=5
    TXT_LINES=0
    if [[ -f "$TXT" ]]; then
        TXT_LINES=$(wc -l < "$TXT" 2>/dev/null || echo "0")
    fi

    if [[ $TXT_LINES -lt $MIN_LINES ]]; then
        echo "[ALERTA] TXT vazio ou com pouco conteúdo ($TXT_LINES linhas). Forçando OCR!"
        run_ocr_on_pdf
        process_in_pipeline
    else
        echo "[OK] Texto extraído diretamente do PDF com $TXT_LINES linhas."
        process_in_pipeline
    fi
}

main "$@"