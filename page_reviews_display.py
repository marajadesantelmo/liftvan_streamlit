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
        st.markdown(f"**Usuario:** {row.get('username', 'anonimo')}")
        st.markdown(f"**Fecha:** {row.get('created_at', '')[:19]}")
        st.markdown(f"**Recomendaría:** {'Sí' if row.get('recomendaria') else 'No'}")
        st.markdown(f"**Comentarios:** {row.get('comentarios', '')}")
        st.markdown("**Puntajes:**")
        st.write({
            "Asistencia del Estimador": row.get("asistencia_estimador"),
            "COORDINADOR DE TRAFICO": row.get("coordinador_trafico"),
            "Cortesía del coordinador": row.get("cortesia_coordinador"),
            "Apoyo del coordinador": row.get("apoyo_coordinador"),
            "Precisión de la información": row.get("precision_informacion"),
            "Servicio General del coordinador": row.get("servicio_general_coordinador"),
            "EMBALADORES": row.get("embaladores"),
            "Cortesía": row.get("cortesia"),
            "Colaboración del personal": row.get("colaboracion_personal"),
            "Puntualidad": row.get("puntualidad"),
            "Calidad del empaque/desempaque": row.get("calidad_empaque"),
        })

def main():
    show_page_reviews_display()

if __name__ == "__main__":
    main()
