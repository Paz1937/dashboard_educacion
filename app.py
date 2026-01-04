import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image  # Librería para manejar imágenes

# 1. Configuración de la página (esto siempre debe ir primero)
st.set_page_config(page_title="Secretaría de Educación - Capital Humano", layout="wide")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* 1. Fondo principal y barra lateral */
    .stApp {
        background-color: #1a1a4b; /* Azul profundo institucional */
        color: white;
    }
    
    /* 2. Estilo de los Botones (Grandes y Azules) */
    div.stButton > button {
        background-color: #2b2b8c;
        color: white;
        border-radius: 15px;
        height: 120px; /* Aumentamos la altura */
        font-size: 20px; /* Letra más grande */
        font-weight: bold;
        border: 2px solid #3d3dcf;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }

    /* 3. Efecto al pasar el mouse por el botón */
    div.stButton > button:hover {
        background-color: #3d3dcf;
        border-color: #ffffff;
        transform: scale(1.02); /* Efecto de crecimiento leve */
    }

    /* 4. Estilo de las métricas */
    [data-testid="stMetricValue"] {
        color: #00ffcc; /* Color llamativo para los números */
        font-size: 40px;
    }
    
    /* 5. Títulos en blanco */
    h1, h2, h3, p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)



# 2. Cargar y mostrar el logo
# Al estar en la misma carpeta, solo necesitas el nombre del archivo
try:
    logo = Image.open("logo_SE_CH.png")
    
    # Puedes mostrarlo en la columna central para que luzca institucional
    col_log1, col_log2, col_log3 = st.columns([1, 2, 1])
    with col_log2:
        st.image(logo, use_container_width=True)
except FileNotFoundError:
    st.error("No se encontró el archivo del logo. Verifica que el nombre sea exacto.")

# 3. Títulos institucionales
st.markdown("<h1 style='text-align: center;'>Dirección Nacional de Políticas de Fortalecimiento Educativo</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Ministerio de Capital Humano</h3>", unsafe_allow_html=True)

st.divider()

# Título de la sección
st.write("### Seleccione un Programa para visualizar")

# Creamos la cuadrícula de botones (4 columnas como en tu imagen)
fila1_col1, fila1_col2, fila1_col3, fila1_col4 = st.columns(4)
fila2_col1, fila2_col2, fila2_col3, fila2_col4 = st.columns(4)

# Lógica de los botones
# Usamos 'session_state' para recordar qué programa se hizo clic
if "programa_seleccionado" not in st.session_state:
    st.session_state.programa_seleccionado = "General"

with fila1_col1:
    if st.button("🎓 Progresar", use_container_width=True):
        st.session_state.programa_seleccionado = "Progresar"

with fila1_col2:
    if st.button("🎫 Vouchers Educativos", use_container_width=True):
        st.session_state.programa_seleccionado = "Vouchers"

with fila1_col3:
    if st.button("❤️ Becas Fortalecimiento", use_container_width=True):
        st.session_state.programa_seleccionado = "Becas"

with fila1_col4:
    if st.button("🍴 Comedores Escolares", use_container_width=True):
        st.session_state.programa_seleccionado = "Comedores"

with fila2_col1:
    if st.button("📖 Libros para aprender", use_container_width=True):
        st.session_state.programa_seleccionado = "Libros"

with fila2_col2:
    if st.button("🧪 Ferias de Ciencia", use_container_width=True):
        st.session_state.programa_seleccionado = "Ferias"

with fila2_col3:
    if st.button("🏆 Olimpiadas", use_container_width=True):
        st.session_state.programa_seleccionado = "Olimpiadas"

st.divider()

# Mostrar información basada en el botón presionado
st.subheader(f"Visualizando: {st.session_state.programa_seleccionado}")

if st.session_state.programa_seleccionado == "Comedores":
    try:
        # Cargar el Excel
        df_comedores = pd.read_excel("Resumen_rondos_comedores.xlsx")
        
        # Limpieza rápida: eliminamos la fila de 'Totales' si existe al final para no deformar los gráficos
        df_comedores = df_comedores[df_comedores['Jurisdicción'] != 'Totales']

        st.info("Datos de Comedores Escolares cargados por Jurisdicción")

        # --- FILTROS ---
        provincias = st.multiselect("Filtrar Provincias:", 
                                   options=df_comedores['Jurisdicción'].unique(),
                                   default=df_comedores['Jurisdicción'].unique())
        
        df_filtrado = df_comedores[df_comedores['Jurisdicción'].isin(provincias)]

        # --- MÉTRICAS RESUMEN ---
        monto_total = df_filtrado['Monto Anual'].sum()
        ejecucion_promedio = df_filtrado['Ejecución Presupuestaria %'].mean()
        
        m1, m2 = st.columns(2)
        m1.metric("Monto Anual Total", f"$ {monto_total:,.0f}")
        m2.metric("Promedio de Ejecución", f"{ejecucion_promedio:.2f}%")

        st.divider()

        # --- LOS 2 GRÁFICOS INTERACTIVOS ---
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.write("#### 💰 Inversión por Jurisdicción")
            # Gráfico de barras horizontales para que se lean mejor los nombres de provincias
            fig1 = px.bar(df_filtrado, 
                          y='Jurisdicción', 
                          x='Monto Anual', 
                          orientation='h',
                          title="Presupuesto Anual Asignado",
                          hover_data=['Organismo provincial responsable'],
                          color='Monto Anual',
                          color_continuous_scale='Blues')
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            st.write("#### 📈 Nivel de Ejecución Presupuestaria")
            # Gráfico de dispersión o burbujas para ver ejecución vs monto
            fig2 = px.scatter(df_filtrado, 
                              x='Ejecución Presupuestaria %', 
                              y='Jurisdicción',
                              size='Monto Anual',
                              color='Ejecución Presupuestaria %',
                              title="% Ejecución por Provincia",
                              color_continuous_scale='RdYlGn', # Rojo a Verde
                              hover_name='Jurisdicción')
            st.plotly_chart(fig2, use_container_width=True)

        # Tabla detallada
        st.write("### Detalle por Organismo Responsable")
        st.dataframe(df_filtrado[['Jurisdicción', 'Organismo provincial responsable', 'Monto Anual', 'Ejecución Presupuestaria %']], 
                     use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer las columnas: {e}. Asegúrate de que los nombres coincidan exactamente con el Excel.")

elif st.session_state.programa_seleccionado == "Vouchers":
    try:
        # Cargamos el Excel sin procesar nombres de columnas primero para evitar el error de str/int
        df_vouchers = pd.read_excel("20251215_VOUCHERS.xlsx", header=1) # Usamos header=1 si la fila 1 son los nombres
        
        # Limpieza: eliminamos filas vacías y la fila de TOTAL
        df_vouchers = df_vouchers.dropna(subset=[df_vouchers.columns[0]])
        df_vouchers = df_vouchers[df_vouchers.iloc[:, 0].str.contains("TOTAL") == False]

        st.info("Visualizando datos de Vouchers Educativos por Nivel")

        # --- EXTRACCIÓN POR POSICIÓN (Basado en tu imagen) ---
        # Columna 0: Jurisdicción
        # Inicial: Col 1(Inst), 2(Alum), 3(Inv)
        # Primario: Col 4(Inst), 5(Alum), 6(Inv)
        # Secundario: Col 7(Inst), 8(Alum), 9(Inv)
        
        # Convertimos a numérico por si hay algún símbolo de "$" o puntos que molesten
        for i in [2, 3, 5, 6, 8, 9]:
            df_vouchers.iloc[:, i] = pd.to_numeric(df_vouchers.iloc[:, i], errors='coerce').fillna(0)

        # Totales calculados
        total_alumnos = df_vouchers.iloc[:, [2, 5, 8]].sum(axis=1)
        total_inversion = df_vouchers.iloc[:, [3, 6, 9]].sum(axis=1)

        # --- MÉTRICAS ---
        v1, v2, v3 = st.columns(3)
        v1.metric("Total Beneficiarios", f"{total_alumnos.sum():,.0f}")
        v2.metric("Inversión Total", f"$ {total_inversion.sum():,.0f}")
        v3.metric("Jurisdicciones", len(df_vouchers))

        st.divider()

        # --- GRÁFICOS ---
        col_v1, col_v2 = st.columns(2)

        with col_v1:
            st.write("#### 🏫 Inversión por Nivel Educativo")
            niveles_data = pd.DataFrame({
                'Nivel': ['Inicial', 'Primario', 'Secundario'],
                'Inversión': [df_vouchers.iloc[:, 3].sum(), 
                              df_vouchers.iloc[:, 6].sum(), 
                              df_vouchers.iloc[:, 9].sum()]
            })
            fig_pie = px.pie(niveles_data, values='Inversión', names='Nivel', 
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_v2:
            st.write("#### 📊 Alumnos por Jurisdicción")
            # Creamos un mini dataframe para el gráfico de barras
            df_barras = pd.DataFrame({
                'Jurisdicción': df_vouchers.iloc[:, 0],
                'Alumnos': total_alumnos
            }).sort_values('Alumnos', ascending=False)
            
            fig_bar = px.bar(df_barras, x='Jurisdicción', y='Alumnos', 
                             color='Alumnos', color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.write("Asegúrate de que el archivo no tenga filas vacías al principio.")
        
elif st.session_state.programa_seleccionado == "Becas":
    try:
        df_becas = pd.read_excel("Becas_Fortaleciemiento.xlsx")
        
        # --- LIMPIEZA AGRESIVA DE COLUMNAS ---
        # Quitamos espacios al principio y al final de los nombres de las columnas
        df_becas.columns = df_becas.columns.str.strip()
        
        # Filtramos la fila de TOTAL
        df_becas = df_becas[df_becas['Jurisdicción'].astype(str).str.contains("TOTAL|Total") == False]

        st.info("Visualizando: Becas de Fortalecimiento Socioeducativo")

        # --- BUSCAR COLUMNAS POR PARTE DEL NOMBRE ---
        # Buscamos la columna que CONTENGA "VG", la que CONTENGA "AP", etc.
        def buscar_col(texto):
            for c in df_becas.columns:
                if texto in c: return c
            return None

        col_vg = buscar_col("VG")
        col_ap = buscar_col("AP")
        col_ai = buscar_col("AI")
        col_mp = buscar_col("MPyCP")
        col_fondos = buscar_col("Fondos")
        col_becarios = buscar_col("Becarios")

        # Verificamos si encontramos las columnas críticas
        if not col_vg or not col_fondos:
            st.error(f"No se encontraron las columnas. Columnas detectadas: {list(df_becas.columns)}")
        else:
            # Convertir a número
            for c in [col_vg, col_ap, col_ai, col_mp, col_fondos, col_becarios]:
                df_becas[c] = pd.to_numeric(df_becas[c], errors='coerce').fillna(0)

            # --- MÉTRICAS ---
            b1, b2 = st.columns(2)
            b1.metric("Monto Total de Fondos", f"$ {df_becas[col_fondos].sum():,.0f}")
            b2.metric("Total de Becarios", f"{df_becas[col_becarios].sum():,.0f}")

            # --- SELECTOR ---
            opciones = {"Becas VG": col_vg, "Becas AP": col_ap, "Becas AI": col_ai, "Becas MPyCP": col_mp}
            seleccion = st.selectbox("Seleccione la línea de beca:", list(opciones.keys()))
            col_activa = opciones[seleccion]

            # --- GRÁFICOS ---
            c_a, c_b = st.columns(2)
            with c_a:
                fig1 = px.bar(df_becas, x='Jurisdicción', y=col_activa, color=col_activa, color_continuous_scale='Viridis')
                st.plotly_chart(fig1, use_container_width=True)
            with c_b:
                fig2 = px.bar(df_becas, x='Jurisdicción', y=col_fondos, color_discrete_sequence=['#00ffcc'])
                st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Error técnico: {e}")