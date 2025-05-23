
import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Envio de Transações API Exchange", layout="wide")

st.title("Envio de Boletos via API Exchange")

uploaded_file = st.file_uploader("Faça upload do arquivo com os boletos (.xlsx ou .csv)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    st.success("Arquivo carregado com sucesso!")
    st.dataframe(df.head())

    required_fields = ['AGENCIA', 'BANCO', 'CNPJPCPFCLIENTE', 'DATAOP', 'DATALQ', 'DATAME', 'DATAMN',
                       'FORMAME', 'FORMAMN', 'GIRO', 'IMPRESSO', 'LEILAO', 'MOEDA', 'OPLINHA',
                       'PAIS', 'PARIDADE', 'PLATBMF', 'RSISB', 'SEGMENTO', 'STATUS', 'TAXAOP',
                       'TIPO', 'VALORME', 'VALORMN']

    missing_cols = [col for col in required_fields if col not in df.columns]
    if missing_cols:
        st.error(f"Colunas obrigatórias ausentes no arquivo: {missing_cols}")
    else:
        api_url = "http://4.203.104.143/wsExchangeREST/api/exchange/insertBoleto"

        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        def send_boleto(row):
            payload = row[required_fields].to_dict()
            try:
                response = requests.post(api_url, headers=headers, json=payload)
                return response.status_code, response.json()
            except Exception as e:
                return 500, {"MENSAGEM": str(e)}

        if st.button("Enviar todos os boletos"):
            st.info("Iniciando envio dos boletos...")
            results = []
            for i, row in df.iterrows():
                code, result = send_boleto(row)
                results.append((i + 1, code, result.get("MENSAGEM", "Erro desconhecido")))

            st.success("Envio concluído!")
            for r in results:
                st.write(f"Linha {r[0]}: Status {r[1]} - {r[2]}")
