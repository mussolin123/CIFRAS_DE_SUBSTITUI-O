import streamlit as st
from collections import Counter
import plotly.express as px
import pandas as pd

# Esta função deixa todas as letras minúsculas e remove tudo que não for letra
def limpar_texto(texto):
    texto = texto.lower()
    return ''.join(letra for letra in texto if letra.isalpha())

# Esta função conta quantas vezes cada letra aparece no texto
def contar_letras(texto):
    texto_limpo = limpar_texto(texto)
    letras_contadas = Counter(texto_limpo)
    total_de_letras = sum(letras_contadas.values())
    return letras_contadas, total_de_letras

# Esta função cria uma lista com as 10 letras mais usadas, mostrando a porcentagem
def preparar_dados(letras_contadas, total):
    dados = []
    for letra, qtd in letras_contadas.most_common(10):
        porcentagem = (qtd / total) * 100
        dados.append({
            'Letra': letra.upper(),
            'Quantidade': qtd,
            'Porcentagem (%)': round(porcentagem, 2)
        })
    return dados

# Esta função mostra o gráfico e a tabela um do lado do outro
def mostrar_grafico_e_tabela(dados, titulo, cor):
    st.subheader(titulo)
    coluna1, coluna2 = st.columns([2, 1])

    # Gráfico
    with coluna1:
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

    # Tabela
    with coluna2:
        tabela = pd.DataFrame(dados)
        tabela.index = range(1, 11)
        st.markdown("**Top 10 Letras:**")
        st.dataframe(tabela, use_container_width=True)

# Esta função mostra um gráfico comparando as 5 letras mais usadas em cada idioma
def comparar_top5(pt_contagem, pt_total, en_contagem, en_total):
    st.subheader("🔠 Comparativo: Top 5 Letras Mais Frequentes")

    top5_pt = pt_contagem.most_common(5)
    top5_en = en_contagem.most_common(5)

    dados_comparativos = []

    for letra, qtd in top5_pt:
        dados_comparativos.append({
            'Letra': letra.upper(),
            'Idioma': 'Português',
            'Porcentagem': round((qtd / pt_total) * 100, 2)
        })

    for letra, qtd in top5_en:
        dados_comparativos.append({
            'Letra': letra.upper(),
            'Idioma': 'Inglês',
            'Porcentagem': round((qtd / en_total) * 100, 2)
        })

    df_comparativo = pd.DataFrame(dados_comparativos)

    fig = px.bar(
        df_comparativo,
        x='Letra',
        y='Porcentagem',
        color='Idioma',
        barmode='group',
        text='Porcentagem',
        color_discrete_map={'Português': 'green', 'Inglês': 'blue'}
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title='Porcentagem (%)', xaxis_title='Letra')
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Começo do aplicativo
# --------------------------

st.title("📊 Análise de Frequência de Letras")

# Caixas para colar os textos
texto_pt = st.text_area("Cole aqui o texto em **Português**:", height=200)
texto_en = st.text_area("Cole aqui o texto em **Inglês**:", height=200)

# Quando clicar no botão, faz a análise
if st.button("Analisar frequência"):
    if texto_pt and texto_en:
        # Conta as letras nos dois textos
        pt_contagem, pt_total = contar_letras(texto_pt)
        en_contagem, en_total = contar_letras(texto_en)

        # Prepara os dados para exibir
        dados_pt = preparar_dados(pt_contagem, pt_total)
        dados_en = preparar_dados(en_contagem, en_total)

        # Mostra resultado em uma linha: Português
        mostrar_grafico_e_tabela(dados_pt, "📘 Português", "green")

        # Linha separadora
        st.markdown("---")

        # Mostra resultado em outra linha: Inglês
        mostrar_grafico_e_tabela(dados_en, "📗 Inglês", "blue")

        # Mostra gráfico comparando os dois idiomas
        comparar_top5(pt_contagem, pt_total, en_contagem, en_total)
    else:
        st.warning("⚠️ Por favor, cole os dois textos para analisar.")
