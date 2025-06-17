import streamlit as st
import pandas as pd
import page_review
from PIL import Image

def show_cliente_page(username, cookies):
    # Try to find the user in expo.csv or impo.csv
    first_name = username.capitalize()
    df_expo = pd.read_csv('expo.csv')
    # Select relevant columns for expo
    expo_columns = ['Titular', 'Domicilio', 'Localidad', 'Coordinador',
                    'Origen', 'Destino', 'Fecha Embalaje', 'Fecha Fiscal', 'Estado']
    df_expo = df_expo[expo_columns]

    # Load and select relevant columns for impo
    df_impo = pd.read_csv('impo.csv')
    impo_columns = ['Titular', 'Domicilio', 'Localidad', 'Coordinador',
                    'Origen', 'Destino', 'Fecha Apertura', 'Fecha Arribo', 'Fecha Fiscal', 'Estado']
    df_impo = df_impo[impo_columns]
    # Find rows where the first name matches
    row_expo = df_expo[df_expo['Titular'].str.split().str[0].str.lower() == username]
    row_impo = df_impo[df_impo['Titular'].str.split().str[0].str.lower() == username]

    st.header('Bienvenido/a, ' + first_name)
    if not row_expo.empty:
        cola, colb, colc, cold = st.columns([5, 1, 1, 1])
        with cola: 
                st.subheader('Operación de Exportación')
        with colb:
            st.image("logo_ypf.png", width=80)
        with colc:
            st.image("logo_liftvan.png", width=80)
        with cold:
            st.write("")  # Spacer
            if st.button("Logout", key="logout_btn_expo"):
                cookies["logged_in"] = str(False)
                cookies["username"] = ""
                cookies.save()
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.rerun()
        estado = row_expo['Estado'].values[0]
        col1, col2 = st.columns([1, 3])
        with col1:
            st.info(f"Estado de la operación: {estado}")
        st.dataframe(row_expo, hide_index=True, use_container_width=True)
    if not row_impo.empty:
        cola, colb, colc, cold = st.columns([5, 1, 1, 1])
        with cola: 
            st.subheader('Operación de Importación')
        with colb:
            st.image("logo_ypf.png", width=80)
        with colc:
            st.image("logo_liftvan.png", width=80)
        with cold:
            st.write("")
            if st.button("Logout", key="logout_btn_impo"):
                cookies["logged_in"] = str(False)
                cookies["username"] = ""
                cookies.save()
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.rerun()

        estado = row_impo['Estado'].values[0]
        col1, col2 = st.columns([1, 3])
        with col1:
            st.info(f"Estado: {estado}")
        st.info(f"Estado de la operación: {estado}")
    if row_expo.empty and row_impo.empty:
        st.warning('No se encontró información de operación para este usuario.')


    col1, col2 = st.columns(2)
    with col1:
        st.image("foto1.png", caption="Contenedor", use_column_width=True)
        st.image("foto3.png", caption="Estado de la carga", use_column_width=True)
    with col2:
        st.image("foto2.png", caption="Precinto", use_column_width=True)
        st.image("foto4.png", caption="Carga en depósito", use_column_width=True)
    st.markdown('---')
    page_review.show_page_review(username)
