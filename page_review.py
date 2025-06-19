import streamlit as st
from supabase_connection import insert_review
import datetime

def show_page_review(username):
    st.header("Dejanos tu review sobre el servicio de mudanza")
    col1nombre, col2puesto = st.columns(2)
    with col1nombre:
        nombre_apellido = st.text_input("Nombre y Apellido")

    # Require username before proceeding
    if not nombre_apellido  or nombre_apellido.strip() == "":
        st.warning("Debes ingresar tu usuario antes de dejar una review.")
        return

    def star_input(label, key=None):
        return st.slider(label, 1, 5, 5, format="%d ⭐", key=key)

    # Two columns for Coordinador and Embaladores
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Coordinador de Tráfico")
        col1a, col1b = st.columns([7, 1])
        with col1a:
            cortesia_coordinador = star_input("Cortesía del coordinador", key="cortesia_coordinador")
            apoyo_coordinador = star_input("Apoyo del coordinador", key="apoyo_coordinador")
            precision_informacion = star_input("Precisión de la información", key="precision_informacion")
            servicio_general_coordinador = star_input("Servicio General del coordinador", key="servicio_general_coordinador")

    with col2:
        st.subheader("Embaladores")
        col2a, col2b = st.columns([7, 1])
        with col2a:
            cortesia = star_input("Cortesía", key="cortesia")
            colaboracion_personal = star_input("Colaboración del personal", key="colaboracion_personal")
            puntualidad = star_input("Puntualidad", key="puntualidad")
            calidad_empaque = star_input("Calidad del empaque/desempaque", key="calidad_empaque")

    col3, col4 = st.columns(2)
    with col3:
        recomendaria = st.radio("¿Recomendaría nuestros servicios?", ["Sí", "No"])
        comentarios = st.text_area("Comentarios")
    with col4:
        col4a, col4b = st.columns([7, 1])
        with col4a:
            st.subheader("Estimador")
            asistencia_estimador = star_input("Asistencia del Estimador", key="asistencia_estimador")


    review = {
        "username": username,
        "nombre_apellido": nombre_apellido,
        "asistencia_estimador": asistencia_estimador,
        "cortesia_coordinador": cortesia_coordinador,
        "apoyo_coordinador": apoyo_coordinador,
        "precision_informacion": precision_informacion,
        "servicio_general_coordinador": servicio_general_coordinador,
        "cortesia": cortesia,
        "colaboracion_personal": colaboracion_personal,
        "puntualidad": puntualidad,
        "calidad_empaque": calidad_empaque,
        "recomendaria": recomendaria == "Sí",
        "comentarios": comentarios,
        "created_at": datetime.datetime.now().isoformat()
    }

    if st.button("Enviar Review"):
        try:
            resp = insert_review(review)
            # Success if data is returned and not empty
            if hasattr(resp, "data") and resp.data:
                st.success("¡Gracias por tu Review!")
            elif hasattr(resp, "error") and resp.error:
                st.error(f"Error al guardar la review: {resp.error}")
            else:
                st.error(f"Error desconocido: {resp}")
        except Exception as e:
            st.error(f"Excepción al guardar la review: {e}")

def main():
    import streamlit as st
    username = st.session_state.get("username", "anonimo")
    show_page_review(username)

if __name__ == "__main__":
    main()
