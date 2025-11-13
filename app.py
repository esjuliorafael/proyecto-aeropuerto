# ============================================================
# PROYECTO AEROPUERTO - Panel de Administración
# ============================================================

import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import date, timedelta

# ------------------------------------------------------------
# BASE DE DATOS
# ------------------------------------------------------------
def get_connection():
    return sqlite3.connect("aeropuerto.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # --- Tabla de vuelos ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS vuelos (
            id_vuelo INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            origen TEXT,
            destino TEXT,
            num_pasajeros INTEGER,
            estado TEXT
        )
    ''')

    # --- Tabla de pasajeros en tránsito ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS pasajeros_transito (
            id_transito INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            aeropuerto TEXT,
            num_pasajeros INTEGER
        )
    ''')

    # --- NUEVA: Tabla de pasajeros ---
    c.execute('''
        CREATE TABLE IF NOT EXISTS pasajeros (
            id_pasajero INTEGER PRIMARY KEY AUTOINCREMENT,
            vuelo_id INTEGER,
            ticket TEXT,
            nombre TEXT,
            edad INTEGER,
            FOREIGN KEY (vuelo_id) REFERENCES vuelos(id_vuelo)
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------
def ejecutar_query(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def cargar_datos(tabla):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    conn.close()
    return df

# ------------------------------------------------------------
# GENERAR DATOS DE EJEMPLO
# ------------------------------------------------------------
def generar_datos_ejemplo():
    conn = get_connection()
    c = conn.cursor()

    # Vuelos
    c.execute("SELECT COUNT(*) FROM vuelos")
    count_vuelos = c.fetchone()[0]
    if count_vuelos == 0:
        aeropuertos = ["MEX", "BOG", "JFK", "LAX", "MAD", "CDG", "GRU", "SCL", "LIM", "PTY"]
        estados = ["En curso", "Completado", "Cancelado"]
        hoy = date.today()
        fechas = [hoy - timedelta(days=i) for i in range(30)]

        for _ in range(100):
            fecha = random.choice(fechas)
            origen, destino = random.sample(aeropuertos, 2)
            num_pasajeros = random.randint(50, 300)
            estado = random.choice(estados)
            ejecutar_query(
                "INSERT INTO vuelos (fecha, origen, destino, num_pasajeros, estado) VALUES (?, ?, ?, ?, ?)",
                (fecha, origen, destino, num_pasajeros, estado)
            )

    # Pasajeros en tránsito
    c.execute("SELECT COUNT(*) FROM pasajeros_transito")
    count_transito = c.fetchone()[0]
    if count_transito == 0:
        aeropuertos = ["MEX", "BOG", "JFK", "LAX", "MAD", "CDG", "GRU", "SCL", "LIM", "PTY"]
        hoy = date.today()
        fechas = [hoy - timedelta(days=i) for i in range(30)]
        for _ in range(40):
            fecha = random.choice(fechas)
            aeropuerto = random.choice(aeropuertos)
            num_pasajeros = random.randint(100, 1000)
            ejecutar_query(
                "INSERT INTO pasajeros_transito (fecha, aeropuerto, num_pasajeros) VALUES (?, ?, ?)",
                (fecha, aeropuerto, num_pasajeros)
            )

    # Pasajeros
    c.execute("SELECT COUNT(*) FROM pasajeros")
    count_pasajeros = c.fetchone()[0]
    if count_pasajeros == 0:
        vuelos_df = pd.read_sql_query("SELECT id_vuelo FROM vuelos", conn)
        if not vuelos_df.empty:
            nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Fernanda", "Jorge", "Sofía", "Andrés", "Elena",
                       "Roberto", "Valeria", "Pedro", "Camila", "Ricardo", "Daniela", "Pablo", "Laura", "Miguel", "Isabel"]
            for _ in range(100):
                vuelo_id = random.choice(vuelos_df["id_vuelo"].tolist())
                nombre = random.choice(nombres) + " " + random.choice(["García", "Pérez", "López", "Martínez", "Hernández"])
                edad = random.randint(18, 70)
                ticket = f"TCK-{random.randint(10000,99999)}"
                ejecutar_query(
                    "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                    (vuelo_id, ticket, nombre, edad)
                )

        st.success("✅ Se generaron 100 vuelos, 40 registros de tránsito y 100 pasajeros.")
    conn.close()

generar_datos_ejemplo()

# ------------------------------------------------------------
# CONFIGURACIÓN DE INTERFAZ
# ------------------------------------------------------------
st.set_page_config(page_title="Proyecto Aeropuerto", layout="wide")

st.markdown("""
    <style>
        body, .stApp {
            background-color: #F9FAFB;
            color: #1F2937;
            font-family: "Inter", sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #1E3A8A;
            color: white;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label, .stRadio label {
            color: white !important;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
        div[data-testid="stMetricValue"] {
            color: #06B6D4;
            font-weight: 600;
        }
        button[kind="primary"] {
            background-color: #06B6D4 !important;
            color: white !important;
            border-radius: 10px !important;
        }
        .stDataFrame {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PANEL LATERAL
# ------------------------------------------------------------
st.sidebar.title("🛫 Proyecto Aeropuerto")
opcion = st.sidebar.radio("Navegación", 
    ["📊 Dashboard", "✈️ Vuelos", "👤 Pasajeros", "👥 Pasajeros en Tránsito", "📅 Historial"])

# ------------------------------------------------------------
# SECCIÓN: DASHBOARD
# ------------------------------------------------------------
if opcion == "📊 Dashboard":
    st.title("📊 Panel General de Monitoreo")

    vuelos_df = cargar_datos("vuelos")
    transito_df = cargar_datos("pasajeros_transito")
    pasajeros_df = cargar_datos("pasajeros")

    total_vuelos = len(vuelos_df)
    total_pasajeros = len(pasajeros_df)
    total_transito = transito_df["num_pasajeros"].sum() if not transito_df.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de vuelos", total_vuelos)
    col2.metric("Pasajeros registrados", total_pasajeros)
    col3.metric("Pasajeros en tránsito", total_transito)

    if not vuelos_df.empty:
        st.subheader("Distribución por Origen y Destino")
        col1, col2 = st.columns(2)
        col1.bar_chart(vuelos_df.groupby("origen")["id_vuelo"].count())
        col2.bar_chart(vuelos_df.groupby("destino")["id_vuelo"].count())

# ------------------------------------------------------------
# SECCIÓN: VUELOS
# ------------------------------------------------------------
elif opcion == "✈️ Vuelos":
    st.title("✈️ Gestión de Vuelos")

    with st.expander("➕ Registrar nuevo vuelo", expanded=True):
        with st.form("form_vuelo"):
            fecha = st.date_input("Fecha del vuelo", value=date.today())
            origen = st.text_input("Aeropuerto de origen")
            destino = st.text_input("Aeropuerto de destino")
            num_pasajeros = st.number_input("Número de pasajeros", min_value=0)
            estado = st.selectbox("Estado del vuelo", ["En curso", "Completado", "Cancelado"])
            submit = st.form_submit_button("Registrar vuelo")

            if submit:
                ejecutar_query(
                    "INSERT INTO vuelos (fecha, origen, destino, num_pasajeros, estado) VALUES (?, ?, ?, ?, ?)",
                    (fecha, origen, destino, num_pasajeros, estado)
                )
                st.success("✅ Vuelo registrado correctamente")

    vuelos_df = cargar_datos("vuelos")
    st.subheader("📋 Lista de vuelos registrados")
    if not vuelos_df.empty:
        st.dataframe(vuelos_df, use_container_width=True)
    else:
        st.info("No hay vuelos registrados.")

# ------------------------------------------------------------
# SECCIÓN: PASAJEROS
# ------------------------------------------------------------
elif opcion == "👤 Pasajeros":
    st.title("👤 Registro y Listado de Pasajeros")

    pasajeros_df = cargar_datos("pasajeros")
    vuelos_df = cargar_datos("vuelos")

    with st.expander("➕ Registrar pasajero manualmente", expanded=True):
        with st.form("form_pasajero"):
            if vuelos_df.empty:
                st.warning("Primero deben existir vuelos registrados.")
            else:
                vuelo_id = st.selectbox("Vuelo asignado", vuelos_df["id_vuelo"])
                ticket = st.text_input("Ticket")
                nombre = st.text_input("Nombre del pasajero")
                edad = st.number_input("Edad", min_value=0, max_value=100)
                submit = st.form_submit_button("Registrar pasajero")

                if submit:
                    ejecutar_query(
                        "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                        (vuelo_id, ticket, nombre, edad)
                    )
                    st.success("✅ Pasajero registrado correctamente")

    st.subheader("📋 Lista de pasajeros")
    if not pasajeros_df.empty:
        st.dataframe(pasajeros_df, use_container_width=True)
    else:
        st.info("No hay pasajeros registrados.")

# ------------------------------------------------------------
# SECCIÓN: PASAJEROS EN TRÁNSITO
# ------------------------------------------------------------
elif opcion == "👥 Pasajeros en Tránsito":
    st.title("👥 Monitoreo de Pasajeros en Tránsito")

    with st.expander("➕ Registrar nuevo tránsito", expanded=True):
        with st.form("form_transito"):
            fecha = st.date_input("Fecha", value=date.today())
            aeropuerto = st.text_input("Aeropuerto")
            num_pasajeros = st.number_input("Número de pasajeros", min_value=0)
            submit = st.form_submit_button("Registrar tránsito")

            if submit:
                ejecutar_query(
                    "INSERT INTO pasajeros_transito (fecha, aeropuerto, num_pasajeros) VALUES (?, ?, ?)",
                    (fecha, aeropuerto, num_pasajeros)
                )
                st.success("✅ Registro añadido correctamente")

    transito_df = cargar_datos("pasajeros_transito")
    st.subheader("📋 Registros existentes")
    if not transito_df.empty:
        st.dataframe(transito_df, use_container_width=True)
    else:
        st.info("No hay registros de pasajeros en tránsito aún.")

# ------------------------------------------------------------
# SECCIÓN: HISTORIAL
# ------------------------------------------------------------
elif opcion == "📅 Historial":
    st.title("📅 Historial de Vuelos")

    df = cargar_datos("vuelos")
    if df.empty:
        st.warning("No hay datos de vuelos registrados.")
    else:
        df["fecha"] = pd.to_datetime(df["fecha"])
        df["mes"] = df["fecha"].dt.to_period("M").astype(str)

        st.subheader("📊 Historial Diario")
        st.line_chart(df.groupby("fecha")["id_vuelo"].count())

        st.subheader("📊 Historial Mensual")
        st.bar_chart(df.groupby("mes")["id_vuelo"].count())

        st.download_button(
            "📥 Descargar historial completo (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name="historial_vuelos.csv"
        )
