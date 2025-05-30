import streamlit as st
from supabase_connection import fetch_reviews

def show_page_reviews_display():
    st.header("Opiniones de usuarios sobre el servicio de mudanza")
    reviews = fetch_reviews()
    if reviews.empty:
        st.info("Aún no hay opiniones registradas.")
        return

    for _, row in reviews.iterrows():
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Nombre y Apellido:** {row.get('nombre_apellido', '')}")
            st.markdown(f"**Puesto:** {row.get('puesto', '')}")
            st.markdown(f"**Fecha:** {row.get('created_at', '')[:19]}")
            st.markdown(f"**Recomendaría:** {'Sí' if row.get('recomendaria') else 'No'}")
            st.markdown(f"**Comentarios:** {row.get('comentarios', '')}")
            st.markdown(f"*Asistencia del Estimador*: {row.get('asistencia_estimador', 'N/A')}")

        with col2:
            st.markdown("**Coordinador de Tráfico**")
            st.write({
                "Cortesía del coordinador": row.get("cortesia_coordinador"),
                "Apoyo del coordinador": row.get("apoyo_coordinador"),
                "Precisión de la información": row.get("precision_informacion"),
                "Servicio General del coordinador": row.get("servicio_general_coordinador"),
            })
            st.markdown("**Embaladores**")
            st.write({
                "Cortesía": row.get("cortesia"),
                "Colaboración del personal": row.get("colaboracion_personal"),
                "Puntualidad": row.get("puntualidad"),
                "Calidad del empaque/desempaque": row.get("calidad_empaque"),
            })

def main():
    show_page_reviews_display()

if __name__ == "__main__":
    main()
