import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="OscarED - Tu guía de películas premiadas",
    page_icon="🎬",
    layout="wide"
)

# Configurar API Key y modelo
def init_gemini():
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("""
            ⚠️ No se encontró la API key en las variables de entorno.
            
            Por favor, asegúrate de:
            1. Tener un archivo .env en el directorio del proyecto
            2. Que el archivo .env contenga la variable GEMINI_API_KEY
            3. Que la API key sea válida
            """)
            return False
            
        genai.configure(api_key=api_key)
        
        # Verificar que el modelo está disponible usando el modelo Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        return True
    except Exception as e:
        st.error(f"""
        ⚠️ Error al inicializar Gemini AI: {str(e)}
        
        Si estás viendo este error, es posible que:
        1. La API key no sea válida
        2. No tengas acceso al modelo de Gemini
        3. Haya un problema de conexión
        
        Por favor, verifica que:
        1. Has habilitado la API de Gemini en tu proyecto de Google Cloud
        2. Tu API key tiene los permisos necesarios
        3. Tienes una conexión estable a internet
        """)
        return False

# Inicializar Gemini
gemini_initialized = init_gemini()

# Función para convertir texto a Pascal Case
def to_pascal_case(text):
    # Dividir el texto en palabras y capitalizar cada una
    words = text.lower().split()
    return ' '.join(word.capitalize() for word in words)

# Función para obtener la URL de la imagen de IMDB
def get_imdb_image(movie_name):
    try:
        # Buscar la película en IMDB
        search_url = f"https://www.imdb.com/find?q={movie_name.replace(' ', '+')}&s=tt&ttype=ft"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar el primer resultado de película
        first_result = soup.find('a', href=re.compile(r'/title/tt\d+/'))
        if first_result:
            movie_url = f"https://www.imdb.com{first_result['href']}"
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
            
            # Buscar la imagen de portada
            poster = movie_soup.find('img', class_='ipc-image')
            if poster and 'src' in poster.attrs:
                return poster['src']
    except Exception as e:
        print(f"Error getting IMDB image: {str(e)}")
    return None

# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Estilos generales */
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Contenedor principal */
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Estilos del título principal */
    h1 {
        color: #FFD700 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Estilos para subtítulos */
    h2, h3, h4 {
        color: #FFD700 !important;
        margin: 1.5rem 0 !important;
        font-weight: 600 !important;
    }
    
    /* Estilos para botones */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFC000) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        background: linear-gradient(45deg, #FFC000, #FFD700) !important;
    }
    
    /* Estilos para el campo de búsqueda */
    .stTextInput > div {
        width: 100% !important;
    }
    
    .stTextInput > div > div {
        background-color: transparent !important;
    }
    
    .stTextInput > div > div > input {
        background-color: transparent !important;
        color: #ffffff !important;
        border: 2px solid #FFD700 !important;
        border-radius: 30px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFC000 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2) !important;
        background-color: rgba(255, 215, 0, 0.05) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Estilos para el spinner */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }
    
    /* Estilos para mensajes de advertencia */
    .stAlert {
        background-color: rgba(255, 215, 0, 0.1) !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        border-radius: 10px !important;
    }
    
    /* Estilos para divisores */
    hr {
        border-color: rgba(255, 215, 0, 0.1) !important;
        margin: 2rem 0 !important;
    }
    
    /* Estilos para listas */
    ul {
        list-style-type: none !important;
        padding-left: 0 !important;
    }
    
    li {
        margin: 0.5rem 0 !important;
        color: #ffffff !important;
    }
    
    /* Estilos para el contenedor de resultados */
    .results-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 215, 0, 0.2);
        line-height: 1.4;
        font-size: 1rem;
    }
    
    .results-container h1 {
        font-size: 2rem !important;
        margin: 1rem 0 !important;
        color: #FFD700 !important;
        text-align: center !important;
    }
    
    .results-section {
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
    }
    
    .results-section:last-child {
        margin-bottom: 0;
        padding-bottom: 0;
        border-bottom: none;
    }
    
    .section-title {
        color: #FFD700;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
        font-weight: 600;
    }
    
    .section-content {
        color: #ffffff;
        margin-left: 1rem;
        font-size: 1rem;
        line-height: 1.4;
    }
    
    .bullet-point {
        color: #FFD700;
        margin-right: 0.3rem;
    }

    .section-content span.bullet-point {
        display: inline-block;
    }

    .section-content > *:not(:first-child) {
        margin-top: 0.4rem;
    }

    /* Contenedor para elementos con bullets */
    .bullet-container {
        display: block;
        margin-top: 0.4rem;
    }

    .bullet-container:first-child {
        margin-top: 0;
    }

    .movie-poster {
        text-align: center;
        margin: 1rem 0;
    }
    
    .movie-poster img {
        max-width: 300px;
        margin: 0 auto;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    
    /* Ocultar el mensaje "press enter to apply" */
    .stTextInput div[data-baseweb="base-input"] {
        width: 100% !important;
    }
    
    .stTextInput div[data-baseweb="base-input"] + div {
        display: none !important;
    }
    
    /* Estilos específicos para los premios */
    .awards-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .award-item {
        background: rgba(255, 215, 0, 0.05);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        border-left: 3px solid #FFD700;
    }
    
    .award-year {
        color: #FFD700;
        font-weight: bold;
        margin-right: 0.5rem;
    }

    .no-awards {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        font-style: italic;
        color: rgba(255, 255, 255, 0.8);
    }

    .nomination {
        border-left-color: #C0C0C0;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para obtener información de una película
def obtener_info_pelicula(nombre_pelicula):
    try:
        # Configuración básica del modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convertir el nombre de la película a Pascal Case
        nombre_pelicula_pascal = to_pascal_case(nombre_pelicula)

        prompt = f"""Proporciona información sobre la película '{nombre_pelicula}' en el siguiente formato exacto, sin incluir marcadores de código ni formato markdown. La información debe ser concisa y directa.

Para la sección de premios, sigue estas reglas:
1. Si la película ganó premios, muestra cada premio en su propio award-item
2. Si la película solo tuvo nominaciones, muestra las nominaciones con la clase 'award-item nomination'
3. Si la película no ganó ni fue nominada a ningún premio importante, muestra el mensaje en un div con clase 'no-awards'

<h1>🎬 {nombre_pelicula_pascal}</h1>

<div class='movie-poster'>
[POSTER_PLACEHOLDER]
</div>

<div class='results-section'>
<div class='section-title'>📝 SINOPSIS</div>
<div class='section-content'>[Breve sinopsis de máximo 3 líneas]</div>
</div>

<div class='results-section'>
<div class='section-title'>🏆 PREMIOS Y NOMINACIONES</div>
<div class='section-content'>
<div class='awards-list'>
[Si ganó premios, usar este formato para cada premio:]
<div class='award-item'>
<span class='award-year'>[Año]</span> [Premio] a [Categoría] - Ganador
</div>

[Si solo tuvo nominaciones, usar este formato:]
<div class='award-item nomination'>
<span class='award-year'>[Año]</span> Nominación al [Premio] por [Categoría]
</div>

[Si no tuvo premios ni nominaciones, usar este formato:]
<div class='no-awards'>
Esta película no recibió nominaciones ni premios destacados en las principales ceremonias de premiación.
</div>
</div>
</div>
</div>

<div class='results-section'>
<div class='section-title'>⭐ VALORACIÓN</div>
<div class='section-content'>
<div class='bullet-container'>
<span class='bullet-point'>•</span> IMDB: [puntuación]/10
</div>
<div class='bullet-container'>
<span class='bullet-point'>•</span> Crítica: [resumen en una línea]
</div>
</div>
</div>

<div class='results-section'>
<div class='section-title'>🎥 PRODUCCIÓN</div>
<div class='section-content'>
<div class='bullet-container'>
<span class='bullet-point'>•</span> Director: [nombre]
</div>
<div class='bullet-container'>
<span class='bullet-point'>•</span> Elenco: [principales actores]
</div>
<div class='bullet-container'>
<span class='bullet-point'>•</span> Año: [año] | Duración: [duración]
</div>
</div>
</div>

<div class='results-section'>
<div class='section-title'>🌟 DATOS CURIOSOS</div>
<div class='section-content'>
<div class='bullet-container'>
<span class='bullet-point'>•</span> [Dato más relevante]
</div>
<div class='bullet-container'>
<span class='bullet-point'>•</span> [Segundo dato más interesante]
</div>
</div>
</div>"""

        # Generar respuesta con manejo de errores mejorado
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                # Limpiar el formato del texto
                texto_limpio = response.text.strip()
                # Eliminar cualquier delimitador de código
                texto_limpio = texto_limpio.replace("```html", "").replace("```", "")
                
                # Obtener la URL de la imagen de IMDB
                poster_url = get_imdb_image(nombre_pelicula)
                if poster_url:
                    # Reemplazar el placeholder con la imagen
                    img_html = f"<img src='{poster_url}' alt='Poster de {nombre_pelicula_pascal}' style='max-width: 300px; margin: 20px auto; display: block; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.5);'>"
                    texto_limpio = texto_limpio.replace("[POSTER_PLACEHOLDER]", img_html)
                else:
                    # Si no se encuentra la imagen, eliminar el placeholder
                    texto_limpio = texto_limpio.replace("[POSTER_PLACEHOLDER]", "")
                
                return texto_limpio
            else:
                return "Lo siento, no pude generar información para esta película. Por favor, intenta con otra película."
        except Exception as generate_error:
            return f"Error al generar contenido: {str(generate_error)}"

    except Exception as e:
        error_message = str(e)
        if "404" in error_message:
            return """⚠️ Error de Conexión: No se pudo conectar con el servicio de IA.
                     Por favor, verifica tu conexión a internet e inténtalo de nuevo."""
        elif "quota" in error_message.lower():
            return """⚠️ Límite de Cuota Alcanzado: 
                     Hemos alcanzado el límite de consultas permitidas. 
                     Por favor, intenta más tarde."""
        else:
            return f"""⚠️ Error Inesperado: {str(e)}
                      Por favor, intenta de nuevo en unos momentos."""

# Header y descripción principal
st.title("🎬 OscarED – Tu guía de películas premiadas")
st.markdown("""
    <div style='text-align: center; max-width: 800px; margin: 0 auto; padding: 1rem;'>
    <p style='color: #ffffff; font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem;'>
    Descubre información detallada sobre las películas más aclamadas de la historia del cine. 
    Utilizamos inteligencia artificial para brindarte datos precisos sobre premios, sinopsis, 
    críticas y mucho más.</p>
    </div>
    """, unsafe_allow_html=True)

# Sección principal de búsqueda
st.markdown("<h2 style='text-align: center; color: #FFD700; margin-bottom: 2rem;'>🔍 Buscar Película</h2>", unsafe_allow_html=True)

# Contenedor centrado para la búsqueda
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Crear una clave única para el estado de la búsqueda anterior
    if 'previous_search' not in st.session_state:
        st.session_state.previous_search = ""
    
    # Input de búsqueda
    pelicula = st.text_input(
        "Nombre de la película",
        placeholder="Ingresa el nombre de una película...",
        label_visibility="collapsed",
        key="movie_input"
    )
    
    # Detectar si se presionó Enter (el texto cambió)
    search_triggered = pelicula != st.session_state.previous_search
    st.session_state.previous_search = pelicula
    
    buscar = st.button("🔍 Buscar Información", use_container_width=True, key="search_button")

# Procesamiento de la búsqueda
if buscar or (search_triggered and pelicula):  # Buscar si se presiona el botón o Enter
    if not gemini_initialized:
        st.error("⚠️ No se puede realizar la búsqueda porque el servicio de IA no está disponible.")
    elif not pelicula:
        st.warning("⚠️ Por favor, ingresa el nombre de una película para comenzar la búsqueda.")
    else:
        with st.spinner("🎬 Analizando la película..."):
            resultado = obtener_info_pelicula(pelicula)
        st.markdown("<h3 style='text-align: center; color: #FFD700; margin: 2rem 0;'>📌 Resultados del Análisis</h3>", unsafe_allow_html=True)
        st.markdown(f"""<div class='results-container'>{resultado}</div>""", unsafe_allow_html=True)

# Sección "Cómo Funciona"
st.markdown("<h2 style='text-align: center; color: #FFD700; margin: 3rem 0 2rem;'>🛠️ ¿Cómo Funciona?</h2>", unsafe_allow_html=True)

# Contenedor centrado para las características
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='color: #ffffff; font-size: 1.1rem; line-height: 1.6;'>
        <div style='margin-bottom: 2rem;'>
            <h4 style='color: #FFD700; margin-bottom: 1rem;'>🔍 Búsqueda Inteligente</h4>
            <ul>
                <li>• Ingresa el nombre de cualquier película</li>
                <li>• Análisis instantáneo con IA avanzada</li>
                <li>• Resultados detallados en segundos</li>
            </ul>
        </div>
        
        <div style='margin-bottom: 2rem;'>
            <h4 style='color: #FFD700; margin-bottom: 1rem;'>📊 Información Completa</h4>
            <ul>
                <li>• Sinopsis detallada</li>
                <li>• Premios y nominaciones</li>
                <li>• Calificaciones y críticas</li>
                <li>• Datos de producción</li>
                <li>• Curiosidades exclusivas</li>
            </ul>
        </div>
        
        <div>
            <h4 style='color: #FFD700; margin-bottom: 1rem;'>✨ Fuentes Confiables</h4>
            <ul>
                <li>• Información verificada</li>
                <li>• Base de datos actualizada</li>
                <li>• Análisis preciso con IA</li>
            </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)

# Footer simple
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
    <p style='color: rgba(255, 255, 255, 0.7); margin-bottom: 0.5rem;'>
        Desarrollado con <span style='color: #FF6B6B;'>❤️</span> por MarraTX usando Streamlit y Gemini AI
    </p>
    <p style='color: rgba(255, 255, 255, 0.5);'>
        © 2024 OscarED - Tu guía definitiva del cine premiado
    </p>
    </div>
    """, unsafe_allow_html=True)
