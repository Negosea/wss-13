import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="WSF+13 Dashboard", page_icon="🏗️", layout="wide")

st.title("🏗️ WSF+13 - Dashboard Simplificado")
st.write(f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S (UTC-3)')}")

# Dados de exemplo
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Projetos Ativos", "15", "+3")
with col2:
    st.metric("Eficiência", "87%", "+5%")
with col3:
    st.metric("Economia", "R$ 45.000", "+12%")

# Tabela simples
st.subheader("📊 Dados de Projetos")
df = pd.DataFrame({
    'Projeto': ['Casa A', 'Casa B', 'Prédio C'],
    'Status': ['Em andamento', 'Concluído', 'Planejamento'],
    'Economia': ['R$ 15.000', 'R$ 20.000', 'R$ 10.000']
})
st.dataframe(df)

st.success("Dashboard funcionando! Instale plotly para gráficos avançados.")
