#!/usr/bin/env python3
"""Corrige o formato do JSON para compatibilidade"""

import json
from datetime import datetime

# Ler o JSON atual
with open('plantas_teste/resultado_analisador.json', 'r') as f:
    dados_atuais = json.load(f)

# Criar novo formato
novo_formato = {
    "projeto": {
        "nome": dados_atuais.get("projeto", "Análise Automática de Planta Baixa"),
        "data": datetime.now().strftime("%Y-%m-%d"),
        "responsavel": "Marcos Sea"
    },
    "geometria": {
        "medidas": dados_atuais.get("medidas", [])
    }
}

# Salvar no formato correto
with open('plantas_teste/resultado_analisador.json', 'w') as f:
    json.dump(novo_formato, f, indent=2, ensure_ascii=False)

print("✅ Formato JSON corrigido!")
print(json.dumps(novo_formato, indent=2, ensure_ascii=False))
