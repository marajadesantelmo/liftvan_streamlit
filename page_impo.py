import streamlit as st
import pandas as pd
import time
from datetime import datetime

def show_page_impo():
    # Load data
    impo = pd.read_csv('impo.csv')

    col_title, col_logo, col_simpa = st.columns([5, 1, 1])
    with col_title:
        st.header(f"Estado de mudanzas de IMPO")
        col_title1, col_title2 = st.columns([1, 3])
        with col_title1:
            titulares = impo['Titular'].dropna().unique().tolist()
            titulares.sort()
            search_name = st.selectbox("Buscar por nombre de titular", options=["(Todos)"] + titulares)
            if search_name and search_name != "(Todos)":
                impo = impo[impo['Titular'] == search_name]
    with col_logo:
        st.image('logo_ypf.png')
    with col_simpa:
        st.image('logo_liftvan.png')
    
    # Apply the filtered dataframe to create the status-based dataframes
    abiertos = impo[impo['Estado'] == 'Abierto'][['Titular', 'Coordinador','Tipo','Origen', 'Destino', 'ETA', 'ETD']]
    arribados = impo[impo['Estado'] == 'Arribado'][['Titular', 'Coordinador','Tipo','Origen', 'Destino', 'ETA', 'ETD', 'Fecha Verificacion']]
    en_deposito = impo[impo['Estado'] == 'En deposito'][['Titular', 'Coordinador','Tipo','Origen', 'Destino', 'ETA', 'ETD', 'Fecha Verificacion','Fecha Fiscal', 'Fecha Entrega']]
    finalizados = impo[impo['Estado'] == 'Finalizado'][['Titular', 'Coordinador','Tipo','Origen', 'Destino', 'ETA', 'ETD', 'Fecha Verificacion','Fecha Fiscal', 'Fecha Retiro', 'Fecha Entrega', 'Quality Report']]

    col1, col2 = st.columns(2)
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Abiertos")
        st.dataframe(abiertos,
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Arribados")
        st.dataframe(arribados,
                    hide_index=True, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("En deposito")
        st.dataframe(en_deposito,
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Finalizados")
        st.dataframe(finalizados,
                     hide_index=True, use_container_width=True)


if __name__ == "__main__":
    while True:
        show_page_impo()
        time.sleep(60)  
        st.experimental_rerun()

