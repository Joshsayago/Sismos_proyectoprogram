import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Proyecto de Sismos en el Perú")
st.write("Análisis del catálogo sísmico del IGP")

# 1. Carga de datos y limpieza inicial única
df = pd.read_csv("sismos.csv", sep=";") 

# Creamos la columna AÑO una sola vez aquí arriba para optimizar rendimiento
df["AÑO"] = df["FECHA_UTC"].astype(str).str[:4].astype(int)

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric("Total sismos", len(df))
col2.metric("Magnitud máxima", df["MAGNITUD"].max())
col3.metric("Profundidad máxima", df["PROFUNDIDAD"].max())

st.subheader("📊 Análisis interactivo")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Décadas",
    "📊 Magnitud",
    "🌋 Profundidad",
    "🎯 Escala Richter",
    "🗺️ Mapa",
    "🔍 Relación de Variables",
    "📝 Conclusiones"
])

# --- TAB 1: DÉCADAS ---
with tab1:
    st.subheader("Sismos por década")

    decadas = {
        "1960-69": ((df["AÑO"] >= 1960) & (df["AÑO"] <= 1969)).sum(),
        "1970-79": ((df["AÑO"] >= 1970) & (df["AÑO"] <= 1979)).sum(),
        "1980-89": ((df["AÑO"] >= 1980) & (df["AÑO"] <= 1989)).sum(),
        "1990-99": ((df["AÑO"] >= 1990) & (df["AÑO"] <= 1999)).sum(),
        "2000-09": ((df["AÑO"] >= 2000) & (df["AÑO"] <= 2009)).sum(),
        "2010-19": ((df["AÑO"] >= 2010) & (df["AÑO"] <= 2019)).sum(),
        "2020-25": ((df["AÑO"] >= 2020) & (df["AÑO"] <= 2025)).sum(),
    }

    fig, ax = plt.subplots()
    ax.bar(decadas.keys(), decadas.values(), color="#c68642", edgecolor="black")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig) # Cerramos la figura para liberar memoria

# --- TAB 2: MAGNITUD ---
with tab2:
    st.subheader("Magnitud de sismos")

    decada = st.selectbox(
        "Selecciona década",
        ["Todas", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    )

    # Añadido .copy() para evitar SettingWithCopyWarning
    if decada == "Todas":
        dff = df.copy()
    elif decada == "1960s":
        dff = df[(df["AÑO"] >= 1960) & (df["AÑO"] <= 1969)].copy()
    elif decada == "1970s":
        dff = df[(df["AÑO"] >= 1970) & (df["AÑO"] <= 1979)].copy()
    elif decada == "1980s":
        dff = df[(df["AÑO"] >= 1980) & (df["AÑO"] <= 1989)].copy()
    elif decada == "1990s":
        dff = df[(df["AÑO"] >= 1990) & (df["AÑO"] <= 1999)].copy()
    elif decada == "2000s":
        dff = df[(df["AÑO"] >= 2000) & (df["AÑO"] <= 2009)].copy()
    elif decada == "2010s":
        dff = df[(df["AÑO"] >= 2010) & (df["AÑO"] <= 2019)].copy()
    else:
        dff = df[(df["AÑO"] >= 2020) & (df["AÑO"] <= 2025)].copy()

    intervalos = [0,1,2,3,4,5,6,10]
    etiquetas = ["0-1","1-2","2-3","3-4","4-5","5-6","6+"]

    dff["RANGO_MAG"] = pd.cut(dff["MAGNITUD"], bins=intervalos, labels=etiquetas)
    conteos = dff["RANGO_MAG"].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.bar(conteos.index, conteos.values, color="#d08c60", edgecolor="black")
    ax.set_xlabel("Magnitud (Mw)")
    ax.set_ylabel("Número de sismos")
    st.pyplot(fig)
    plt.close(fig)

# --- TAB 3: PROFUNDIDAD ---
with tab3:
    st.subheader("Profundidad de sismos")

    decada_prof = st.selectbox("Década (profundidad)", ["Todas", "1960s","1970s","1980s","1990s","2000s","2010s","2020s"], key="prof")

    if decada_prof == "Todas":
        dff = df.copy()
    else:
        # Se corrigió la sangría y lógica para evitar error al intentar convertir "Todas" a entero
        año = int(decada_prof[:4])
        dff = df[(df["AÑO"] >= año) & (df["AÑO"] <= año+9)].copy()

    intervalos_prof = [0,50,100,200,300,500,800]
    etiquetas_prof = ["0-50", "50-100", "100-200", "200-300", "300-500", "500+"]

    dff["RANGO_PROF"] = pd.cut(dff["PROFUNDIDAD"], bins=intervalos_prof, labels=etiquetas_prof)
    conteos_prof = dff["RANGO_PROF"].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.bar(conteos_prof.index, conteos_prof.values, color="#a67c52", edgecolor="black")
    ax.set_xlabel("Profundidad (km)")
    ax.set_ylabel("Número de sismos")
    st.pyplot(fig)
    plt.close(fig)

# --- TAB 4: INTERACTIVO ---
with tab4:
    st.subheader("Magnitud vs Década (Interactivo)")

    rango = st.selectbox(
        "Rango de magnitud",
        ["0-1","1-2","2-3","3-4","4-5","5-6","6+"],
        key="mag"
    )

    if rango == "0-1":
        dff = df[df["MAGNITUD"] < 1].copy()
    elif rango == "1-2":
        dff = df[(df["MAGNITUD"] >= 1) & (df["MAGNITUD"] < 2)].copy()
    elif rango == "2-3":
        dff = df[(df["MAGNITUD"] >= 2) & (df["MAGNITUD"] < 3)].copy()
    elif rango == "3-4":
        dff = df[(df["MAGNITUD"] >= 3) & (df["MAGNITUD"] < 4)].copy()
    elif rango == "4-5":
        dff = df[(df["MAGNITUD"] >= 4) & (df["MAGNITUD"] < 5)].copy()
    elif rango == "5-6":
        dff = df[(df["MAGNITUD"] >= 5) & (df["MAGNITUD"] < 6)].copy()
    else:
        dff = df[df["MAGNITUD"] >= 6].copy()

    decadas_interactiva = {
        "60s": ((dff["AÑO"]>=1960)&(dff["AÑO"]<=1969)).sum(),
        "70s": ((dff["AÑO"]>=1970)&(dff["AÑO"]<=1979)).sum(),
        "80s": ((dff["AÑO"]>=1980)&(dff["AÑO"]<=1989)).sum(),
        "90s": ((dff["AÑO"]>=1990)&(dff["AÑO"]<=1999)).sum(),
        "00s": ((dff["AÑO"]>=2000)&(dff["AÑO"]<=2009)).sum(),
        "10s": ((dff["AÑO"]>=2010)&(dff["AÑO"]<=2019)).sum(),
        "20s": ((dff["AÑO"]>=2020)&(dff["AÑO"]<=2025)).sum(),
    }

    fig, ax = plt.subplots()
    ax.bar(decadas_interactiva.keys(), decadas_interactiva.values(), color="#b07d62", edgecolor="black")
    st.pyplot(fig)
    plt.close(fig)

# --- TAB 5: MAPA ---
with tab5:
    st.subheader("🗺️ Mapa de sismos")
    # Streamlit requiere que las columnas se llamen exactamente 'latitude' y 'longitude'
    # o especificarlas explícitamente como ya hiciste:
    st.map(df, latitude="LATITUD", longitude="LONGITUD")

# --- TAB 6: RELACIÓN ---
with tab6:
    st.subheader("Relación entre magnitud y profundidad")
    fig, ax = plt.subplots()
    ax.scatter(df["MAGNITUD"], df["PROFUNDIDAD"], alpha=0.4, color="#a67c52")
    ax.set_xlabel("Magnitud (Mw)")
    ax.set_ylabel("Profundidad (km)")
    st.pyplot(fig)
    plt.close(fig)

# --- TAB 7: CONCLUSIONES ---
with tab7:
    st.subheader("📝 Conclusiones del análisis")
    st.success("La mayor cantidad de sismos registrados se concentra en magnitudes entre 4 y 5 Mw.")
    st.info("La mayoría de los eventos sísmicos presentan profundidades menores a 50 km.")
    st.warning("La década 2010-2019 registra el mayor número de sismos dentro del catálogo analizado.")
    st.success("El mapa muestra una alta concentración de eventos sísmicos frente a la costa peruana, coherente con la interacción de placas tectónicas en el borde occidental de Sudamérica.")
    st.markdown("---")
    st.write("En general, los resultados evidencian la alta actividad sísmica del Perú y permiten identificar patrones relacionados con la magnitud, profundidad y distribución temporal de los eventos registrados.")
