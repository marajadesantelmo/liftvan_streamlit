import streamlit as st
st.set_page_config(page_title="Seguimiento de mudanzas YPF - Liftvan", 
                   page_icon="📊", 
                   layout="wide")

import page_expo
import page_impo
import page_review
import page_reviews_display
import page_nacionales
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager
import os
import csv

# Page configurations


# Estilo
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_users():
    users = {}
    with open('users.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if ':' in line:
                    user, pwd = line.split(':', 1)
                    users[user.strip()] = pwd.strip()
    return users

USERS = load_users()

# Update login to check users.txt

def login(username, password):
    return USERS.get(username) == password

# Initialize cookies manager
cookies = EncryptedCookieManager(prefix="dassa_", password="your_secret_password")

if not cookies.ready():
    st.stop()

# Check if user is already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = cookies.get("logged_in", False)
if 'username' not in st.session_state:
    st.session_state.username = cookies.get("username", "")

if not st.session_state['logged_in']:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
            st.session_state.username = username
            cookies["logged_in"] = str(True)  # Convert to string
            cookies["username"] = username  # Username is already a string
            cookies.save()  # Persist the changes
            st.success("Usuario logeado")
            st.rerun()
        else:
            st.error("Usuario o clave invalidos")
else:
    # If user is employee, show full menu. If customer, show only their page.
    employee_users = ["operativo", "administrativo"]
    username = st.session_state.get("username", "")
    if username in employee_users:
        pages = [
            "Importación", 
            "Exportación", 
            "Nacionales", 
            "Ver Reviews", 
            "Logout"
        ]
        icons = [
            "arrow-down-circle", 
            "arrow-up-circle", 
            "clock-history", 
            "chat-dots", 
            "box-arrow-right"
        ]

        page_selection = option_menu(
                None,  # No menu title
                pages,  
                icons=icons,
                menu_icon="cast",  
                default_index=0, 
                orientation="horizontal")
        if page_selection == "Importación":
            page_impo.show_page_impo()
        elif page_selection == "Exportación":
            page_expo.show_page_expo()
        elif page_selection == "Nacionales":
            page_nacionales.show_page_nacionales()
        elif page_selection == "Agregar Review":
            page_review.show_page_review(st.session_state.get("username", "anonimo"))
        elif page_selection == "Ver Reviews":
            page_reviews_display.show_page_reviews_display()
        elif page_selection == "Logout":
            cookies.pop("logged_in", None)
            cookies.pop("username", None)
            cookies.save()
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.rerun()
    else:
        import page_cliente
        page_cliente.show_cliente_page(username, cookies)


