import streamlit as st
from supabase_connection import insert_review
import datetime

def show_page_review(username):
    st.header("Dejanos tu opinión sobre el servicio de mudanza")
    col1nombre, col2puesto = st.columns(2)
    with col1nombre:
        nombre_apellido = st.text_input("Nombre y Apellido")
    with col2puesto:
        puesto = st.text_input("Puesto")

    def star_input(label, key=None):
        return st.slider(label, 1, 5, 3, format="%d ⭐", key=key)

    # Asistencia del Estimador (above columns)
    asistencia_estimador = star_input("Asistencia del Estimador", key="asistencia_estimador")

    # Two columns for Coordinador and Embaladores
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Coordinador de Tráfico")
        cortesia_coordinador = star_input("Cortesía del coordinador", key="cortesia_coordinador")
        apoyo_coordinador = star_input("Apoyo del coordinador", key="apoyo_coordinador")
        precision_informacion = star_input("Precisión de la información", key="precision_informacion")
        servicio_general_coordinador = star_input("Servicio General del coordinador", key="servicio_general_coordinador")

    with col2:
        st.subheader("Embaladores")
        cortesia = star_input("Cortesía", key="cortesia")
        colaboracion_personal = star_input("Colaboración del personal", key="colaboracion_personal")
        puntualidad = star_input("Puntualidad", key="puntualidad")
        calidad_empaque = star_input("Calidad del empaque/desempaque", key="calidad_empaque")

    recomendaria = st.radio("¿Recomendaría nuestros servicios?", ["Sí", "No"])
    comentarios = st.text_area("Comentarios")

    review = {
        "username": username,
        "nombre_apellido": nombre_apellido,
        "puesto": puesto,
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

    if st.button("Enviar opinión"):
        try:
            resp = insert_review(review)
            # Success if data is returned and not empty
            if hasattr(resp, "data") and resp.data:
                st.success("¡Gracias por tu opinión!")
            elif hasattr(resp, "error") and resp.error:
                st.error(f"Error al guardar la opinión: {resp.error}")
            else:
                st.error(f"Error desconocido: {resp}")
        except Exception as e:
            st.error(f"Excepción al guardar la opinión: {e}")

def main():
    import streamlit as st
    username = st.session_state.get("username", "anonimo")
    show_page_review(username)

if __name__ == "__main__":
    main()
