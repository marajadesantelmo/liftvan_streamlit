import streamlit as st
from supabase_connection import insert_review
import datetime

def show_page_review(username):
    st.header("Dejanos tu opinión sobre el servicio de mudanza")

    def star_input(label):
        return st.slider(label, 1, 5, 3, format="%d ⭐")

    review = {
        "username": username,
        "asistencia_estimador": star_input("Asistencia del Estimador"),
        "coordinador_trafico": star_input("COORDINADOR DE TRAFICO"),
        "cortesia_coordinador": star_input("Cortesía del coordinador"),
        "apoyo_coordinador": star_input("Apoyo del coordinador"),
        "precision_informacion": star_input("Precisión de la información"),
        "servicio_general_coordinador": star_input("Servicio General del coordinador"),
        "embaladores": star_input("EMBALADORES"),
        "cortesia": star_input("Cortesía"),
        "colaboracion_personal": star_input("Colaboración del personal"),
        "puntualidad": star_input("Puntualidad"),
        "calidad_empaque": star_input("Calidad del empaque/desempaque"),
        "recomendaria": st.radio("¿Recomendaría nuestros servicios?", ["Sí", "No"]) == "Sí",
        "comentarios": st.text_area("Comentarios"),
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
