
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Ecommerce Analyzer", layout="centered")

st.title("🔍 Ecommerce Analyzer")
st.markdown("Analizza un sito ecommerce e ottieni insight utili in pochi secondi.")

url = st.text_input("Inserisci l'URL del sito ecommerce", "https://")

if st.button("Analizza"):
    if url.startswith("http"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "Nessun titolo trovato"
            description = soup.find("meta", attrs={"name": "description"})
            description = description["content"] if description else "Nessuna descrizione trovata"

            st.success("Analisi completata ✅")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta description:** {description}")
            st.markdown("---")
            st.info("🚀 Versione demo — Per report avanzati integra pixel, SEO, velocità, tracciamenti e ADV.")

        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")
    else:
        st.warning("Inserisci un URL valido.")
