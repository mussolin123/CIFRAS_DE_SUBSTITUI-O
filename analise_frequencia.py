import streamlit as st
from collections import Counter
import plotly.express as px
import pandas as pd  # <- usamos para exibir tabelas bonitas

# Função para limpar o texto
def limpar_texto(texto):
    texto = texto.lower()
    return ''.join(letra for letra in texto if letra.isalpha())

# Função para contar letras e calcular porcentagem
def contar_letras(texto):
    texto_limpo = limpar_texto(texto)
    contagem = Counter(texto_limpo)
    total = sum(contagem.values())
    return contagem, total

# Função para mostrar gráfico + tabela
def mostrar_resultado(contagem, total, titulo, cor):
    st.subheader(titulo)

    # Top 10 letras mais comuns
    dados = []
    for letra, quantidade in contagem.most_common(10):
        porcentagem = (quantidade / total) * 100
        dados.append({
            'Letra': letra.upper(),
            'Quantidade': quantidade,
            'Porcentagem (%)': round(porcentagem, 2)
        })

    # Gráfico interativo
    fig = px.bar(
        dados,
        x='Letra',
        y='Quantidade',
        text='Porcentagem (%)',
        color_discrete_sequence=[cor],
        hover_data={'Porcentagem (%)': True}
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title='Quantidade', xaxis_title='Letra')
    st.plotly_chart(fig, use_container_width=True)

    # Tabela formatada com pandas
    df_tabela = pd.DataFrame(dados)
    df_tabela.index = range(1, 11)  # para numerar de 1 a 10
    st.markdown("**Top 10 letras mais frequentes:**")
    st.dataframe(df_tabela, use_container_width=True)

# Título do app
st.title("Análise de Frequência de Letras")

# Entrada de texto
texto_pt = st.text_area("Texto em Português:", height=200)
texto_en = st.text_area("Texto em Inglês:", height=200)

# Botão de análise
if st.button("Analisar frequência"):
    if texto_pt and texto_en:
        cont_pt, total_pt = contar_letras(texto_pt)
        cont_en, total_en = contar_letras(texto_en)

        col1, col2 = st.columns(2)
        with col1:
            mostrar_resultado(cont_pt, total_pt, "Português", "green")
        with col2:
            mostrar_resultado(cont_en, total_en, "Inglês", "blue")
    else:
        st.warning("Por favor, cole os dois textos antes de clicar no botão.")
