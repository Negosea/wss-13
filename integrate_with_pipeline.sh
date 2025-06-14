#!/bin/bash
# integrate_with_pipeline.sh - Adiciona organizador ao pipeline

# Fazer backup do pipeline.sh
if [ -f "pipeline.sh" ]; then
    cp pipeline.sh pipeline.sh.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup do pipeline.sh criado"
fi

# Adicionar organização ao início do pipeline
if [ -f "pipeline.sh" ]; then
    # Criar novo pipeline com organização
    cat > pipeline_temp.sh << 'EOF'
#!/bin/bash
# Pipeline com Framework Organizer integrado

echo "🧹 Organizando projeto antes do processamento..."
./organize.sh

# Continuar com o pipeline original
EOF
    
    # Adicionar conteúdo original do pipeline (pulando shebang)
    tail -n +2 pipeline.sh >> pipeline_temp.sh
    
    # Substituir pipeline
    mv pipeline_temp.sh pipeline.sh
    chmod +x pipeline.sh
    
    echo "✅ Organizador integrado ao pipeline.sh"
else
    echo "⚠️  pipeline.sh não encontrado"
fi
