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

    # Promedios de cada categoría
    # Definir columnas por grupo
    coordinador_columns = [
        "cortesia_coordinador",
        "apoyo_coordinador",
        "precision_informacion",
        "servicio_general_coordinador"
    ]
    embaladores_columns = [
        "cortesia",
        "colaboracion_personal",
        "puntualidad",
        "calidad_empaque"
    ]
    estimador_column = "asistencia_estimador"

    # Calcular promedios por categoría
    avg_scores = {
        "Coordinador": reviews[coordinador_columns].mean(axis=1).mean().round(2),
        "Embaladores": reviews[embaladores_columns].mean(axis=1).mean().round(2),
        "Estimador": reviews[estimador_column].mean().round(2)
    }

    # Preparar datos para gráfico de barras agrupado
    avg_scores_by_cat = pd.DataFrame({
        "Categoría": ["Cortesía Coord.", "Apoyo Coord.", "Precisión Info.", "Serv. Gral. Coord.",
                      "Cortesía Emb.", "Colab. Emb.", "Puntualidad", "Calidad Empaque"],
        "Grupo": ["Coordinador"] * 4 + ["Embaladores"] * 4,
        "Promedio": reviews[coordinador_columns + embaladores_columns].mean().round(2).values
    })

    fig = px.bar(
        avg_scores_by_cat,
        x="Categoría",
        y="Promedio",
        color="Grupo",
        barmode="group",
        title="Promedio de Puntajes por Grupo y Categoría",
        color_discrete_map={"Coordinador": "#4F8DFD", "Embaladores": "#7ED957"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabla de promedios por grupo
    st.markdown("**Promedio general por grupo:**")
    st.table(pd.DataFrame({
        "Grupo": ["Estimador", "Coordinador", "Embaladores"],
        "Promedio": [avg_scores["Estimador"], avg_scores["Coordinador"], avg_scores["Embaladores"]]
    }).set_index("Grupo"))

    # Porcentaje de recomendación
    rec_rate = reviews["recomendaria"].mean() * 100
    st.metric("Recomendaría el servicio (%)", f"{rec_rate:.1f}%")

    # Distribución de puntajes (histograma)
    st.subheader("Distribución de Puntajes")
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
    # Formatear fecha y recomendación
    df = reviews[compact_cols].copy()
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
    df["recomendaria"] = df["recomendaria"].map({True: "Sí", False: "No"})

    # Mostrar tabla compacta
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
