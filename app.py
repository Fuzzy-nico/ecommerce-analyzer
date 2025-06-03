
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Ecommerce Analyzer", layout="centered")

# Sezione email
email = st.text_input("Inserisci la tua email per accedere:")
if email:
    st.success(f"✅ Benvenuto {email}")

# Selezione ruolo
ruolo = st.radio("Chi sei?", ("Hunter", "Responsabile"))

st.markdown("---")

# Input URL
url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare", "https://")
if st.button("Analizza"):
    if url.startswith("http"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "Nessun titolo trovato"
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = description_tag["content"] if description_tag and description_tag.has_attr("content") else "Nessuna descrizione trovata"
            h1_tags = soup.find_all("h1")
            h1_count = len(h1_tags)

            # CMS detection (semplificata)
            cms = "Shopify" if "shopify" in url.lower() else "Non identificato"

            st.success("✅ Analisi completata")
            st.markdown("## 📊 SEO & Contenuti")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta Description:** {description}")
            st.markdown(f"**Tag H1 trovati:** {h1_count}")

            st.markdown("## 🛠️ CMS utilizzato")
            st.markdown(f"**CMS:** {cms}")

            st.markdown("## 💼 Cosa proporre al cliente")
            st.info("💡 Suggerimento: Proponi il Pacchetto Tecnico")
            st.markdown("**Motivo:** Perché manca il Meta Pixel, quindi il sito non può tracciare chi visita e chi acquista.")

        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")
    else:
        st.warning("⚠️ Inserisci un URL valido.")

st.markdown("---")

# Chat: obiezioni comuni
try:
    st.subheader("💬 Chat assistente Fuzzy: risposte a obiezioni")
    msg = st.text_input("Scrivi l'obiezione ricevuta dal cliente")
    if msg:
        # Placeholder per la risposta automatica alle obiezioni
        st.write("Risposta suggerita: Grazie per il feedback, ecco come risolvere...")
except Exception as e:
    st.error(f"Errore nella sezione chat: {e}")
