#!/usr/bin/env python3

from fpdf import FPDF
import json
import sys
import os
from datetime import datetime
from PIL import Image

class RelatorioPlanta(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ConstruCode Framework - Relatório de Análise', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def gerar_relatorio_pdf(arquivo_json, arquivo_imagem, arquivo_pdf):
    # Carregar dados JSON
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    projeto = dados["projeto"]
    geometria = dados["geometria"]
    
    # Criar PDF
    pdf = RelatorioPlanta()
    pdf.add_page()
    
    # Título do projeto
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Projeto: {projeto['nome']}", ln=True)
    
    # Informações do projeto
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Data da Análise: {projeto['data']}", ln=True)
    pdf.cell(0, 8, f"Responsável: {projeto['responsavel']}", ln=True)
    pdf.cell(0, 8, f"Arquivo Original: {os.path.basename(arquivo_imagem)}", ln=True)
    pdf.ln(5)
    
    # Adicionar imagem da planta (se existir)
    if os.path.exists(arquivo_imagem):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Planta Analisada:", ln=True)
        
        # Redimensionar imagem para caber no PDF
        img = Image.open(arquivo_imagem)
        img_width, img_height = img.size
        
        # Calcular dimensões para o PDF (máximo 170mm de largura)
        max_width = 170
        ratio = min(max_width / img_width, 100 / img_height)
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        # Adicionar imagem centralizada
        x = (210 - new_width) / 2  # A4 = 210mm largura
        pdf.image(arquivo_imagem, x=x, y=pdf.get_y(), w=new_width)
        pdf.ln(new_height + 5)
    
    # Tabela de ambientes
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalhamento dos Ambientes:", ln=True)
    pdf.ln(2)
    
    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(60, 8, "Ambiente", 1, 0, 'C', True)
    pdf.cell(35, 8, "Largura (m)", 1, 0, 'C', True)
    pdf.cell(45, 8, "Comprimento (m)", 1, 0, 'C', True)
    pdf.cell(40, 8, "Área (m²)", 1, 1, 'C', True)
    
    # Dados da tabela
    pdf.set_font("Arial", "", 10)
    total_area = 0
    for i, m in enumerate(geometria["medidas"]):
        area = m["largura"] * m["comprimento"]
        total_area += area
        
        # Alternar cores das linhas
        if i % 2 == 0:
            pdf.set_fill_color(240, 240, 240)
            fill = True
        else:
            fill = False
            
        pdf.cell(60, 7, str(m["ambiente"]), 1, 0, 'L', fill)
        pdf.cell(35, 7, f"{m['largura']:.2f}", 1, 0, 'C', fill)
        pdf.cell(45, 7, f"{m['comprimento']:.2f}", 1, 0, 'C', fill)
        pdf.cell(40, 7, f"{area:.2f}", 1, 1, 'C', fill)
    
    # Total
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(180, 180, 180)
    pdf.cell(140, 8, "ÁREA TOTAL CONSTRUÍDA", 1, 0, 'R', True)
    pdf.cell(40, 8, f"{geometria.get('area_total', total_area):.2f} m²", 1, 1, 'C', True)
    
    # Rodapé com timestamp
    pdf.ln(10)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 8, f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", ln=True, align='R')
    
    # Salvar PDF
    pdf.output(arquivo_pdf)
    print(f"✅ PDF gerado: {arquivo_pdf}")

# Execução principal
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python gera_relatorio_pdf_completo.py <arquivo_json> <arquivo_imagem> [arquivo_pdf]")
        sys.exit(1)
    
    arquivo_json = sys.argv[1]
    arquivo_imagem = sys.argv[2]
    
    # Nome do PDF baseado no nome da imagem
    if len(sys.argv) > 3:
        arquivo_pdf = sys.argv[3]
    else:
        nome_base = os.path.splitext(os.path.basename(arquivo_imagem))[0]
        arquivo_pdf = f"plantas_teste/relatorio_{nome_base}.pdf"
    
    gerar_relatorio_pdf(arquivo_json, arquivo_imagem, arquivo_pdf)