import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import date, timedelta

# ------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Admin Aeropuerto",
    page_icon="🛫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# DATOS GLOBALES (Coordenadas)
# ------------------------------------------------------------
AEROPUERTO_COORDS = {
    "MEX": {"lat": 19.4363, "lon": -99.0721},
    "BOG": {"lat": 4.7016, "lon": -74.1469},
    "JFK": {"lat": 40.6413, "lon": -73.7781},
    "LAX": {"lat": 33.9416, "lon": -118.4085},
    "MAD": {"lat": 40.4983, "lon": -3.5676},
    "CDG": {"lat": 49.0097, "lon": 2.5479},
    "GRU": {"lat": -23.4356, "lon": -46.4731},
    "SCL": {"lat": -33.3930, "lon": -70.7858},
    "LIM": {"lat": -12.0219, "lon": -77.1143},
    "PTY": {"lat": 9.0713, "lon": -79.3835}
}


# ------------------------------------------------------------
# BASE DE DATOS (Sin cambios)
# ------------------------------------------------------------
def get_connection():
    return sqlite3.connect("aeropuerto.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS pasajeros_transito (
            id_transito INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            aeropuerto TEXT,
            num_pasajeros INTEGER
        )
    ''')
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

# ------------------------------------------------------------
# FUNCIONES AUXILIARES DE DB (Sin cambios)
# ------------------------------------------------------------
def ejecutar_query(query, params=()):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}")
    finally:
        if conn:
            conn.close()

def cargar_datos(tabla):
    try:
        conn = get_connection()
        df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
        return df
    except Exception as e:
        st.error(f"Error al cargar datos de {tabla}: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# ------------------------------------------------------------
# GENERAR/REINICIAR DATOS (Sin cambios)
# ------------------------------------------------------------
def generar_datos_ejemplo(force_run=False):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM vuelos")
        count_vuelos = c.fetchone()[0]
        if count_vuelos == 0 or force_run:
            aeropuertos = list(AEROPUERTO_COORDS.keys())
            estados = ["Programado", "En curso", "Completado", "Cancelado"]
            hoy = date.today()
            fechas = [hoy - timedelta(days=i) for i in range(90)]
            for _ in range(100):
                c.execute(
                    "INSERT INTO vuelos (fecha, origen, destino, num_pasajeros, estado) VALUES (?, ?, ?, ?, ?)",
                    (random.choice(fechas), *random.sample(aeropuertos, 2), random.randint(50, 300), random.choice(estados))
                )

        c.execute("SELECT COUNT(*) FROM pasajeros_transito")
        count_transito = c.fetchone()[0]
        if count_transito == 0 or force_run:
            aeropuertos = list(AEROPUERTO_COORDS.keys())
            hoy = date.today()
            fechas = [hoy - timedelta(days=i) for i in range(90)]
            for _ in range(40):
                c.execute(
                    "INSERT INTO pasajeros_transito (fecha, aeropuerto, num_pasajeros) VALUES (?, ?, ?)",
                    (random.choice(fechas), random.choice(aeropuertos), random.randint(100, 1000))
                )

        c.execute("SELECT COUNT(*) FROM pasajeros")
        count_pasajeros = c.fetchone()[0]
        if count_pasajeros == 0 or force_run:
            vuelos_df = pd.read_sql_query("SELECT id_vuelo FROM vuelos", conn)
            if not vuelos_df.empty:
                nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Fernanda", "Jorge", "Sofía", "Andrés", "Elena"]
                apellidos = ["García", "Pérez", "López", "Martínez", "Hernández", "Díaz", "Moreno", "Álvarez"]
                for _ in range(200):
                    c.execute(
                        "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                        (random.choice(vuelos_df["id_vuelo"].tolist()), f"TCK-{random.randint(10000,99999)}",
                         f"{random.choice(nombres)} {random.choice(apellidos)}", random.randint(18, 80))
                    )
        
        conn.commit()
        if force_run:
            st.toast("✅ Base de datos reiniciada con nuevos datos.", icon="🔄")
        
    except Exception as e:
        st.error(f"Error generando datos: {e}")
    finally:
        conn.close()

def reiniciar_base_de_datos():
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS pasajeros")
        c.execute("DROP TABLE IF EXISTS pasajeros_transito")
        c.execute("DROP TABLE IF EXISTS vuelos")
        conn.commit()
    except Exception as e:
        st.error(f"Error limpiando la DB: {e}")
    finally:
        conn.close()
    
    init_db()
    generar_datos_ejemplo(force_run=True)
    st.success("Base de datos reiniciada exitosamente.")

# ------------------------------------------------------------
# NUEVA FUNCIÓN DE LÓGICA FUZZY (DE Fuzzy.py)
# ------------------------------------------------------------
def triangular(x, a=17, b=28, c=30):
    """
    Calcula el grado de pertenencia para una función triangular.
    Por defecto, define el conjunto "Joven" (17-30) con pico en 28.
    """
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    elif x == b: # Caso especial para el pico
        return 1.0


# ------------------------------------------------------------
# APLICAR CSS MODERNO v4 (Elegante + Acento Turquesa)
# ------------------------------------------------------------
st.markdown("""
    <style>
        /* --- General --- */
        body, .stApp {
            background-color: #F0F2F6; /* Fondo gris claro */
            color: #333;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        /* --- Sidebar --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(160deg, #003366 0%, #001122 100%); /* Azul marino oscuro a casi negro */
            border-right: 0px;
        }
        [data-testid="stSidebar"] h1 {
            color: white;
            padding: 10px 0 10px 10px;
        }
        
        /* --- Navegación del Sidebar (Radio Buttons) --- */
        [data-testid="stSidebar"] [data-testid="stRadio"] > label {
            padding: 14px 20px;
            border-radius: 8px;
            margin: 4px 10px;
            transition: all 0.3s ease;
            color: #A9B2C0; /* Color de texto no seleccionado (gris-azulado) */
            border-left: 4px solid transparent; /* Borde izquierdo transparente */
        }
        /* Hover en item */
        [data-testid="stSidebar"] [data-testid="stRadio"] > label:hover {
            background-color: rgba(255, 255, 255, 0.05);
            color: #FFFFFF;
            border-left: 4px solid rgba(255, 255, 255, 0.2);
        }
        /* Item seleccionado */
        [data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
            display: none; /* Ocultar el punto de radio original */
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] div[aria-checked="true"] > label {
            background-color: rgba(0, 170, 178, 0.1); /* Fondo sutil de acento */
            color: #FFFFFF !important; /* Texto blanco brillante */
            font-weight: 600;
            border-left: 4px solid #00AAB2; /* Borde de acento turquesa */
        }

        /* --- Títulos Principales --- */
        h1, h2 {
            color: #003366; /* Azul marino oscuro */
            font-weight: 600;
        }
        h3 {
            color: #004488;
            font-weight: 500;
        }

        /* --- Métricas (KPIs) --- */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 22px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            border: 1px solid #E0E0E0;
        }
        [data-testid="stMetricValue"] {
            font-size: 2.75rem !important;
            font-weight: 700;
            color: #00AAB2; /* <-- NUEVO COLOR DE ACENTO */
        }
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            color: #555;
            font-weight: 500;
        }

        /* --- Pestañas (Tabs) --- */
        button[data-baseweb="tab"] {
            font-size: 1rem;
            font-weight: 500;
            color: #555;
            transition: all 0.3s;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #003366; /* Azul marino */
            border-bottom: 3px solid #003366;
        }

        /* --- Botones --- */
        button[kind="primary"] {
            background-color: #00AAB2 !important; /* <-- NUEVO COLOR DE ACENTO */
            color: white !important;
            border: 0 !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            font-weight: 600 !important;
            transition: background-color 0.3s, box-shadow 0.3s !important;
        }
        button[kind="primary"]:hover {
            background-color: #007A7C !important; /* Versión oscura del acento */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
        }

        /* --- DataFrames --- */
        .stDataFrame {
            border: 0;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }
        
        /* --- Contenedores y Formularios --- */
        [data-testid="stForm"] {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        /* --- Footer --- */
        .footer {
            font-size: 0.8rem;
            color: #A9B2C0; /* Color suave del sidebar */
            text-align: center;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# INICIALIZACIÓN (Una sola vez)
# ------------------------------------------------------------
init_db()
generar_datos_ejemplo(force_run=False) # Solo genera si está vacío


# ------------------------------------------------------------
# PANEL LATERAL (SIDEBAR)
# ------------------------------------------------------------
st.sidebar.title("🛫 Admin Aeropuerto")

opcion = st.sidebar.radio(
    "Navegación Principal",
    [
        "📊 Dashboard",
        "✈️ Gestión de Vuelos",
        "👤 Gestión de Pasajeros",
        "🗺️ Mapa de Rutas",
        "📈 Análisis y Reportes",
        "⚙️ Configuración"
    ],
    label_visibility="collapsed"
)

# Footer en Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="footer">Panel v5.0<br/>Desarrollado con Streamlit</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# CARGAR DATOS (una vez para todo el script)
# ------------------------------------------------------------
vuelos_df = cargar_datos("vuelos")
pasajeros_df = cargar_datos("pasajeros")
transito_df = cargar_datos("pasajeros_transito")

# ------------------------------------------------------------
# SECCIÓN: DASHBOARD
# ------------------------------------------------------------
if opcion == "📊 Dashboard":
    st.title("📊 Dashboard: Monitor General")
    st.markdown("Visión general de las operaciones del aeropuerto.")

    total_vuelos = len(vuelos_df)
    total_pasajeros_reg = len(pasajeros_df)
    total_pasajeros_trans = transito_df["num_pasajeros"].sum() if not transito_df.empty else 0
    vuelos_completados = len(vuelos_df[vuelos_df["estado"] == "Completado"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Vuelos", f"{total_vuelos}")
    col2.metric("Vuelos Completados", f"{vuelos_completados}")
    col3.metric("Pasajeros Registrados", f"{total_pasajeros_reg}")
    col4.metric("Total Pasajeros Tránsito", f"{total_pasajeros_trans:,.0f}")

    st.markdown("---")

    tab1, tab2 = st.tabs(["Análisis de Vuelos", "Análisis de Tránsito"])

    with tab1:
        st.subheader("Rendimiento de Vuelos")
        if not vuelos_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Vuelos por Estado")
                estado_counts = vuelos_df.groupby("estado")["id_vuelo"].count()
                st.bar_chart(estado_counts, color="#00AAB2")
            with col2:
                st.write("Vuelos por Origen (Top 5)")
                origen_counts = vuelos_df.groupby("origen")["id_vuelo"].count().nlargest(5)
                st.bar_chart(origen_counts, color="#003366")
        else:
            st.info("No hay datos de vuelos para mostrar.")

    with tab2:
        st.subheader("Volumen de Pasajeros en Tr
