# OscarED - Tu guía de películas premiadas

## Descripción del Proyecto

**OscarED** es una aplicación web desarrollada con **Streamlit** que permite a los usuarios obtener información detallada sobre películas premiadas en eventos como los **Oscar, BAFTA, Cannes** y otros festivales de cine. Utiliza **Gemini AI** para generar contenido preciso y estructurado basado en los datos ingresados por el usuario.

## Características Principales

✅ Búsqueda inteligente de películas mediante IA.  
✅ Información detallada: sinopsis, premios, críticas y datos de producción.  
✅ Estilo visual atractivo con personalización de UI/UX.  
✅ Respuesta rápida gracias a **Gemini AI (Google AI Studio)**.  
✅ Aplicación interactiva con **Streamlit**.

## Tecnologías Utilizadas

- **Python** (para la lógica del servidor)
- **Streamlit** (para la interfaz web)
- **Gemini AI** (para la generación de contenido)
- **HTML & CSS** (para la personalización del diseño)

## Instalación y Ejecución

### 1️⃣ Clonar el Repositorio

```sh
 git clone https://github.com/MarraTX/oscared-AI.git
 cd oscared-AI
```

### 2️⃣ Instalar Dependencias

Asegúrate de tener **Python 3.8+** instalado. Luego, ejecuta:

```sh
 pip install -r requirements.txt
```

### 3️⃣ Configurar API Key de Gemini AI

1. Ve a [Google AI Studio](https://aistudio.google.com/).
2. Crea una API Key en la configuración de tu cuenta.
3. Cópiala y agrégala en `.env` reemplazando `TU_API_KEY`, tal y como se muesta en el .env de ejemplo.

### 4️⃣ Ejecutar la Aplicación

Ejecuta el siguiente comando:

```sh
 streamlit run app.py
```

Esto abrirá la aplicación en tu navegador predeterminado. 🚀

## Uso de la Aplicación

1. Ingresa el nombre de una película en el campo de búsqueda.
2. Presiona el botón "🔍 Buscar Información".
3. Obtén una respuesta detallada con **sinopsis, premios, puntuaciones y datos curiosos**.

## Licencia

Este proyecto está bajo la **Licencia MIT**. Puedes usarlo, modificarlo y distribuirlo libremente.

---

💡 _Si tienes alguna duda o sugerencia, no dudes en contribuir al repositorio._ 😊
