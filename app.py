# ============================================================
# SISTEMA DE GESTIÓN AEROPORTUARIA - VERSIÓN MEJORADA
# ============================================================

import streamlit as st
import sqlite3
import pandas as pd
import random
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sistema Aeroportuario",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# ESTILOS MODERNOS Y MINIMALISTAS
# ------------------------------------------------------------
st.markdown("""
    <style>
        /* Variables de color */
        :root {
            --primary: #2563EB;
            --secondary: #10B981;
            --accent: #F59E0B;
            --danger: #EF4444;
            --bg-main: #F8FAFC;
            --bg-card: #FFFFFF;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --border: #E2E8F0;
        }
        
        /* Fondo general */
        .stApp {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
        }
        
        /* Sidebar mejorado */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E40AF 0%, #1E3A8A 100%);
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            font-size: 0.85rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.05);
            cursor: pointer;
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateX(5px);
        }
        
        /* Títulos */
        h1 {
            color: #1E3A8A;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        h2 {
            color: #1E40AF;
            font-weight: 600;
            font-size: 1.75rem;
            margin: 2rem 0 1rem 0;
        }
        
        h3 {
            color: #2563EB;
            font-weight: 600;
            font-size: 1.25rem;
            margin: 1.5rem 0 1rem 0;
        }
        
        /* Métricas mejoradas */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #1E40AF;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 0.875rem;
        }
        
        /* Tarjetas de métricas personalizadas */
        div[data-testid="column"] > div:first-child {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        div[data-testid="column"] > div:first-child:hover {
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        /* Botones */
        .stButton > button {
            background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 0.75rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(37, 99, 235, 0.3);
        }
        
        /* Formularios */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            border-radius: 0.5rem;
            border: 2px solid #E2E8F0;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stDateInput > div > div > input:focus {
            border-color: #2563EB;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: white;
            border-radius: 0.75rem;
            border: 2px solid #E2E8F0;
            font-weight: 600;
            color: #1E40AF;
            padding: 1rem;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #2563EB;
        }
        
        /* DataFrames */
        .stDataFrame {
            border-radius: 0.75rem;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: white;
            padding: 0.5rem;
            border-radius: 0.75rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
            color: white;
        }
        
        /* Alertas */
        .stSuccess, .stInfo, .stWarning, .stError {
            border-radius: 0.75rem;
            padding: 1rem;
            border-left: 4px solid;
        }
        
        /* Scrollbar personalizado */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #F1F5F9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94A3B8;
        }
        
        /* Animaciones */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .element-container {
            animation: fadeIn 0.5s ease-out;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# BASE DE DATOS
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

def generar_datos_ejemplo():
    conn = get_connection()
    c = conn.cursor()

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

    c.execute("SELECT COUNT(*) FROM pasajeros")
    count_pasajeros = c.fetchone()[0]
    if count_pasajeros == 0:
        vuelos_df = pd.read_sql_query("SELECT id_vuelo FROM vuelos", conn)
        if not vuelos_df.empty:
            nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Fernanda", "Jorge", "Sofía", "Andrés", "Elena"]
            apellidos = ["García", "Pérez", "López", "Martínez", "Hernández", "Rodríguez", "González", "Fernández"]
            for _ in range(100):
                vuelo_id = random.choice(vuelos_df["id_vuelo"].tolist())
                nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
                edad = random.randint(18, 70)
                ticket = f"TCK-{random.randint(10000,99999)}"
                ejecutar_query(
                    "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                    (vuelo_id, ticket, nombre, edad)
                )

    conn.close()

generar_datos_ejemplo()

# ------------------------------------------------------------
# SIDEBAR - NAVEGACIÓN
# ------------------------------------------------------------
st.sidebar.markdown("### ✈️ SISTEMA AEROPORTUARIO")
st.sidebar.markdown("---")

opcion = st.sidebar.radio(
    "NAVEGACIÓN",
    ["🏠 Dashboard", "✈️ Vuelos", "👤 Pasajeros", "🔄 Tránsito", "📊 Análisis", "⚙️ Configuración"],
    label_visibility="visible"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Información del Sistema**")
st.sidebar.info(f"📅 {date.today().strftime('%d/%m/%Y')}\n\n🌐 Sistema v2.0")

# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------
if opcion == "🏠 Dashboard":
    st.title("🏠 Panel de Control Principal")
    st.markdown("**Resumen ejecutivo del sistema aeroportuario**")
    st.markdown("---")

    # Cargar datos
    vuelos_df = cargar_datos("vuelos")
    transito_df = cargar_datos("pasajeros_transito")
    pasajeros_df = cargar_datos("pasajeros")

    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vuelos = len(vuelos_df)
        vuelos_hoy = len(vuelos_df[vuelos_df['fecha'] == str(date.today())]) if not vuelos_df.empty else 0
        st.metric("Total Vuelos", f"{total_vuelos:,}", f"+{vuelos_hoy} hoy")
    
    with col2:
        total_pasajeros = len(pasajeros_df)
        st.metric("Pasajeros", f"{total_pasajeros:,}")
    
    with col3:
        total_transito = transito_df["num_pasajeros"].sum() if not transito_df.empty else 0
        st.metric("En Tránsito", f"{total_transito:,}")
    
    with col4:
        if not vuelos_df.empty:
            completados = len(vuelos_df[vuelos_df['estado'] == 'Completado'])
            tasa = (completados / total_vuelos * 100) if total_vuelos > 0 else 0
            st.metric("Tasa Éxito", f"{tasa:.1f}%")
        else:
            st.metric("Tasa Éxito", "0%")

    st.markdown("---")

    # Gráficos principales
    if not vuelos_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribución por Estado")
            estado_counts = vuelos_df['estado'].value_counts()
            fig = px.pie(
                values=estado_counts.values,
                names=estado_counts.index,
                color_discrete_sequence=['#10B981', '#F59E0B', '#EF4444'],
                hole=0.4
            )
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🌍 Top 10 Rutas")
            vuelos_df['ruta'] = vuelos_df['origen'] + ' → ' + vuelos_df['destino']
            top_rutas = vuelos_df['ruta'].value_counts().head(10)
            fig = px.bar(
                x=top_rutas.values,
                y=top_rutas.index,
                orientation='h',
                color=top_rutas.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False,
                xaxis_title="Cantidad",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)

        # Tendencia temporal
        st.subheader("📅 Tendencia de Vuelos")
        vuelos_df['fecha'] = pd.to_datetime(vuelos_df['fecha'])
        vuelos_por_dia = vuelos_df.groupby('fecha').size().reset_index(name='cantidad')
        
        fig = px.line(
            vuelos_por_dia,
            x='fecha',
            y='cantidad',
            markers=True
        )
        fig.update_traces(
            line_color='#2563EB',
            marker=dict(size=8, color='#2563EB')
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Fecha",
            yaxis_title="Número de Vuelos"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No hay datos suficientes para mostrar gráficos.")

# ------------------------------------------------------------
# VUELOS
# ------------------------------------------------------------
elif opcion == "✈️ Vuelos":
    st.title("✈️ Gestión de Vuelos")
    st.markdown("**Administración completa de operaciones de vuelo**")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["➕ Nuevo Vuelo", "📋 Lista de Vuelos", "🔍 Búsqueda"])

    with tab1:
        st.subheader("Registrar Nuevo Vuelo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("📅 Fecha del vuelo", value=date.today())
            origen = st.text_input("🛫 Aeropuerto de origen", placeholder="Ej: MEX, JFK, MAD")
            num_pasajeros = st.number_input("👥 Número de pasajeros", min_value=0, max_value=500, value=150)
        
        with col2:
            estado = st.selectbox("📊 Estado del vuelo", ["En curso", "Completado", "Cancelado"])
            destino = st.text_input("🛬 Aeropuerto de destino", placeholder="Ej: LAX, CDG, BOG")
            st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ Registrar Vuelo", use_container_width=True):
            if origen and destino:
                ejecutar_query(
                    "INSERT INTO vuelos (fecha, origen, destino, num_pasajeros, estado) VALUES (?, ?, ?, ?, ?)",
                    (fecha, origen.upper(), destino.upper(), num_pasajeros, estado)
                )
                st.success(f"✅ Vuelo {origen} → {destino} registrado correctamente")
                st.rerun()
            else:
                st.error("⚠️ Por favor completa todos los campos obligatorios")

    with tab2:
        st.subheader("Lista Completa de Vuelos")
        vuelos_df = cargar_datos("vuelos")
        
        if not vuelos_df.empty:
            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                estado_filter = st.multiselect("Estado", vuelos_df['estado'].unique(), default=vuelos_df['estado'].unique())
            with col2:
                origen_filter = st.multiselect("Origen", vuelos_df['origen'].unique())
            with col3:
                destino_filter = st.multiselect("Destino", vuelos_df['destino'].unique())
            
            # Aplicar filtros
            df_filtered = vuelos_df.copy()
            df_filtered = df_filtered[df_filtered['estado'].isin(estado_filter)]
            if origen_filter:
                df_filtered = df_filtered[df_filtered['origen'].isin(origen_filter)]
            if destino_filter:
                df_filtered = df_filtered[df_filtered['destino'].isin(destino_filter)]
            
            st.dataframe(
                df_filtered.sort_values('fecha', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Botón de descarga
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Descargar CSV",
                csv,
                "vuelos.csv",
                "text/csv"
            )
        else:
            st.info("📭 No hay vuelos registrados todavía")

    with tab3:
        st.subheader("Búsqueda Avanzada")
        
        search_id = st.number_input("ID del vuelo", min_value=1, step=1)
        
        if st.button("🔍 Buscar"):
            vuelos_df = cargar_datos("vuelos")
            resultado = vuelos_df[vuelos_df['id_vuelo'] == search_id]
            
            if not resultado.empty:
                st.success("✅ Vuelo encontrado")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("⚠️ No se encontró ningún vuelo con ese ID")

# ------------------------------------------------------------
# PASAJEROS
# ------------------------------------------------------------
elif opcion == "👤 Pasajeros":
    st.title("👤 Gestión de Pasajeros")
    st.markdown("**Registro y control de pasajeros**")
    st.markdown("---")

    tab1, tab2 = st.tabs(["➕ Nuevo Pasajero", "📋 Lista de Pasajeros"])

    with tab1:
        st.subheader("Registrar Nuevo Pasajero")
        
        vuelos_df = cargar_datos("vuelos")
        
        if vuelos_df.empty:
            st.warning("⚠️ Primero deben existir vuelos registrados")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                vuelo_options = vuelos_df.apply(
                    lambda x: f"ID {x['id_vuelo']} - {x['origen']} → {x['destino']} ({x['fecha']})", 
                    axis=1
                )
                vuelo_selected = st.selectbox("✈️ Vuelo asignado", vuelo_options)
                vuelo_id = int(vuelo_selected.split()[1])
                
                nombre = st.text_input("👤 Nombre completo", placeholder="Ej: Juan Pérez García")
            
            with col2:
                ticket = st.text_input("🎫 Número de ticket", placeholder="Ej: TCK-12345")
                edad = st.number_input("📅 Edad", min_value=0, max_value=120, value=30)
            
            if st.button("✅ Registrar Pasajero", use_container_width=True):
                if nombre and ticket:
                    ejecutar_query(
                        "INSERT INTO pasajeros (vuelo_id, ticket, nombre, edad) VALUES (?, ?, ?, ?)",
                        (vuelo_id, ticket, nombre, edad)
                    )
                    st.success(f"✅ Pasajero {nombre} registrado correctamente")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor completa todos los campos")

    with tab2:
        st.subheader("Lista de Pasajeros")
        pasajeros_df = cargar_datos("pasajeros")
        
        if not pasajeros_df.empty:
            # Búsqueda
            search = st.text_input("🔍 Buscar por nombre o ticket", placeholder="Escribe para buscar...")
            
            if search:
                df_filtered = pasajeros_df[
                    pasajeros_df['nombre'].str.contains(search, case=False, na=False) |
                    pasajeros_df['ticket'].str.contains(search, case=False, na=False)
                ]
            else:
                df_filtered = pasajeros_df
            
            st.dataframe(
                df_filtered.sort_values('id_pasajero', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Estadísticas
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Pasajeros", len(pasajeros_df))
            col2.metric("Edad Promedio", f"{pasajeros_df['edad'].mean():.1f} años")
            col3.metric("Edad Mediana", f"{pasajeros_df['edad'].median():.0f} años")
        else:
            st.info("📭 No hay pasajeros registrados")

# ------------------------------------------------------------
# TRÁNSITO
# ------------------------------------------------------------
elif opcion == "🔄 Tránsito":
    st.title("🔄 Pasajeros en Tránsito")
    st.markdown("**Monitoreo de flujo de pasajeros**")
    st.markdown("---")

    tab1, tab2 = st.tabs(["➕ Nuevo Registro", "📊 Visualización"])

    with tab1:
        st.subheader("Registrar Tránsito")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("📅 Fecha", value=date.today())
            aeropuerto = st.text_input("🏢 Código de aeropuerto", placeholder="Ej: MEX, JFK")
        
        with col2:
            num_pasajeros = st.number_input("👥 Número de pasajeros", min_value=0, value=100)
        
        if st.button("✅ Registrar", use_container_width=True):
            if aeropuerto:
                ejecutar_query(
                    "INSERT INTO pasajeros_transito (fecha, aeropuerto, num_pasajeros) VALUES (?, ?, ?)",
                    (fecha, aeropuerto.upper(), num_pasajeros)
                )
                st.success("✅ Registro añadido correctamente")
                st.rerun()
            else:
                st.error("⚠️ Por favor ingresa el código del aeropuerto")

    with tab2:
        st.subheader("Análisis de Tránsito")
        transito_df = cargar_datos("pasajeros_transito")
        
        if not transito_df.empty:
            # Gráfico por aeropuerto
            transito_por_aeropuerto = transito_df.groupby('aeropuerto')['num_pasajeros'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=transito_por_aeropuerto.values,
                y=transito_por_aeropuerto.index,
                orientation='h',
                labels={'x': 'Pasajeros', 'y': 'Aeropuerto'},
                color=transito_por_aeropuerto.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de datos
            st.dataframe(
                transito_df.sort_values('fecha', ascending=False),
                use_container_width=True,
                height=300
            )
        else:
            st.info("📭 No hay registros de tránsito")

# ------------------------------------------------------------
# ANÁLISIS
# ------------------------------------------------------------
elif opcion == "📊 Análisis":
    st.title("📊 Análisis y Reportes")
    st.markdown("**Insights y estadísticas detalladas**")
    st.markdown("---")

    vuelos_df = cargar_datos("vuelos")
    pasajeros_df = cargar_datos("pasajeros")
    transito_df = cargar_datos("pasajeros_transito")

    if not vuelos_df.empty:
        # Análisis temporal
        st.subheader("📅 Análisis Temporal")
        
        vuelos_df['fecha'] = pd.to_datetime(vuelos_df['fecha'])
        vuelos_df['mes'] = vuelos_df['fecha'].dt.to_period('M').astype(str)
        vuelos_df['dia_semana'] = vuelos_df['fecha'].dt.day_name()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Por mes
            vuelos_mes = vuelos_df.groupby('mes').size()
            fig = px.bar(
                x=vuelos_mes.index, 
                y=vuelos_mes.values, 
                labels={'x': 'Mes', 'y': 'Vuelos'},
                title="Vuelos por Mes"
            )
            fig.update_traces(marker_color='#2563EB')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Por día de la semana
            dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            vuelos_dia = vuelos_df['dia_semana'].value_counts().reindex(dias_orden, fill_value=0)
            
            fig = px.bar(
                x=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                y=vuelos_dia.values,
                labels={'x': 'Día', 'y': 'Vuelos'},
                title="Vuelos por Día de la Semana"
            )
            fig.update_traces(marker_color='#10B981')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        # Análisis de aeropuertos
        st.subheader("🌍 Análisis de Aeropuertos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🛫 Top Orígenes**")
            top_origenes = vuelos_df['origen'].value_counts().head(10)
            for i, (aeropuerto, cantidad) in enumerate(top_origenes.items(), 1):
                st.write(f"{i}. **{aeropuerto}**: {cantidad} vuelos")
        
        with col2:
            st.markdown("**🛬 Top Destinos**")
            top_destinos = vuelos_df['destino'].value_counts().head(10)
            for i, (aeropuerto, cantidad) in enumerate(top_destinos.items(), 1):
                st.write(f"{i}. **{aeropuerto}**: {cantidad} vuelos")

        # Mapa de calor de ocupación
        st.subheader("🔥 Análisis de Ocupación")
        
        ocupacion_stats = vuelos_df.groupby('estado')['num_pasajeros'].agg(['mean', 'sum', 'count'])
        ocupacion_stats.columns = ['Promedio', 'Total', 'Cantidad']
        ocupacion_stats = ocupacion_stats.round(1)
        
        st.dataframe(ocupacion_stats, use_container_width=True)

        # Exportar reporte completo
        st.markdown("---")
        st.subheader("📥 Exportar Reportes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_vuelos = vuelos_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📄 Vuelos (CSV)",
                csv_vuelos,
                "reporte_vuelos.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            if not pasajeros_df.empty:
                csv_pasajeros = pasajeros_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "👤 Pasajeros (CSV)",
                    csv_pasajeros,
                    "reporte_pasajeros.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col3:
            if not transito_df.empty:
                csv_transito = transito_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "🔄 Tránsito (CSV)",
                    csv_transito,
                    "reporte_transito.csv",
                    "text/csv",
                    use_container_width=True
                )

    else:
        st.info("📊 No hay suficientes datos para generar análisis")

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------
elif opcion == "⚙️ Configuración":
    st.title("⚙️ Configuración del Sistema")
    st.markdown("**Ajustes y mantenimiento**")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🗄️ Base de Datos", "📊 Estadísticas", "ℹ️ Información"])

    with tab1:
        st.subheader("Gestión de Base de Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔄 Regenerar Datos de Ejemplo**")
            st.info("Esto eliminará todos los datos actuales y generará nuevos datos de prueba.")
            
            if st.button("🔄 Regenerar Datos", type="primary"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("DELETE FROM pasajeros")
                c.execute("DELETE FROM pasajeros_transito")
                c.execute("DELETE FROM vuelos")
                conn.commit()
                conn.close()
                generar_datos_ejemplo()
                st.success("✅ Datos regenerados exitosamente")
                st.rerun()
        
        with col2:
            st.markdown("**🗑️ Limpiar Base de Datos**")
            st.warning("⚠️ Esta acción eliminará TODOS los datos permanentemente.")
            
            confirmar = st.checkbox("Confirmo que quiero eliminar todos los datos")
            if st.button("🗑️ Limpiar Todo", disabled=not confirmar):
                conn = get_connection()
                c = conn.cursor()
                c.execute("DELETE FROM pasajeros")
                c.execute("DELETE FROM pasajeros_transito")
                c.execute("DELETE FROM vuelos")
                conn.commit()
                conn.close()
                st.success("✅ Base de datos limpiada")
                st.rerun()

    with tab2:
        st.subheader("Estadísticas del Sistema")
        
        vuelos_df = cargar_datos("vuelos")
        pasajeros_df = cargar_datos("pasajeros")
        transito_df = cargar_datos("pasajeros_transito")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Vuelos", len(vuelos_df))
            st.metric("✅ Completados", len(vuelos_df[vuelos_df['estado'] == 'Completado']) if not vuelos_df.empty else 0)
        
        with col2:
            st.metric("👥 Total Pasajeros", len(pasajeros_df))
            st.metric("📍 Registros Tránsito", len(transito_df))
        
        with col3:
            if not vuelos_df.empty:
                st.metric("🌍 Aeropuertos Origen", vuelos_df['origen'].nunique())
                st.metric("🎯 Aeropuertos Destino", vuelos_df['destino'].nunique())
        
        # Resumen detallado
        st.markdown("---")
        st.markdown("**📋 Resumen Detallado**")
        
        if not vuelos_df.empty:
            resumen = {
                "Categoría": ["Vuelos Totales", "Vuelos en Curso", "Vuelos Completados", "Vuelos Cancelados", 
                             "Pasajeros Totales", "Pasajeros en Tránsito"],
                "Cantidad": [
                    len(vuelos_df),
                    len(vuelos_df[vuelos_df['estado'] == 'En curso']),
                    len(vuelos_df[vuelos_df['estado'] == 'Completado']),
                    len(vuelos_df[vuelos_df['estado'] == 'Cancelado']),
                    len(pasajeros_df),
                    transito_df['num_pasajeros'].sum() if not transito_df.empty else 0
                ]
            }
            st.dataframe(pd.DataFrame(resumen), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Información del Sistema")
        
        st.markdown("""
        ### 📱 Sistema de Gestión Aeroportuaria v2.0
        
        **Características principales:**
        - ✅ Gestión completa de vuelos
        - ✅ Registro de pasajeros
        - ✅ Monitoreo de tránsito
        - ✅ Análisis y reportes
        - ✅ Exportación de datos
        - ✅ Interfaz moderna y responsive
        
        **Tecnologías utilizadas:**
        - 🐍 Python 3.x
        - 📊 Streamlit
        - 🗄️ SQLite
        - 📈 Plotly
        - 🐼 Pandas
        
        **Desarrollado con** ❤️ **para gestión aeroportuaria eficiente**
        
        ---
        
        ### 📞 Soporte
        Para consultas o reportar problemas, contacta al administrador del sistema.
        
        ### 📝 Notas de la versión 2.0
        - Interfaz completamente rediseñada
        - Nuevas visualizaciones interactivas
        - Mejoras en rendimiento
        - Sistema de búsqueda mejorado
        - Exportación de reportes
        """)
        
        st.markdown("---")
        st.info(f"💻 Sistema en ejecución | 📅 Fecha: {date.today().strftime('%d/%m/%Y')}")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748B; padding: 2rem 0;'>
        <p>Sistema de Gestión Aeroportuaria v2.0 | Desarrollado con Streamlit</p>
        <p style='font-size: 0.875rem;'>© 2024 - Todos los derechos reservados</p>
    </div>
    """,
    unsafe_allow_html=True
)
