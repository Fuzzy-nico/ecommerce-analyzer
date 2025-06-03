import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", page_icon="🛍️", layout="centered")

# Login Screen
if "email" not in st.session_state:
    st.title("🔵 Benvenuto nel Fuzzy Ecommerce Analyzer")
    st.markdown("_Il tuo assistente di vendita per ecommerce, firmato Fuzzy Marketing._")
    email = st.text_input("Inserisci la tua email per accedere:")
    if st.button("Accedi") and email:
        st.session_state["email"] = email
        st.rerun()
    st.stop()

# Greet user
st.title("Fuzzy Ecommerce Analyzer")
st.markdown(f"👋 Benvenuto **{st.session_state['email'].split('@')[0].capitalize()}**")

# Selezione ruolo
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"], horizontal=True)

# Inserimento URL
url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare")

if st.button("Analizza") and url:
    with st.spinner("Analisi in corso..."):
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "Titolo non trovato"
            meta_desc_tag = soup.find("meta", attrs={"name": "description"})
            description = meta_desc_tag["content"].strip() if meta_desc_tag and meta_desc_tag.get("content") else "Nessuna description trovata"
            h1_count = len(soup.find_all("h1"))

            st.success("✅ Analisi completata")
            st.markdown(f"**🧠 SEO & Contenuti**\n- Titolo: {title}\n- Meta Description: {description}\n- Tag H1 trovati: {h1_count}")

            # Suggerimento commerciale
            if ruolo == "Hunter":
                if not meta_desc_tag:
                    suggerimento = "Proponi pacchetto SEO: manca la meta description."
                elif h1_count <= 1:
                    suggerimento = "Proponi SEO + Tecnico: struttura debole, sito non pronto per Google."
                else:
                    suggerimento = "Proponi ADV Meta o Intervento Tecnico se il sito non è ottimizzato alla vendita."
            else:
                if not meta_desc_tag and h1_count <= 1:
                    suggerimento = "Consiglia restyling del sito e un pacchetto SEO completo."
                elif not soup.find("script", attrs={"src": lambda x: x and "facebook" in x}):
                    suggerimento = "Manca il Pixel: consiglia intervento tecnico + strategico."
                else:
                    suggerimento = "Analizza la struttura interna e proponi strategico se il cliente vuole scalare."

            st.success(f"💬 Risposta suggerita:
{suggerimento}")

        except Exception as e:
            st.error(f"Errore durante l'analisi del sito: {e}")
