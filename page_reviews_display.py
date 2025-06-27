import streamlit as st
from supabase_connection import fetch_reviews
import pandas as pd
import plotly.express as px

def show_page_reviews_display():
    st.header("Estadísticas de Reviews de Mudanzas")

    reviews = fetch_reviews()

    col1, col2 = st.columns([7, 1])
    with col1:
        st.info("Resumen de puntajes y recomendaciones dejadas por los usuarios")
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

    avg_scores = {
        "Coordinador": reviews[coordinador_columns].mean(axis=1).mean().round(2),
        "Embaladores": reviews[embaladores_columns].mean(axis=1).mean().round(2),
        "Estimador": reviews[estimador_column].mean().round(2)
    }
    col1b, col2b = st.columns([3, 5])
    with col1b:
        col1b1, col1b2 = st.columns([3, 1])
        with col1b1:
            st.subheader("Promedio general por grupo")
            st.table(pd.DataFrame({
            "Grupo": ["Estimador", "Coordinador", "Embaladores"],
            "Promedio": [avg_scores["Estimador"], avg_scores["Coordinador"], avg_scores["Embaladores"]]
        }).set_index("Grupo"))
            

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
            textfont_size=22,
            textfont_color='white'  # Make values white for better contrast
        )
        fig_pie.update_layout(
            width=400,
            height=400,
            showlegend=False,  # Remove legend
            title_font_size=28,  # Bigger title
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2b:
        avg_scores_by_cat = pd.DataFrame({
            "Categoría": ["Cortesía Coord.", "Apoyo Coord.", "Precisión Info.", "Serv. Gral. Coord.",
                        "Cortesía Emb.", "Colab. Emb.", "Puntualidad", "Calidad Empaque"],
            "Grupo": ["Coordinador"] * 4 + ["Embaladores"] * 4,
            "Promedio": reviews[coordinador_columns + embaladores_columns].mean().round(2).values    })

        score_columns = [estimador_column] + coordinador_columns + embaladores_columns

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
        avg_by_cat = reviews[score_columns].mean().round(1).reset_index()
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
        fig_barh.update_layout(
            yaxis_title="", xaxis_title="Promedio",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_size=28  # Bigger title
        )
        st.plotly_chart(fig_barh, use_container_width=True)

    st.markdown("---")
    st.subheader("Dealles de Reviews")

    compact_cols = [
        "created_at", "nombre_apellido", "puesto", "asistencia_estimador",
        "cortesia_coordinador", "apoyo_coordinador", "precision_informacion",
        "servicio_general_coordinador", "cortesia", "colaboracion_personal",
        "puntualidad", "calidad_empaque", "recomendaria", "comentarios"
    ]
    # Filtros y buscador
    with st.expander("Filtrar y buscar reviews"):
        col_f1, col_f2, col_f3 = st.columns([2, 2, 4])
        with col_f1:
            recomendar_filter = st.selectbox(
                "¿Recomienda?",
                options=["Todos", "Sí", "No"],
                index=0
            )
        with col_f2:
            fecha_min = reviews["created_at"].min()
            fecha_max = reviews["created_at"].max()
            fecha_range = st.date_input(
                "Rango de fechas",
                value=(pd.to_datetime(fecha_min), pd.to_datetime(fecha_max)),
                min_value=pd.to_datetime(fecha_min),
                max_value=pd.to_datetime(fecha_max)
            )
        with col_f3:
            search_text = st.text_input("Buscar por nombre o comentario")

    df = reviews[compact_cols].copy()
    df = df.drop(columns=["puesto"], errors='ignore')
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["recomendaria"] = df["recomendaria"].map({True: "Sí", False: "No"})

    # Aplicar filtros
    if recomendar_filter != "Todos":
        df = df[df["recomendaria"] == recomendar_filter]
    if isinstance(fecha_range, tuple) and len(fecha_range) == 2:
        start, end = pd.to_datetime(fecha_range[0]), pd.to_datetime(fecha_range[1])
        df = df[(df["created_at"] >= start) & (df["created_at"] <= end + pd.Timedelta(days=1))]
    if search_text:
        mask = (
            df["nombre_apellido"].str.contains(search_text, case=False, na=False) |
            df["comentarios"].str.contains(search_text, case=False, na=False)
        )
        df = df[mask]

    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M")

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
