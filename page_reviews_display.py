import streamlit as st
from supabase_connection import fetch_reviews
import pandas as pd
import plotly.express as px

def show_page_reviews_display():
    st.header("Estadísticas de Reviews de Mudanzas")

    reviews = fetch_reviews()
    if reviews.empty:
        st.info("Aún no hay opiniones registradas.")
        return

    # --- Estadísticas ---
    st.subheader("Resumen de Puntajes y Recomendaciones")

    # Agrupar promedios por grupo
    scores_embaladores = [
        "cortesia", "colaboracion_personal", "puntualidad", "calidad_empaque"
    ]
    scores_coordinador = [
        "cortesia_coordinador", "apoyo_coordinador", "precision_informacion", "servicio_general_coordinador"
    ]
    scores_estimador = ["asistencia_estimador"]

    avg_embaladores = reviews[scores_embaladores].mean().mean().round(2)
    avg_coordinador = reviews[scores_coordinador].mean().mean().round(2)
    avg_estimador = reviews[scores_estimador].mean().mean().round(2)

    avg_grouped = pd.DataFrame({
        "Grupo": ["Embaladores", "Coordinador de Tráfico", "Estimador"],
        "Promedio": [avg_embaladores, avg_coordinador, avg_estimador]
    })

    fig_grouped = px.bar(
        avg_grouped,
        x="Grupo",
        y="Promedio",
        color="Grupo",
        text="Promedio",
        title="Promedio de Puntajes por Grupo"
    )
    fig_grouped.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_grouped.update_layout(yaxis=dict(range=[0, 5]), showlegend=False)
    st.plotly_chart(fig_grouped, use_container_width=True)

    # Porcentaje de recomendación
    rec_rate = reviews["recomendaria"].mean() * 100
    st.metric("Recomendaría el servicio (%)", f"{rec_rate:.1f}%")

    # Distribución de puntajes (histograma)
    st.subheader("Distribución de Puntajes")
    score_columns = scores_estimador + scores_coordinador + scores_embaladores
    hist_data = reviews.melt(value_vars=score_columns, var_name="Categoría", value_name="Puntaje")
    fig_hist = px.histogram(hist_data, x="Puntaje", color="Categoría", barmode="group", nbins=5)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("Reseñas Recientes")

    # --- Tabla compacta de reviews ---
    compact_cols = [
        "created_at", "nombre_apellido", "puesto", "asistencia_estimador",
        "cortesia_coordinador", "apoyo_coordinador", "precision_informacion",
        "servicio_general_coordinador", "cortesia", "colaboracion_personal",
        "puntualidad", "calidad_empaque", "recomendaria", "comentarios"
    ]
    df = reviews[compact_cols].copy()
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
    df["recomendaria"] = df["recomendaria"].map({True: "Sí", False: "No"})

    st.dataframe(
        df.rename(columns={
            "created_at": "Fecha",
            "nombre_apellido": "Nombre y Apellido",
            "puesto": "Puesto",
            "asistencia_estimador": "Estimador",
            "cortesia_coordinador": "Cortesía Coord.",
            "apoyo_coordinador": "Apoyo Coord.",
            "precision_informacion": "Precisión Info.",
            "servicio_general_coordinador": "Serv. Gral. Coord.",
            "cortesia": "Cortesía Emb.",
            "colaboracion_personal": "Colab. Emb.",
            "puntualidad": "Puntualidad",
            "calidad_empaque": "Calidad Empaque",
            "recomendaria": "¿Recomienda?",
            "comentarios": "Comentarios"
        }),
        hide_index=True,
        use_container_width=True,
        height=400
    )

def main():
    show_page_reviews_display()

if __name__ == "__main__":
    main()
