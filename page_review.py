import streamlit as st
from supabase_connection import insert_review
import datetime

def show_page_review(username):
    st.header("Dejanos tu opinión sobre el servicio de mudanza")

    def star_input(label, key=None):
        return st.slider(label, 1, 5, 3, format="%d ⭐", key=key)

    # Asistencia del Estimador (above columns)
    asistencia_estimador = star_input("Asistencia del Estimador", key="asistencia_estimador")

    # Two columns for Coordinador and Embaladores
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("COORDINADOR DE TRAFICO")
        cortesia_coordinador = star_input("Cortesía del coordinador", key="cortesia_coordinador")
        apoyo_coordinador = star_input("Apoyo del coordinador", key="apoyo_coordinador")
        precision_informacion = star_input("Precisión de la información", key="precision_informacion")
        servicio_general_coordinador = star_input("Servicio General del coordinador", key="servicio_general_coordinador")

    with col2:
        st.subheader("EMBALADORES")
        cortesia = star_input("Cortesía", key="cortesia")
        colaboracion_personal = star_input("Colaboración del personal", key="colaboracion_personal")
        puntualidad = star_input("Puntualidad", key="puntualidad")
        calidad_empaque = star_input("Calidad del empaque/desempaque", key="calidad_empaque")

    recomendaria = st.radio("¿Recomendaría nuestros servicios?", ["Sí", "No"])
    comentarios = st.text_area("Comentarios")

    review = {
        "username": username,
        "asistencia_estimador": asistencia_estimador,
        "cortesia_coordinador": cortesia_coordinador,
        "apoyo_coordinador": apoyo_coordinador,
        "precision_informacion": precision_informacion,
        "servicio_general_coordinador": servicio_general_coordinador,
        "embaladores": 5,  # You can remove or adjust this field if not needed
        "cortesia": cortesia,
        "colaboracion_personal": colaboracion_personal,
        "puntualidad": puntualidad,
        "calidad_empaque": calidad_empaque,
        "recomendaria": recomendaria == "Sí",
        "comentarios": comentarios,
        "created_at": datetime.datetime.now().isoformat()
    }

    if st.button("Enviar opinión"):
        resp = insert_review(review)
        if hasattr(resp, "status_code") and resp.status_code == 201:
            st.success("¡Gracias por tu opinión!")
        else:
            st.error("Hubo un error al guardar tu opinión. Intenta nuevamente.")

def main():
    import streamlit as st
    username = st.session_state.get("username", "anonimo")
    show_page_review(username)

if __name__ == "__main__":
    main()
