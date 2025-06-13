import streamlit as st
import pandas as pd
import page_review

def show_cliente_page(username, cookies):
    # Try to find the user in expo.csv or impo.csv
    first_name = username.capitalize()
    df_expo = pd.read_csv('expo.csv')
    df_impo = pd.read_csv('impo.csv')
    # Find rows where the first name matches
    row_expo = df_expo[df_expo['Titular'].str.split().str[0].str.lower() == username]
    row_impo = df_impo[df_impo['Titular'].str.split().str[0].str.lower() == username]

    st.header('Bienvenido/a, ' + first_name)
    if not row_expo.empty:
        st.subheader('Operación de Exportación')
        st.dataframe(row_expo, hide_index=True, use_container_width=True)
    if not row_impo.empty:
        st.subheader('Operación de Importación')
        st.dataframe(row_impo, hide_index=True, use_container_width=True)
    if row_expo.empty and row_impo.empty:
        st.warning('No se encontró información de operación para este usuario.')
    st.markdown('---')
    st.subheader('Dejanos tu review sobre el servicio')
    page_review.show_page_review(username)

    # Logout button for customers
    if st.button('Logout'):
        cookies.pop("logged_in", None)
        cookies.pop("username", None)
        cookies.save()
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
