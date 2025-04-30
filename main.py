import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Barbearia", layout="wide")
st.title("💈 Dashboard da Barbearia")

# Carregar dados
df = pd.read_csv("agendamentos_barbearia.csv")
df['Data'] = pd.to_datetime(df['Data'])

# Sidebar
st.sidebar.title("Filtros")
barbeiros = st.sidebar.multiselect("Selecione os Barbeiros", options=df['Barbeiro'].unique(), default=df['Barbeiro'].unique())
formas_pagamento = st.sidebar.multiselect("Selecione as Formas de Pagamento", options=df['Forma de pagamento'].unique(), default=df['Forma de pagamento'].unique())

# Filtrando os dados com base nos filtros da sidebar
df_filtered = df[df['Barbeiro'].isin(barbeiros) & df['Forma de pagamento'].isin(formas_pagamento)]

# Visualizar dados filtrados
st.subheader("📋 Visualização dos Agendamentos")
st.dataframe(df_filtered)

# KPIs
st.header("🔢 Indicadores Gerais")
col1, col2, col3 = st.columns(3)

faturamento_total = df_filtered['Valor pago'].sum()
clientes_totais = df_filtered['Nome'].nunique()
servicos_totais = df_filtered['Serviço'].count()

col1.metric("💵 Faturamento Total", f"R${faturamento_total:.2f}")
col2.metric("🧍‍♂️ Clientes Únicos", clientes_totais)
col3.metric("✂️ Serviços Realizados", servicos_totais)

# Faturamento por Forma de Pagamento
st.subheader("💳 Faturamento por Forma de Pagamento")
pagamento_fig = px.pie(df_filtered, names='Forma de pagamento', values='Valor pago', title="Distribuição por Forma de Pagamento")
st.plotly_chart(pagamento_fig, use_container_width=True)

# Serviços mais vendidos
st.subheader("✂️ Serviços Mais Vendidos")
# Contar os serviços e resetar o índice
servicos_count = df_filtered['Serviço'].value_counts().reset_index()
# Renomear as colunas para que fique mais fácil de usar no gráfico
servicos_count.columns = ['Serviço', 'Quantidade']
# Agora podemos passar as colunas corretamente
servicos_fig = px.bar(servicos_count, 
                      x='Serviço', y='Quantidade',
                      title="Tipos de Serviços")
st.plotly_chart(servicos_fig, use_container_width=True)


# Faturamento por barbeiro
st.subheader("🧔‍♂️ Faturamento por Barbeiro")
barbeiro_fig = px.bar(df_filtered.groupby('Barbeiro')['Valor pago'].sum().reset_index(), 
                      x='Barbeiro', y='Valor pago',
                      title="Faturamento por Barbeiro",
                      text_auto='.2s')
st.plotly_chart(barbeiro_fig, use_container_width=True)

# Faturamento diário
st.subheader("📅 Faturamento por Dia")
dia_fig = px.line(df_filtered.groupby('Data')['Valor pago'].sum().reset_index(), 
                  x='Data', y='Valor pago', 
                  title="Faturamento Diário", markers=True)
st.plotly_chart(dia_fig, use_container_width=True)
