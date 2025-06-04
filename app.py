
import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# Import OpenAI if available
try:
    import openai
except ImportError:
    openai = None

# Imposta il layout
st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="wide")

# Sfondo sfumato blu
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    input, textarea, button, .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.9) !important;
        color: black !important;
    }
    .stButton>button {
        background-color: #0d3b66;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Gestione login via session state
if 'email' not in st.session_state:
    st.session_state['email'] = None

if st.session_state['email'] is None:
    st.title("Fuzzy Marketing - Ecommerce Analyzer")
    st.caption("Inserisci la tua email per iniziare:")
    email = st.text_input("", placeholder="es. nome@azienda.it", key="inp_email")
    if st.button("Accedi"):
        if email and "@" in email:
            st.session_state['email'] = email
            # Compatibilità con versioni diverse di Streamlit
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.rerun()
        else:
            st.error("Inserisci un indirizzo email valido.")
    st.stop()

# Dopo login
st.title("Fuzzy Marketing - Ecommerce Analyzer")
st.write(f"Benvenuto, {st.session_state['email']}!")

st.markdown("### 🔍 Analisi Completa del Sito eCommerce")
url = st.text_input("URL Home Page:", placeholder="https://")

if st.button("Analizza Sito"):
    if url.startswith("http"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            # Titolo e meta description
            title = soup.title.string if soup.title else "Nessun titolo trovato"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            desc = meta_desc["content"] if meta_desc else "Nessuna meta description trovata"

            # Conteggio intestazioni
            h1 = len(soup.find_all("h1"))
            h2 = len(soup.find_all("h2"))
            # Check footer
            footer = soup.find("footer")
            footer_info = "Trovato" if footer else "Non trovato"

            st.success("Analisi completata ✅")
            st.markdown(f"**Titolo Pagina:** {title}")
            st.markdown(f"**Meta Description:** {desc}")
            st.markdown(f"- Numero di tag H1: {h1}")
            st.markdown(f"- Numero di tag H2: {h2}")
            st.markdown(f"- Sezione Footer: {footer_info}")
            # Suggerimenti
            st.markdown("**Suggerimenti:**")
            st.markdown("- Assicurati di avere almeno un tag H1 descrittivo.")
            if not meta_desc:
                st.markdown("- Aggiungi una meta description unica per migliorare la SEO.")
            if not footer:
                st.markdown("- Crea un footer con link utili e informazioni di contatto.")
        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")
    else:
        st.warning("Inserisci un URL valido.")

st.markdown("---")

# Chat interattiva GPT
st.markdown("### 💬 Chat Interattiva con Assistente Fuzzy (GPT-4)")
if openai is None:
    st.warning("OpenAI non è installato. Installa `openai` per abilitare la chat.")
elif "OPENAI_API_KEY" not in os.environ:
    st.info("Per usare la chat, imposta la variabile d'ambiente `OPENAI_API_KEY`.")
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    user_input = st.text_input("Scrivi qualcosa per l'assistente:")
    if st.button("Invia al Chatbot"):
        if user_input:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=150
                )
                reply = completion.choices[0].message.content
                st.markdown(f"**Assistente:** {reply}")
            except Exception as e:
                st.error(f"Errore dalla API ChatGPT: {e}")
        else:
            st.warning("Scrivi un messaggio da inviare.")
