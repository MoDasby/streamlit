import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Dashboard Barbearia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS com tema escuro
st.markdown("""
    <style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stMetric {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #404040;
        color: #ffffff;
    }
    .stMetric:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        border: 1px solid #505050;
    }
    h1 {
        color: #00b4d8;
        font-size: 2.5rem;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #00b4d8;
    }
    h2 {
        color: #90e0ef;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
    }
    h3 {
        color: #caf0f8;
        font-size: 1.4rem;
        font-weight: 600;
    }
    .stDataFrame {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 10px;
        padding: 1rem;
    }
    .stSidebar {
        background-color: #2d2d2d;
        padding: 1rem;
    }
    .stSidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stSelectbox, .stMultiselect, .stDateInput {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stSelectbox > div, .stMultiselect > div, .stDateInput > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stSelectbox > div > div, .stMultiselect > div > div, .stDateInput > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stSelectbox > div > div:hover, .stMultiselect > div > div:hover, .stDateInput > div > div:hover {
        background-color: #404040;
    }
    .stDataFrame > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stDataFrame > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Título com ícone e descrição
st.title("💈 Dashboard da Barbearia")
st.markdown("### Análise completa de desempenho e métricas do negócio")

# Carregar dados
df = pd.read_csv("agendamentos_barbearia.csv")
df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M').dt.hour

# Sidebar com filtros avançados
st.sidebar.title("⚙️ Filtros")
st.sidebar.markdown("---")

# Filtro de período
data_inicio = st.sidebar.date_input(
    "Data Inicial",
    value=df['Data'].min(),
    min_value=df['Data'].min(),
    max_value=df['Data'].max()
)
data_fim = st.sidebar.date_input(
    "Data Final",
    value=df['Data'].max(),
    min_value=df['Data'].min(),
    max_value=df['Data'].max()
)

# Outros filtros
barbeiros = st.sidebar.multiselect(
    "👨‍💼 Barbeiros",
    options=df['Barbeiro'].unique(),
    default=df['Barbeiro'].unique()
)

formas_pagamento = st.sidebar.multiselect(
    "💳 Formas de Pagamento",
    options=df['Forma de pagamento'].unique(),
    default=df['Forma de pagamento'].unique()
)

servicos = st.sidebar.multiselect(
    "✂️ Serviços",
    options=df['Serviço'].unique(),
    default=df['Serviço'].unique()
)

# Filtrando os dados
df_filtered = df[
    (df['Data'].dt.date >= data_inicio) &
    (df['Data'].dt.date <= data_fim) &
    (df['Barbeiro'].isin(barbeiros)) &
    (df['Forma de pagamento'].isin(formas_pagamento)) &
    (df['Serviço'].isin(servicos))
]

# Métricas principais
st.header("📊 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

faturamento_total = df_filtered['Valor pago'].sum()
clientes_totais = df_filtered['Nome'].nunique()
servicos_totais = df_filtered['Serviço'].count()
ticket_medio = faturamento_total / servicos_totais if servicos_totais > 0 else 0

col1.metric("💵 Faturamento Total", f"R${faturamento_total:.2f}")
col2.metric("🧍‍♂️ Clientes Únicos", clientes_totais)
col3.metric("✂️ Serviços Realizados", servicos_totais)
col4.metric("💰 Ticket Médio", f"R${ticket_medio:.2f}")

# Métricas secundárias
st.header("📈 Métricas de Desempenho")
col1, col2, col3, col4 = st.columns(4)

# Calcular métricas adicionais
dias_operacao = (data_fim - data_inicio).days + 1
faturamento_diario = faturamento_total / dias_operacao if dias_operacao > 0 else 0
servicos_diarios = servicos_totais / dias_operacao if dias_operacao > 0 else 0
ocupacao_diaria = servicos_totais / (len(barbeiros) * dias_operacao * 8) * 100 if dias_operacao > 0 else 0

col1.metric("📅 Faturamento Diário", f"R${faturamento_diario:.2f}")
col2.metric("⏰ Serviços por Dia", f"{servicos_diarios:.1f}")
col3.metric("📊 Taxa de Ocupação", f"{ocupacao_diaria:.1f}%")
col4.metric("👥 Clientes por Dia", f"{clientes_totais/dias_operacao:.1f}")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Distribuição por Forma de Pagamento")
    pagamento_fig = px.pie(
        df_filtered,
        names='Forma de pagamento',
        values='Valor pago',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    pagamento_fig.update_traces(textposition='inside', textinfo='percent+label')
    pagamento_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    st.plotly_chart(pagamento_fig, use_container_width=True)

with col2:
    st.subheader("✂️ Serviços Mais Vendidos")
    servicos_count = df_filtered['Serviço'].value_counts().reset_index()
    servicos_count.columns = ['Serviço', 'Quantidade']
    servicos_fig = px.bar(
        servicos_count,
        x='Serviço',
        y='Quantidade',
        color='Serviço',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    servicos_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Serviço",
        yaxis_title="Quantidade",
        font=dict(color='#ffffff')
    )
    st.plotly_chart(servicos_fig, use_container_width=True)

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧔‍♂️ Desempenho por Barbeiro")
    barbeiro_metrics = df_filtered.groupby('Barbeiro').agg({
        'Valor pago': 'sum',
        'Serviço': 'count'
    }).reset_index()
    barbeiro_metrics.columns = ['Barbeiro', 'Faturamento', 'Serviços']
    
    barbeiro_fig = go.Figure()
    barbeiro_fig.add_trace(go.Bar(
        x=barbeiro_metrics['Barbeiro'],
        y=barbeiro_metrics['Faturamento'],
        name='Faturamento',
        marker_color='#00b4d8'
    ))
    barbeiro_fig.add_trace(go.Bar(
        x=barbeiro_metrics['Barbeiro'],
        y=barbeiro_metrics['Serviços'],
        name='Serviços',
        marker_color='#90e0ef'
    ))
    barbeiro_fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Barbeiro",
        yaxis_title="Valor",
        font=dict(color='#ffffff')
    )
    st.plotly_chart(barbeiro_fig, use_container_width=True)

with col2:
    st.subheader("📅 Evolução do Faturamento")
    faturamento_diario = df_filtered.groupby('Data')['Valor pago'].sum().reset_index()
    dia_fig = px.line(
        faturamento_diario,
        x='Data',
        y='Valor pago',
        markers=True,
        color_discrete_sequence=['#00b4d8']
    )
    dia_fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Faturamento (R$)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    st.plotly_chart(dia_fig, use_container_width=True)

# Análise de horários
st.header("⏰ Análise de Horários")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição por Horário")
    horarios_count = df_filtered['Hora'].value_counts().sort_index().reset_index()
    horarios_count.columns = ['Hora', 'Quantidade']
    
    horarios_fig = px.bar(
        horarios_count,
        x='Hora',
        y='Quantidade',
        color='Quantidade',
        color_continuous_scale='Viridis'
    )
    horarios_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Hora do Dia",
        yaxis_title="Quantidade de Serviços",
        font=dict(color='#ffffff')
    )
    st.plotly_chart(horarios_fig, use_container_width=True)

with col2:
    st.subheader("Horários por Barbeiro")
    horarios_barbeiro = df_filtered.pivot_table(
        values='Serviço',
        index='Hora',
        columns='Barbeiro',
        aggfunc='count'
    ).fillna(0)
    
    horarios_barbeiro_fig = go.Figure(data=go.Heatmap(
        z=horarios_barbeiro.values,
        x=horarios_barbeiro.columns,
        y=horarios_barbeiro.index,
        colorscale='Viridis'
    ))
    horarios_barbeiro_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Barbeiro",
        yaxis_title="Hora do Dia",
        font=dict(color='#ffffff')
    )
    st.plotly_chart(horarios_barbeiro_fig, use_container_width=True)

# Tabela de dados filtrados
st.header("📋 Dados Detalhados")
st.dataframe(
    df_filtered.sort_values('Data', ascending=False),
    use_container_width=True,
    hide_index=True
)
