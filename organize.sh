#!/bin/bash
# organize.sh - Script para executar o Framework Organizer

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Executar organizador
python3 scripts/organizer/framework_organizer.py "$@"
