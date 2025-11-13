# ============================================================
# PROYECTO AEROPUERTO - Panel de Administración v4.0
# ============================================================
# (Refactorizado por Gemini con Sidebar Elegante y Acento Turquesa)
# ============================================================

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
    '<div class="footer">Panel v4.0<br/>Desarrollado con Streamlit</div>',
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
                st.bar_chart(estado_counts, color="#00AAB2") # <-- COLOR ACTUALIZADO
            with col2:
                st.write("Vuelos por Origen (Top 5)")
                origen_counts = vuelos_df.groupby("origen")["id_vuelo"].count().nlargest(5)
                st.bar_chart(origen_counts, color="#003366") # <-- COLOR ACTUALIZADO
        else:
            st.info("No hay datos de vuelos para mostrar.")

    with tab2:
        st.subheader("Volumen de Pasajeros en Tránsito")
        if not transito_df.empty:
            transito_df['fecha'] = pd.to_datetime(transito_df['fecha'])
            transito_diario = transito_df.groupby('fecha')['num_pasajeros'].sum()
            st.write("Tránsito de Pasajeros por Día")
            st.area_chart(transito_diario, color="#00AAB2") # <-- COLOR ACTUALIZADO
        else:
            st.info("No hay datos de tránsito para mostrar.")

# ------------------------------------------------------------
# SECCIÓN: GESTIÓN DE VUELOS
# ------------------------------------------------------------
elif opcion == "✈️ Gestión de Vuelos":
    st.title("✈️ Gestión de Vuelos")

    tab1, tab2 = st.tabs(["📋 Visualizar y Filtrar Vuelos", "➕ Registrar Nuevo Vuelo"])

    with tab1:
        st.subheader("Filtros y Búsqueda")
        col1, col2 = st.columns([1, 1])
        with col1:
            buscar_origen_destino = st.text_input("Buscar por Origen o Destino", placeholder="Ej: MEX, JFK...")
        with col2:
            estados_disponibles = ["Todos"] + vuelos_df["estado"].unique().tolist()
            filtrar_estado = st.selectbox("Filtrar por Estado", options=estados_disponibles)
        
        vuelos_filtrados = vuelos_df.copy()
        if buscar_origen_destino:
            vuelos_filtrados = vuelos_filtrados[
                vuelos_filtrados["origen"].str.contains(buscar_origen_destino, case=False) |
                vuelos_filtrados["destino"].str.contains(buscar_origen_destino, case=False)
            ]
        if filtrar_estado != "Todos":
            vuelos_filtrados = vuelos_filtrados[vuelos_filtrados["estado"] == filtrar_estado]

        st.subheader("Lista de Vuelos Registrados")
        if not vuelos_filtrados.empty:
            st.dataframe(vuelos_filtrados, use_container_width=True)
            csv = vuelos_filtrados.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Descargar Lista Filtrada (CSV)",
                data=csv,
                file_name="lista_vuelos_filtrada.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.warning("No se encontraron vuelos que coincidan con los filtros.")

    with tab2:
        st.subheader("Formulario de Registro")
        with st.form("form_vuelo"):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha del vuelo", value=date.today())
                origen = st.text_input("Aeropuerto de origen", placeholder="Ej: MEX")
                estado = st.selectbox("Estado del vuelo", ["Programado", "En curso", "Completado", "Cancelado"])
            with col2:
                destino = st.text_input("Aeropuerto de destino", placeholder="Ej: JFK")
                num_pasajeros = st.number_input("Número de pasajeros", min_value=0, step=1)
            
            submit = st.form_submit_button("Registrar vuelo")

            if submit:
                if not origen or not destino:
                    st.error("Los campos Origen y Destino son obligatorios.")
                else:
                    if origen.upper() not in AEROPUERTO_COORDS or destino.upper() not in AEROPUERTO_COORDS:
                        st.warning(f"Advertencia: Uno de los aeropuertos ({origen}, {destino}) no tiene coordenadas GPS definidas. Se registrará, pero no aparecerá en el mapa.")
                    
                    ejecutar_query(
                        "INSERT INTO vuelos (fecha, origen, destino, num_pasajeros, estado) VALUES (?, ?, ?, ?, ?)",
                        (fecha, origen.upper(), destino.upper(), num_pasajeros, estado)
                    )
                    st.success("✅ Vuelo registrado correctamente")
                    st.experimental_rerun()

# ------------------------------------------------------------
# SECCIÓN: GESTIÓN DE PASAJEROS
# ------------------------------------------------------------
elif opcion == "👤 Gestión de Pasajeros":
    st.title("👤 Gestión de Pasajeros")

    tab1, tab2 = st.tabs(["👥 Pasajeros de Vuelo", "🚶 Pasajeros en Tránsito"])

    with tab1:
        st.subheader("Pasajeros de Vuelo")
        
        sub_tab1, sub_tab2 = st.tabs(["📋 Búsqueda Simple", "🔍 Búsqueda Avanzada por Edad"])

        with sub_tab1:
            buscar_pasajero = st.text_input("Buscar por Nombre o Ticket", placeholder="Ej: Juan Pérez, TCK-12345...", key="busqueda_simple")
            pasajeros_filtrados = pasajeros_df.copy()
            if buscar_pasajero:
                pasajeros_filtrados = pasajeros_filtrados[
                    pasajeros_filtrados["nombre"].str.contains(buscar_pasajero, case=False) |
                    pasajeros_filtrados["ticket"].str.contains(buscar_pasajero, case=False)
                ]
            st.dataframe(pasajeros_filtrados, use_container_width=True)

        with sub_tab2:
            st.subheader("Filtros Avanzados de Pasajeros")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                buscar_avanzado = st.text_input("Buscar por Nombre/Ticket (Opcional)", key="busqueda_avanzada")
                grupo_etario = st.selectbox(
                    "Grupo Etario (Pre-selección)",
                    ["Personalizado", "Jóvenes (18-30)", "Adultos (31-60)", "Seniors (61+)"]
                )
            
            with col2:
                min_edad_db = pasajeros_df["edad"].min() if not pasajeros_df.empty else 18
                max_edad_db = pasajeros_df["edad"].max() if not pasajeros_df.empty else 100
                
                if grupo_etario == "Jóvenes (18-30)":
                    default_range = (18, 30)
                elif grupo_etario == "Adultos (31-60)":
                    default_range = (31, 60)
                elif grupo_etario == "Seniors (61+)":
                    default_range = (61, int(max_edad_db))
                else:
                    default_range = (int(min_edad_db), int(max_edad_db))
                
                edad_range = st.slider(
                    "Seleccionar rango de edad",
                    min_value=int(min_edad_db),
                    max_value=int(max_edad_db),
                    value=default_range
                )
            
            pasajeros_filtrados_av = pasajeros_df.copy()
            if buscar_avanzado:
                pasajeros_filtrados_av = pasajeros_filtrados_av[
                    pasajeros_filtrados_av["nombre"].str.contains(buscar_avanzado, case=False) |
                    pasajeros_filtrados_av["ticket"].str.contains(buscar_avanzado, case=False)
                ]
            
            min_edad, max_edad = edad_range
            pasajeros_filtrados_av = pasajeros_filtrados_av[
                (pasajeros_filtrados_av["edad"] >= min_edad) & (pasajeros_filtrados_av["edad"] <= max_edad)
            ]

            st.subheader("Resultados del Filtro Avanzado")
            
            if not pasajeros_filtrados_av.empty:
                st.dataframe(pasajeros_filtrados_av, use_container_width=True)
                
                st.markdown("---")
                st.subheader("Estadísticas y Distribución del Grupo")
                
                col_stats, col_chart = st.columns([1, 2])
                
                with col_stats:
                    edad_promedio = pasajeros_filtrados_av['edad'].mean()
                    edad_mediana = pasajeros_filtrados_av['edad'].median()
                    edad_moda = pasajeros_filtrados_av['edad'].mode().tolist()
                    
                    st.metric("Pasajeros Encontrados", f"{len(pasajeros_filtrados_av)}")
                    st.metric("Edad Promedio", f"{edad_promedio:.1f} años")
                    st.metric("Edad Mediana", f"{edad_mediana:.0f} años")
                    st.metric("Edad(es) Moda", f"{', '.join(map(str, edad_moda))} años")

                with col_chart:
                    st.write("Distribución de Edades (Histograma)")
                    hist_data = pasajeros_filtrados_av['edad'].value_counts().sort_index()
                    st.bar_chart(hist_data, color="#00AAB2") # <-- COLOR ACTUALIZADO
            else:
                st.info("No se encontraron pasajeros que coincidan con todos los filtros.")

        with st.expander("➕ Registrar nuevo pasajero de vuelo"):
            with st.form("form_pasajero"):
                if vuelos_df.empty:
                    st.warning("Debe registrar al menos un vuelo antes de añadir pasajeros.")
                else:
                    vuelos_opciones = {f"{row.id_vuelo} ({row.origen} > {row.destino})": row.id_vuelo for row in vuelos_df.itertuples()}
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        vuelo_seleccionado = st.selectbox("Vuelo asignado", options=vuelos_opciones.keys())
                        vuelo_id = vuelos_opciones[vuelo_seleccionado]
                        nombre = st.text_input("Nombre del pasajero")
                    with col2:
                        ticket = st.text_input("Ticket (Ej: TCK-12345)")
                        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
                    
                    submit = st.form_submit_button("Registrar pasajero")

                    if submit:
                        if not nombre or not ticket:
                            st.error("Nombre y Ticket son obligatorios.")
                        else:
                            ejecutar_query(
                                "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                                (vuelo_id, ticket.upper(), nombre, edad)
                            )
                            st.success("✅ Pasajero registrado correctamente")
                            st.experimental_rerun()

    with tab2:
        st.subheader("Pasajeros en Tránsito")
        buscar_aeropuerto = st.text_input("Buscar por Aeropuerto", placeholder="Ej: PTY, MAD...", key="busqueda_transito")
        transito_filtrado = transito_df.copy()
        if buscar_aeropuerto:
            transito_filtrado = transito_filtrado[
                transito_filtrado["aeropuerto"].str.contains(buscar_aeropuerto, case=False)
            ]
        st.dataframe(transito_filtrado, use_container_width=True)

        with st.expander("➕ Registrar nuevo conteo de tránsito"):
            with st.form("form_transito"):
                col1, col2 = st.columns(2)
                with col1:
                    fecha_transito = st.date_input("Fecha", value=date.today(), key="transito_fecha")
                with col2:
                    aeropuerto_transito = st.text_input("Aeropuerto (Ej: PTY)", key="transito_aero")
                
                num_pasajeros_transito = st.number_input("Número de pasajeros", min_value=0, step=1, key="transito_num")
                
                submit = st.form_submit_button("Registrar tránsito")

                if submit:
                    if not aeropuerto_transito:
                        st.error("El aeropuerto es obligatorio.")
                    else:
                        ejecutar_query(
                            "INSERT INTO pasajeros_transito (fecha, aeropuerto, num_pasajeros) VALUES (?, ?, ?)",
                            (fecha_transito, aeropuerto_transito.upper(), num_pasajeros_transito)
                        )
                        st.success("✅ Registro de tránsito añadido correctamente")
                        st.experimental_rerun()

# ------------------------------------------------------------
# SECCIÓN: MAPA DE RUTAS
# ------------------------------------------------------------
elif opcion == "🗺️ Mapa de Rutas":
    st.title("🗺️ Mapa de Rutas de Vuelos")
    st.markdown("Visualización de los aeropuertos de origen y destino de los vuelos filtrados.")

    st.subheader("Filtros de Visualización")
    aeropuertos_en_vuelos = pd.concat([vuelos_df['origen'], vuelos_df['destino']]).unique().tolist()
    aeropuertos_validos = [a for a in aeropuertos_en_vuelos if a in AEROPUERTO_COORDS]
    estados_validos = vuelos_df['estado'].unique().tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_origen = st.multiselect("Origen(es)", options=aeropuertos_validos, placeholder="Todos")
    with col2:
        filtro_destino = st.multiselect("Destino(s)", options=aeropuertos_validos, placeholder="Todos")
    with col3:
        filtro_estado = st.multiselect("Estado(s) del Vuelo", options=estados_validos, placeholder="Todos")
    
    vuelos_mapa_filtrados = vuelos_df.copy()
    if filtro_origen:
        vuelos_mapa_filtrados = vuelos_mapa_filtrados[vuelos_mapa_filtrados['origen'].isin(filtro_origen)]
    if filtro_destino:
        vuelos_mapa_filtrados = vuelos_mapa_filtrados[vuelos_mapa_filtrados['destino'].isin(filtro_destino)]
    if filtro_estado:
        vuelos_mapa_filtrados = vuelos_mapa_filtrados[vuelos_mapa_filtrados['estado'].isin(filtro_estado)]

    map_data_list = []
    vuelos_mapa_validos = vuelos_mapa_filtrados[
        vuelos_mapa_filtrados['origen'].isin(AEROPUERTO_COORDS.keys()) &
        vuelos_mapa_filtrados['destino'].isin(AEROPUERTO_COORDS.keys())
    ]
    
    aeropuertos_en_mapa = set()
    for row in vuelos_mapa_validos.itertuples():
        aeropuertos_en_mapa.add(row.origen)
        aeropuertos_en_mapa.add(row.destino)

    for aero in aeropuertos_en_mapa:
        map_data_list.append(AEROPUERTO_COORDS[aero])

    col_mapa, col_stats_mapa = st.columns([3, 1])

    with col_mapa:
        st.subheader("Aeropuertos Activos (Según Filtro)")
        if map_data_list:
            map_df = pd.DataFrame(map_data_list)
            st.map(map_df, zoom=1)
            st.info("Nota: `st.map()` nativo de Streamlit solo puede mostrar puntos (aeropuertos), no las líneas de ruta directas.")
        else:
            st.warning("No se encontraron vuelos o aeropuertos que coincidan con los filtros y tengan coordenadas definidas.")

    with col_stats_mapa:
        st.subheader("Rutas Más Frecuentes")
        st.write("(Basado en los vuelos filtrados)")
        if not vuelos_mapa_validos.empty:
            rutas_frecuentes = vuelos_mapa_validos.groupby(['origen', 'destino'])\
                                .size().nlargest(10).reset_index(name='Conteo')
            rutas_frecuentes.index += 1
            st.dataframe(rutas_frecuentes, use_container_width=True)
        else:
            st.info("No hay datos de rutas para mostrar.")


# ------------------------------------------------------------
# SECCIÓN: ANÁLISIS Y REPORTES
# ------------------------------------------------------------
elif opcion == "📈 Análisis y Reportes":
    st.title("📈 Análisis y Reportes")
    
    tab1, tab2 = st.tabs(["Historial de Vuelos", "Análisis de Pasajeros"])

    with tab1:
        st.subheader("Historial de Operaciones de Vuelos")
        if not vuelos_df.empty:
            vuelos_df["fecha"] = pd.to_datetime(vuelos_df["fecha"])
            
            st.write("Vuelos por Día (Últimos 90 días)")
            historial_diario = vuelos_df.groupby("fecha")["id_vuelo"].count()
            st.line_chart(historial_diario, color="#003366") # <-- COLOR ACTUALIZADO

            st.write("Vuelos por Mes")
            vuelos_df["mes"] = vuelos_df["fecha"].dt.to_period("M").astype(str)
            historial_mensual = vuelos_df.groupby("mes")["id_vuelo"].count()
            st.bar_chart(historial_mensual, color="#00AAB2") # <-- COLOR ACTUALIZADO

            csv_vuelos_full = vuelos_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Descargar Historial Completo de Vuelos (CSV)",
                data=csv_vuelos_full,
                file_name="historial_vuelos_completo.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.warning("No hay datos de vuelos para generar reportes.")

    with tab2:
        st.subheader("Análisis Demográfico de Pasajeros")
        if not pasajeros_df.empty:
            st.write("Distribución de Edades General")
            bins = [0, 18, 25, 35, 45, 55, 65, 100]
            labels = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
            try:
                pasajeros_df["rango_edad"] = pd.cut(pasajeros_df["edad"], bins=bins, labels=labels, right=False)
                conteo_edades = pasajeros_df.groupby("rango_edad")["id_pasajero"].count()
                st.bar_chart(conteo_edades, color="#00AAB2") # <-- COLOR ACTUALIZADO
            except Exception as e:
                st.error(f"Error al procesar rangos de edad: {e}")
        else:
            st.warning("No hay datos de pasajeros para analizar.")


# ------------------------------------------------------------
# SECCIÓN: CONFIGURACIÓN
# ------------------------------------------------------------
elif opcion == "⚙️ Configuración":
    st.title("⚙️ Configuración del Sistema")
    st.subheader("Gestión de la Base de Datos")

    st.info("Utiliza estos controles para manejar los datos de la aplicación.")

    if st.button("Forzar Generación de Datos de Ejemplo", type="primary"):
        with st.spinner("Generando nuevos datos..."):
            generar_datos_ejemplo(force_run=True)
    
    st.markdown("---")
    
    st.subheader("Zona de Peligro")
    st.warning("⚠️ **Atención:** Esta acción es irreversible. Se borrarán todos los vuelos, pasajeros y registros de tránsito existentes.")
    
    if st.button("Reiniciar y Borrar TODA la Base de Datos"):
        with st.spinner("Reiniciando base de datos..."):
            reiniciar_base_de_datos()
