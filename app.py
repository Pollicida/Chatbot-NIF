# Streamlit Libs
import os
import streamlit as st
import fitz
import google.generativeai as genai

# Configurar clave API
GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# Función para extraer texto de un PDF
def extraer_texto(pdf_path):
    texto = ""
    with fitz.open(pdf_path) as doc:
        for pagina in doc:
            texto += pagina.get_text("text") + "\n"
    return texto

# Cargar el contenido del PDF
pdf_texto = extraer_texto("./utils/documento_contabilidad.pdf")

# Inicializar modelo Gemini
model = genai.GenerativeModel("gemini-2.0-flash")

# Título del chatbot
st.title("Chatbot de Contabilidad 📊")

# Inicializar historial del chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
user_input = st.chat_input("Haz una pregunta sobre contabilidad...")

if user_input:
    # Agregar pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Crear el prompt con el contenido del PDF
    prompt = (
        f"Tengo una conversación en proceso, tengo los siguientes mensajes que quiero que recuerdes para que puedas guiar tu respuesta también con ellos."
        f"Te llamas contabot"
        f"Saluda y dí tu nombre al comienzo de la conversación"
        f"Usa el siguiente texto como referencia para responder de forma precisa. "
        f"Si la pregunta tiene que ver con contabilidad pero no puedes encontrar la información en el texto, entonces solo contesta que no estás capacitado para responder la pregunta."
        f"Si la pregunta no tiene nada que ver con contabilidad, contesta de forma amable al usuario pero no le des información externa al texto, sino puedes responder algo coherente con el texto, contesta de forma natural y redirije el tema a la contabilidad"
        f"Si no encuentras información relevante, indica al usuario que no estás capacitado para responder esa pregunta y motivalo a preguntar sobre contabilidad sin revelar que estás usando un texto de referencia:\n\n"
        f"Conversación en curso: {str(st.session_state.messages)}\n\n"
        f"Texto: {pdf_texto}\n\n"
        f"Pregunta del usuario: {user_input}"
    )
    if user_input: 
        with st.chat_message("user"):
            st.markdown(user_input)

    # Obtener respuesta del chatbot
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = "Lo siento, ha ocurrido un error al procesar tu pregunta. Inténtalo de nuevo."

    # Agregar respuesta del chatbot al historial
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Mostrar respuesta en la interfaz
        
    with st.chat_message("assistant"):
        st.markdown(bot_reply)