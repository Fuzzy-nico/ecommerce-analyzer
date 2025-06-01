
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Logo e colori Fuzzy
st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", page_icon="🔍", layout="centered")

# Logo e header
st.image("logo_fuzzy.png", width=180)
st.markdown("<h1 style='color:#000000;'>Fuzzy Ecommerce Analyzer</h1>", unsafe_allow_html=True)
st.markdown("🚀 <span style='color:#555555;'>Analizza il sito e-commerce del tuo cliente in 5 secondi.</span>", unsafe_allow_html=True)

# Form
url = st.text_input("🔗 Inserisci l'URL del sito e-commerce")

if st.button("Analizza", use_container_width=True):
    if not url:
        st.warning("Inserisci un URL valido.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "Titolo non trovato"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else "Nessuna descrizione trovata"

            st.success("✅ Analisi completata")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta description:** {description}")
        except Exception as e:
            st.error(f"Errore nell'analisi del sito: {e}")

st.markdown("---")
st.markdown("👨‍💻 Versione demo — Per la versione avanzata con SEO, ADV, pixel e velocità, contattaci su [fuzzymarketing.it](https://www.fuzzymarketing.it).")
