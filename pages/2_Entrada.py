import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

df = pd.read_csv('content/gasto.csv')

col1, col2, col3, col4 = st.columns(4)

with col1:
    name = st.text_input('Qual seu nome?', '')
with col2:
    entrada = st.text_input('Adicione o valor de entrada de dinheiro:', '')
with col3:
    data = st.text_input('Adicione a data da entrada:', '')
with col4:
    origem = st.text_input('De onde veio?', '')

with st.form('my_form'):
    submitted = st.form_submit_button("Enviar")

st.write(df)