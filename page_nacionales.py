import streamlit as st
import pandas as pd

def show_page_nacionales():
    # Hardcoded sample data for demonstration
    nacionales = pd.read_csv('nacionales.csv')
    abiertos = nacionales[nacionales['Estado'] == 'Abierto'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Apertura', 'Fecha Embalaje']]
    embalados = nacionales[nacionales['Estado'] == 'Embalado'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Embalaje', 'Fecha Fiscal']]
    en_deposito = nacionales[nacionales['Estado'] == 'En deposito'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Fiscal', 'Fecha Salida']]
    finalizados = nacionales[nacionales['Estado'] == 'Finalizado'][['Titular', 'Domicilio', 'Localidad', 'Coordinador',
        'Origen', 'Destino', 'Fecha Salida',  'Fecha Llegada']]

    col_title, col_logo, col_simpa = st.columns([5, 1, 1])
    with col_title:
        st.header(f"Estado de mudanzas nacionales")
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

