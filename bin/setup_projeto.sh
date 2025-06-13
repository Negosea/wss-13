#!/usr/bin/env bash
# Script: setup_projeto.sh
# Descrição: Configura ambiente do framework de construção
# Uso: ./setup_projeto.sh
# Autor: Marcos Sea
# Data: 2025-01-11

set -euo pipefail
trap 'echo "❌ Erro na linha $LINENO"; exit 1' ERR

# Diretórios do projeto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🏗️  Configurando Framework de Construção Civil..."
echo "📁 Diretório do projeto: $PROJECT_ROOT"

# Criar estrutura adicional se necessário
mkdir -p "$PROJECT_ROOT"/{plantas_baixadas,plantas_raspadas,saidas_split}

echo "✅ Estrutura criada com sucesso!"
