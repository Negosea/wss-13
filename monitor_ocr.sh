#!/bin/bash
echo "🔍 Monitorando OCR..."
while true; do
    if [ -f dados/pipeline_output/construcode_ocr.txt ]; then
        SIZE=$(stat -c%s dados/pipeline_output/construcode_ocr.txt)
        echo -ne "\rArquivo: ${SIZE} bytes"
    fi
    sleep 1
done
