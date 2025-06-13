#!/bin/bash

echo "🏗️  Processamento em Lote - ConstruCode Framework"
echo "=============================================="
echo ""

# Diretório com as plantas
DIR_PLANTAS="plantas_teste"

# Criar diretório para relatórios com timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR_RELATORIOS="relatorios_${TIMESTAMP}"
mkdir -p "$DIR_RELATORIOS"

# Contador
TOTAL=0
SUCESSO=0

# Processar cada imagem PNG/JPG no diretório
for IMAGEM in "$DIR_PLANTAS"/*.{png,jpg,jpeg,PNG,JPG,JPEG} 2>/dev/null; do
    if [ -f "$IMAGEM" ]; then
        echo "📄 Processando: $(basename "$IMAGEM")"
        echo "----------------------------------------"
        
        # Executar pipeline
        ./pipeline.sh "$IMAGEM"
        
        if [ $? -eq 0 ]; then
            # Copiar PDF para diretório de relatórios
            NOME_BASE=$(basename "$IMAGEM" | sed 's/\.[^.]*$//')
            cp "${DIR_PLANTAS}/relatorio_${NOME_BASE}.pdf" "$DIR_RELATORIOS/" 2>/dev/null
            ((SUCESSO++))
            echo "✅ Sucesso!"
        else
            echo "❌ Erro ao processar"
        fi
        
        ((TOTAL++))
        echo ""
    fi
done

echo "=============================================="
echo "📊 Resumo do Processamento:"
echo "   Total de plantas: $TOTAL"
echo "   Processadas com sucesso: $SUCESSO"
echo "   Relatórios salvos em: $DIR_RELATORIOS/"
echo ""

# Criar índice HTML com todos os relatórios
if [ $SUCESSO -gt 0 ]; then
    echo "📝 Gerando índice HTML..."
    cat > "$DIR_RELATORIOS/index.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Relatórios ConstruCode - $TIMESTAMP</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .relatorio { margin: 10px 0; padding: 10px; background: #f5f5f5; }
        a { text-decoration: none; color: #0066cc; }
    </style>
</head>
<body>
    <h1>🏗️ Relatórios ConstruCode Framework</h1>
    <p>Gerado em: $(date '+%d/%m/%Y às %H:%M:%S')</p>
    <hr>
EOF

    for PDF in "$DIR_RELATORIOS"/*.pdf; do
        if [ -f "$PDF" ]; then
            NOME=$(basename "$PDF")
            echo "    <div class='relatorio'>📄 <a href='$NOME' target='_blank'>$NOME</a></div>" >> "$DIR_RELATORIOS/index.html"
        fi
    done

    echo "</body></html>" >> "$DIR_RELATORIOS/index.html"
    echo "✅ Índice HTML criado: $DIR_RELATORIOS/index.html"
fi