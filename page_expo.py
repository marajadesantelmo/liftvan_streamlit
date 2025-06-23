import streamlit as st
import pandas as pd
import time
from datetime import datetime

def show_page_expo():
    # Load data
    expo = pd.read_csv('expo.csv')

    col_title, col_logo, col_simpa = st.columns([5, 1, 1])
    with col_title:
        st.header(f"Estado de mudanzas de EXPO")
        col_title1, col_title2 = st.columns([1, 3])
        with col_title1:
            titulares = expo['Titular'].dropna().unique().tolist()
            titulares.sort()
            search_name = st.selectbox("Buscar por nombre de titular", options=["(Todos)"] + titulares)
            if search_name and search_name != "(Todos)":
                expo = expo[expo['Titular'] == search_name]
    with col_logo:
        st.image('logo_ypf.png')
    with col_simpa:
        st.image('logo_liftvan.png')
    
    abiertos = expo[expo['Estado'] == 'Abierto'][['Titular', 'Coordinador', 'Tipo','Origen', 'Destino', 'Fecha Apertura', 'Fecha Embalaje']]
    embalados = expo[expo['Estado'] == 'Embalado'][['Titular', 'Coordinador', 'Tipo','Origen', 'Destino', 'Fecha Embalaje', 'Fecha Verificacion']]
    en_deposito = expo[expo['Estado'] == 'En deposito'][['Titular', 'Coordinador','Tipo', 'Origen', 'Destino', 'Fecha Fiscal', 'ETD']]
    finalizados = expo[expo['Estado'] == 'Finalizado'][['Titular', 'Coordinador', 'Tipo','Origen', 'Destino', 'ETD',  'Fecha Llegada']]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Abiertos")
        st.dataframe(abiertos,
                     hide_index=True, use_container_width=True)
    with col2:
        st.subheader("Embalados")
        st.dataframe(embalados,
                    hide_index=True, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("En tránsito")
        st.dataframe(en_deposito,
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Finalizados")
        st.dataframe(finalizados,
                    hide_index=True, use_container_width=True)

# Run the show_page function
if __name__ == "__main__":
    while True:
        show_page_expo()
        time.sleep(60)  
        st.experimental_rerun()

