import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

df = pd.read_csv('content/gasto.csv')


with st.form('my_form'):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input('Qual seu nome?', '')
    with col2:
        entrada = st.text_input('Adicione o valor de entrada de dinheiro:', '')
    with col3:
        data = st.text_input('Adicione a data da entrada:', '')
    with col4:
        origem = st.text_input('De onde veio?', '')

    submitted = st.form_submit_button("Enviar")

if submitted:
    new_data = {"Nome": name, "Valor": int(entrada), "Data": data, "Origem": origem}
    df = df.append(new_data)
    df.to_csv('content/gasto.csv')

st.write(df)