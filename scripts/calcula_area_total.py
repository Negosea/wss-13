import json
import os

CAMINHO_JSON = "plantas_teste/resultado_analisador.json"  # defina aqui o caminho do seu JSON de entrada
CAMINHO_SAIDA = "plantas_teste/resultado_analisador_com_area.json"

# Critérios para filtrar dimensões válidas (ajuste conforme sua planta)
LARGURA_MINIMA = 2  # em metros (valores menores podem ser ruído, como 2x4 pode ser parede ou porta)
COMPRIMENTO_MINIMO = 2

def calcula_area_total(medidas):
    area_total = 0.0
    for medida in medidas:
        try:
            largura = float(medida["largura"])
            comprimento = float(medida["comprimento"])
            if largura >= LARGURA_MINIMA and comprimento >= COMPRIMENTO_MINIMO:
                area = largura * comprimento
                area_total += area
        except Exception as e:
            print(f"Erro em medida: {medida}. Detalhes: {e}")
    return area_total
# Leitura do arquivo JSON
if not os.path.exists(CAMINHO_JSON):
    raise FileNotFoundError(f"O arquivo de entrada '{CAMINHO_JSON}' não foi encontrado.")
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Verifica se as chaves esperadas existem
if "geometria" not in dados or "medidas" not in dados["geometria"]:
    raise KeyError("O JSON de entrada deve conter as chaves 'geometria' e 'geometria'['medidas']")

# Cálculo da soma das áreas
area_total = calcula_area_total(dados["geometria"]["medidas"])
print(f"Área total calculada: {area_total:.2f} m²")

# Atualiza o JSON e salva
dados["geometria"]["area_total"] = area_total

with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

print(f"Arquivo atualizado salvo em: {CAMINHO_SAIDA}")