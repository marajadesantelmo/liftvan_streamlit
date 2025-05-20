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
    with col_logo:
        st.image('logo_ypf.png')
    with col_simpa:
        st.image('logo_liftvan.png')
    col1, col2 = st.columns(2)
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Abiertos")
        st.dataframe(impo[impo['Estado'] =='Abierto'],
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Arribados")
        st.dataframe(impo[impo['Estado'] == 'Arribado'],
                    hide_index=True, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("En deposito")
        st.dataframe(impo[impo['Estado'] == 'En deposito'],
                     hide_index=True, use_container_width=True)
    with col5:
        st.subheader("Finalizados")
        st.dataframe(impo[impo['Estado'] == 'Finalizado'],
                    hide_index=True, use_container_width=True)
# Run the show_page function
if __name__ == "__main__":
    while True:
        show_page_impo()
        time.sleep(60)  
        st.experimental_rerun()

