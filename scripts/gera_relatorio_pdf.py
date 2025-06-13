#!/usr/bin/env python3

from fpdf import FPDF
import json
import sys

ARQUIVO_JSON = 'plantas_teste/resultado_analisador_com_area.json'
ARQUIVO_PDF  = 'plantas_teste/relatorio_area.pdf'

if len(sys.argv) > 1:
    ARQUIVO_JSON = sys.argv[1]
if len(sys.argv) > 2:
    ARQUIVO_PDF = sys.argv[2]

with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

projeto = dados["projeto"]
geometria = dados["geometria"]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatório de Áreas - ConstruCode Framework", ln=True, align="C")

pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, f"Projeto: {projeto['nome']}", ln=True)
pdf.cell(0, 10, f"Data da Análise: {projeto['data']}", ln=True)
pdf.cell(0, 10, f"Responsável: {projeto['responsavel']}", ln=True)
pdf.ln(10)

pdf.set_font("Arial", "B", 12)
pdf.cell(60, 10, "Ambiente", 1)
pdf.cell(35, 10, "Largura (m)", 1)
pdf.cell(45, 10, "Comprimento (m)", 1)
pdf.cell(40, 10, "Área (m²)", 1)
pdf.ln()

pdf.set_font("Arial", "", 12)
for m in geometria["medidas"]:
    area = m["largura"] * m["comprimento"]
    pdf.cell(60, 10, str(m["ambiente"]), 1)
    pdf.cell(35, 10, f"{m['largura']:.2f}", 1, align="C")
    pdf.cell(45, 10, f"{m['comprimento']:.2f}", 1, align="C")
    pdf.cell(40, 10, f"{area:.2f}", 1, align="C")
    pdf.ln()

pdf.ln(5)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 12, f"Área Total Construída: {geometria.get('area_total', sum(m['largura']*m['comprimento'] for m in geometria['medidas'])):.2f} m²", ln=True, align="C")

pdf.output(ARQUIVO_PDF)
print(f"✅ Relatório PDF gerado: {ARQUIVO_PDF}")