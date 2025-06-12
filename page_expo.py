import streamlit as st
import pandas as pd
import time
from datetime import datetime

def show_page_expo():
    # Load data
    expo = pd.read_csv('expo.csv')

    # Add a filter to search by name
    search_name = st.text_input("Buscar por nombre de titular")
    if search_name:
        expo = expo[expo['Titular'].str.contains(search_name, case=False, na=False)]

    abiertos = expo[expo['Estado'] == 'Abierto'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Apertura', 'Fecha Embalaje']]
    embalados = expo[expo['Estado'] == 'Embalado'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Embalaje', 'Fecha Fiscal']]
    en_deposito = expo[expo['Estado'] == 'En deposito'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Fiscal', 'Fecha Salida']]
    finalizados = expo[expo['Estado'] == 'Finalizado'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Salida',  'Fecha Llegada']]

    col_title, col_logo, col_simpa = st.columns([5, 1, 1])
    with col_title:
        st.header(f"Estado de mudanzas de EXPO")
    with col_logo:
        st.image('logo_ypf.png')
    with col_simpa:
        st.image('logo_liftvan.png')
    col1, col2 = st.columns(2)
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Abiertos")
        st.dataframe(abiertos,
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Embalados")
        st.dataframe(embalados,
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

# Run the show_page function
if __name__ == "__main__":
    while True:
        show_page_expo()
        time.sleep(60)  
        st.experimental_rerun()

