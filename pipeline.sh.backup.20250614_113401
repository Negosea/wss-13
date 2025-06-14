#!/bin/bash

# pipeline.sh - Pipeline completo Framework Construção Civil

set -e

IMAGEM=${1:-plantas_teste/planta_construcode_pagina1.png}
JSON_ANALISADOR="plantas_teste/resultado_analisador.json"
JSON_FINAL="plantas_teste/resultado_analisador_com_area.json"

echo "🏗️  Framework Construção Civil - Pipeline Automático"
echo "==============================================="
echo "🔍 Processando imagem: $IMAGEM"
echo

# 1. Analisar a planta
python scripts/analisador_plantas_wsf.py "$IMAGEM"

# 2. Corrigir para o formato compatível
python scripts/corrige_formato_json.py

# 3. Calcular áreas
python scripts/calcula_area_total.py

# 4. Exibir arquivos e resumo
echo
echo "📄 Arquivos JSON gerados:"
ls -la plantas_teste/*.json

echo
echo "�� Resultado final (áreas calculadas):"
if [ -f "$JSON_FINAL" ]; then
    cat "$JSON_FINAL"
else
    echo "Arquivo $JSON_FINAL não encontrado."
fi

echo
echo "✅ Pipeline concluído com sucesso!"
