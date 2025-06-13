import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
# Novas importações para OCR
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile

# Configuração da página
st.set_page_config(
    page_title="WSF+13 - Análise de Construção",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main {padding-top: 0;}
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Funções de OCR
def extract_text_from_image(file, lang='por'):
    """Extrai texto de imagem usando OCR"""
    try:
        img = Image.open(file)
        text = pytesseract.image_to_string(img, lang=lang)
        return text
    except Exception as e:
        return f"Erro ao processar imagem: {str(e)}"

def extract_text_from_pdf(file, lang='por'):
    """Extrai texto de PDF usando OCR"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(tmp_file_path, output_folder=path)
            texto = ""
            progress_bar = st.progress(0)
            for i, img in enumerate(images):
                texto += f"\n--- Página {i+1} ---\n"
                texto += pytesseract.image_to_string(img, lang=lang) + "\n"
                progress_bar.progress((i + 1) / len(images))
            progress_bar.empty()
        
        os.unlink(tmp_file_path)
        return texto
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"

# Funções auxiliares
def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    data = {
        'Data': dates,
        'Custo_Planejado': np.cumsum(np.random.uniform(1000, 5000, len(dates))),
        'Custo_Real': np.cumsum(np.random.uniform(800, 5500, len(dates))),
        'Progresso_Fisico': np.minimum(100, np.cumsum(np.random.uniform(0.1, 0.5, len(dates)))),
        'Recursos_Alocados': np.random.randint(10, 50, len(dates)),
        'Qualidade_Score': np.random.uniform(0.7, 1.0, len(dates))
    }
    return pd.DataFrame(data)

# Header
st.markdown("""
<div class="metric-container">
    <h1 style='text-align: center; margin: 0;'>🏗️ WSF+13 - Framework de Análise de Construção</h1>
    <p style='text-align: center; margin: 10px 0 0 0; opacity: 0.9;'>Sistema Integrado de Gestão e Monitoramento</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção do tipo de análise
    tipo_analise = st.selectbox(
        "Tipo de Análise",
        ["📊 Dashboard Principal", "📈 Análise de Custos", "⏱️ Cronograma", 
         "👥 Recursos", "🎯 Indicadores KPI", "🔍 OCR de Documentos"]
    )
    
    # Filtros de data
    st.subheader("📅 Período de Análise")
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data Início", datetime(2024, 1, 1))
    with col2:
        data_fim = st.date_input("Data Fim", datetime(2024, 12, 31))
    
    # Opções avançadas
    with st.expander("🔧 Opções Avançadas"):
        mostrar_tendencias = st.checkbox("Mostrar Tendências", True)
        incluir_previsoes = st.checkbox("Incluir Previsões", False)
        intervalo_confianca = st.slider("Intervalo de Confiança (%)", 80, 99, 95)

# Dados
df = generate_sample_data()
df_filtrado = df[(df['Data'] >= pd.Timestamp(data_inicio)) & (df['Data'] <= pd.Timestamp(data_fim))]

# Conteúdo principal baseado na seleção
if tipo_analise == "🔍 OCR de Documentos":
    st.header("🔍 OCR de Documentos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📄 Upload de Documentos
        Faça upload de imagens ou PDFs para extrair texto automaticamente usando OCR.
        """)
        
        file = st.file_uploader(
            "Selecione um arquivo", 
            type=["jpg", "jpeg", "png", "pdf"],
            help="Formatos suportados: JPG, PNG, PDF"
        )
        
        if file:
            st.success(f"✅ Arquivo '{file.name}' carregado com sucesso!")
            
            # Opções de OCR
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                idioma = st.selectbox("Idioma do documento", ["por", "eng", "spa"])
            with col_opt2:
                processar = st.button("🚀 Processar OCR", type="primary")
            
            if processar:
                with st.spinner("🔄 Processando OCR..."):
                    if file.type.startswith("image"):
                        # Preview da imagem
                        st.image(file, caption=f"Preview: {file.name}", use_container_width=True)
                        texto = extract_text_from_image(file, lang=idioma)
                    elif file.type == "application/pdf":
                        texto = extract_text_from_pdf(file, lang=idioma)
                    else:
                        texto = "Formato não suportado."
                
                # Exibir resultado
                st.markdown("### 📝 Texto Extraído")
                text_area = st.text_area(
                    "Edite o texto se necessário:", 
                    texto, 
                    height=400,
                    help="Você pode editar o texto extraído antes de salvá-lo"
                )
                
                # Opções de download
                col_save1, col_save2, col_save3 = st.columns(3)
                with col_save1:
                    st.download_button(
                        label="💾 Salvar como TXT",
                        data=text_area,
                        file_name=f"ocr_{file.name.split('.')[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                with col_save2:
                    if st.button("📊 Analisar Texto"):
                        st.info("🚧 Análise de texto em desenvolvimento...")
                with col_save3:
                    if st.button("🔗 Integrar ao WSF+13"):
                        st.info("🚧 Integração em desenvolvimento...")
    
    with col2:
        st.markdown("""
        ### 💡 Dicas de Uso
        
        **Qualidade do OCR:**
        - ✅ Imagens nítidas e bem iluminadas
        - ✅ Texto em preto sobre fundo branco
        - ✅ Resolução mínima de 300 DPI
        - ❌ Evite imagens borradas ou inclinadas
        
        **Formatos suportados:**
        - 🖼️ JPG/JPEG
        - 🖼️ PNG
        - 📄 PDF (múltiplas páginas)
        
        **Idiomas disponíveis:**
        - 🇧🇷 Português (por)
        - 🇺🇸 Inglês (eng)
        - 🇪🇸 Espanhol (spa)
        """)
        
        # Estatísticas de OCR
        st.markdown("### 📊 Estatísticas")
        st.metric("Documentos Processados Hoje", "0")
        st.metric("Taxa de Sucesso", "0%")

elif tipo_analise == "📊 Dashboard Principal":
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        valor_atual = df_filtrado['Custo_Real'].iloc[-1]
        valor_planejado = df_filtrado['Custo_Planejado'].iloc[-1]
        delta = ((valor_atual - valor_planejado) / valor_planejado * 100)
        st.metric(
            "Custo Total", 
            f"R$ {valor_atual:,.2f}",
            f"{delta:+.1f}% vs planejado"
        )
    
    with col2:
        progresso = df_filtrado['Progresso_Fisico'].iloc[-1]
        st.metric(
            "Progresso Físico",
            f"{progresso:.1f}%",
            f"{progresso - df_filtrado['Progresso_Fisico'].iloc[-30]:.1f}% último mês"
        )
    
    with col3:
        recursos = df_filtrado['Recursos_Alocados'].mean()
        st.metric(
            "Recursos Médios",
            f"{recursos:.0f} pessoas",
            f"{(recursos - df_filtrado['Recursos_Alocados'].iloc[-30:].mean()):.0f} vs mês anterior"
        )
    
    with col4:
        qualidade = df_filtrado['Qualidade_Score'].mean()
        st.metric(
            "Score Qualidade",
            f"{qualidade:.2%}",
            f"{(qualidade - 0.85)*100:.1f}% vs meta"
        )
    
    # Gráficos principais
    st.subheader("📊 Análise Visual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_custo = go.Figure()
        fig_custo.add_trace(go.Scatter(
            x=df_filtrado['Data'],
            y=df_filtrado['Custo_Planejado'],
            name='Planejado',
            line=dict(color='blue', dash='dash')
        ))
        fig_custo.add_trace(go.Scatter(
            x=df_filtrado['Data'],
            y=df_filtrado['Custo_Real'],
            name='Real',
            line=dict(color='red')
        ))
        fig_custo.update_layout(
            title='Evolução de Custos',
            xaxis_title='Data',
            yaxis_title='Custo (R$)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_custo, use_container_width=True)
    
    with col2:
        fig_progresso = px.area(
            df_filtrado, 
            x='Data', 
            y='Progresso_Fisico',
            title='Progresso Físico do Projeto',
            color_discrete_sequence=['#00cc88']
        )
        fig_progresso.update_layout(
            yaxis_title='Progresso (%)',
            showlegend=False
        )
        st.plotly_chart(fig_progresso, use_container_width=True)

elif tipo_analise == "📈 Análise de Custos":
    st.header("📈 Análise Detalhada de Custos")
    
    # Análise de variação
    variacao = df_filtrado['Custo_Real'] - df_filtrado['Custo_Planejado']
    
    fig_variacao = go.Figure()
    fig_variacao.add_trace(go.Bar(
        x=df_filtrado['Data'],
        y=variacao,
        name='Variação',
        marker_color=np.where(variacao > 0, 'red', 'green')
    ))
    fig_variacao.update_layout(
        title='Variação de Custos (Real vs Planejado)',
        xaxis_title='Data',
        yaxis_title='Variação (R$)',
        showlegend=False
    )
    st.plotly_chart(fig_variacao, use_container_width=True)

elif tipo_analise == "⏱️ Cronograma":
    st.header("⏱️ Análise de Cronograma")
    st.info("Módulo em desenvolvimento - Gantt Chart em breve!")

elif tipo_analise == "👥 Recursos":
    st.header("👥 Gestão de Recursos")
    
    fig_recursos = px.line(
        df_filtrado,
        x='Data',
        y='Recursos_Alocados',
        title='Alocação de Recursos ao Longo do Tempo'
    )
    st.plotly_chart(fig_recursos, use_container_width=True)

elif tipo_analise == "🎯 Indicadores KPI":
    st.header("🎯 Indicadores de Performance (KPIs)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KPI de eficiência
        eficiencia = (df_filtrado['Custo_Planejado'].iloc[-1] / 
                     df_filtrado['Custo_Real'].iloc[-1] * 100)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = eficiencia,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Eficiência de Custo (%)"},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 150]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 80], 'color': "lightgray"},
                    {'range': [80, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Score de qualidade
        fig_quality = px.box(
            df_filtrado,
            y='Qualidade_Score',
            title='Distribuição do Score de Qualidade'
        )
        st.plotly_chart(fig_quality, use_container_width=True)

# Seção de relatórios
st.markdown("---")
st.subheader("📄 Geração de Relatórios")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="📊 Baixar PDF",
        data="Relatório em PDF",
        file_name=f"relatorio_wsf13_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )

with col2:
    st.download_button(
        label="📈 Baixar Dashboard",
        data="Dashboard completo",
        file_name=f"dashboard_wsf13_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )

with col3:
    st.download_button(
        label="📥 Baixar Excel",
        data="Relatório em Excel",
        file_name=f"relatorio_wsf13_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.ms-excel"
    )

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666;'>
        <p>WSF+13 Framework v1.0 | Desenvolvido por Marcos Sea | 
        {datetime.now().strftime("%d/%m/%Y %H:%M:%S (UTC-3)")}</p>
    </div>
    """,
    unsafe_allow_html=True
)