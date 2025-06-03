
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Page config
st.set_page_config(page_title="Ecommerce Analyzer", layout="wide")

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #87CEFA, #1E90FF);
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True
)

# Login section
st.title("🔒 Login Fuzzy Marketing")
email = st.text_input("Inserisci la tua email aziendale", "")
if not email:
    st.stop()

# Main application
st.title("🔍 Ecommerce Analyzer by Fuzzy Marketing")
st.markdown(f"Benvenuto, **{email}**")
st.markdown("---")

# URL input
url = st.text_input("Inserisci l'URL del sito ecommerce da analizzare", "https://")
if st.button("Analizza"):
    if url.startswith("http"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            # Basic analysis
            title = soup.title.string if soup.title else "Nessun titolo trovato"
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = description_tag["content"] if description_tag else "Nessuna descrizione trovata"
            # Check for CTA buttons
            ctas = soup.find_all("a")
            cta_texts = [a.text.strip() for a in ctas if a.text.strip()]
            # Display results
            st.success("Analisi completata ✅")
            st.markdown(f"**Titolo Pagina:** {title}")
            st.markdown(f"**Meta Description:** {description}")
            st.markdown("**Esempi di CTA trovate:**")
            if cta_texts:
                for text in cta_texts[:5]:
                    st.write(f"- {text}")
            else:
                st.write("Nessuna CTA trovata.")
            st.markdown("---")
        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")
    else:
        st.warning("Inserisci un URL valido.")

st.markdown("---")

# Chat section
st.subheader("💬 Chat Assistenza Fuzzy: risposte a obiezioni")
try:
    msg = st.text_input("Scrivi l'obiezione ricevuta dal cliente")
    if msg:
        # Dummy responses based on keywords
        msg_lower = msg.lower()
        if "prezzo" in msg_lower:
            response_text = "Capisco la tua preoccupazione sul prezzo. Il pacchetto front-end da 350€ include 2 ore di intervento personalizzato con un nostro esperto."
        elif "tempo" in msg_lower:
            response_text = "Il progetto richiede in media 2 ore per l'intervento tecnico. Possiamo concordare una data a te comoda."
        else:
            response_text = "Grazie per il tuo feedback. Il nostro pacchetto front-end risolve problemi tecnici e strategici fondamentali per il tuo eCommerce."
        st.info(response_text)
except Exception as e:
    st.error(f"Errore nella sezione chat: {e}")
