import streamlit as st
from supabase_connection import fetch_reviews
import pandas as pd
import plotly.express as px

def show_page_reviews_display():
    st.header("Estadísticas de Reviews de Mudanzas")

    reviews = fetch_reviews()

    col1, col2 = st.columns([7, 1])
    with col1:
        st.subheader("Resumen de Puntajes y Recomendaciones")
    with col2:
        rec_rate = reviews["recomendaria"].mean() * 100
        st.metric("Recomendaría el servicio (%)", f"{rec_rate:.1f}%")

    
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
    col1b, col2b = st.columns([3, 5])
    with col1b:
        st.markdown("**Promedio general por grupo:**")
        st.table(pd.DataFrame({
        "Grupo": ["Estimador", "Coordinador", "Embaladores"],
        "Promedio": [avg_scores["Estimador"], avg_scores["Coordinador"], avg_scores["Embaladores"]]
    }).set_index("Grupo"))
        # Pie chart for "Recomendaría / No recomendaría"
        rec_counts = reviews["recomendaria"].value_counts().rename({True: "Sí", False: "No"})
        fig_pie = px.pie(
            names=rec_counts.index,
            values=rec_counts.values,
            title="¿Recomendaría el servicio?",
            color=rec_counts.index,
            color_discrete_map={"Sí": "#4F8DFD", "No": "#FF6961"}
        )
        fig_pie.update_traces(
            textinfo='percent+label',
            textfont_size=22  # Bigger values font
        )
        fig_pie.update_layout(
            width=200,  # Half smaller (default is 400)
            height=200,
            legend=dict(
            font=dict(size=20)  # Bigger legend font
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2b:
        avg_scores_by_cat = pd.DataFrame({
            "Categoría": ["Cortesía Coord.", "Apoyo Coord.", "Precisión Info.", "Serv. Gral. Coord.",
                        "Cortesía Emb.", "Colab. Emb.", "Puntualidad", "Calidad Empaque"],
            "Grupo": ["Coordinador"] * 4 + ["Embaladores"] * 4,
            "Promedio": reviews[coordinador_columns + embaladores_columns].mean().round(2).values    })
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

    # Definir score_columns para el histograma
    score_columns = [estimador_column] + coordinador_columns + embaladores_columns

    # --- Promedio por Categoría (Barra Horizontal) ---
    st.subheader("Promedio por Categoría")
    # Mapeo de nombres a formato título
    categoria_map = {
        "asistencia_estimador": "Asistencia Estimador",
        "cortesia_coordinador": "Cortesía Coordinador",
        "apoyo_coordinador": "Apoyo Coordinador",
        "precision_informacion": "Precisión Información",
        "servicio_general_coordinador": "Servicio General Coordinador",
        "cortesia": "Cortesía Embaladores",
        "colaboracion_personal": "Colaboración Personal",
        "puntualidad": "Puntualidad",
        "calidad_empaque": "Calidad Empaque"
    }
    avg_by_cat = reviews[score_columns].mean().reset_index()
    avg_by_cat.columns = ["Categoría", "Promedio"]
    avg_by_cat["Categoría"] = avg_by_cat["Categoría"].map(categoria_map)
    fig_barh = px.bar(
        avg_by_cat,
        y="Categoría",
        x="Promedio",
        orientation="h",
        title="Promedio por Categoría",
        text="Promedio",
        color="Promedio",
        color_continuous_scale="Blues"
    )
    fig_barh.update_layout(yaxis_title="", xaxis_title="Promedio")
    st.plotly_chart(fig_barh, use_container_width=True)

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
    df = df.drop(columns=["puesto"], errors='ignore') 
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
    df["recomendaria"] = df["recomendaria"].map({True: "Sí", False: "No"})

    # Mostrar tabla compacta
    st.dataframe(
        df.rename(columns={
            "created_at": "Fecha",
            "nombre_apellido": "Nombre y Apellido",
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
