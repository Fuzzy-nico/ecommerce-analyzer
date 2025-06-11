
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="wide")

def login():
    st.title("🔑 Fuzzy Marketing - Ecommerce Analyzer")
    email = st.text_input("Inserisci la tua email aziendale:")
    if st.button("Accedi"):
        if email.endswith("@fuzzymarketing.it"):
            st.success(f"Benvenuto, {email}!")
        else:
            st.error("Email non valida. Usa il dominio @fuzzymarketing.it")
            return False
    else:
        st.stop()
    return True

if not login():
    st.stop()

col1, col2 = st.columns([1,3])

with col1:
    st.subheader("🧑‍💼 Hunter")
    st.markdown("**(Flusso Hunter invariato — solo analisi homepage & prodotto)**")

    st.subheader("🔑 Hunter")
    role = st.radio("Cosa hai proposto?", ["Hunter","Closer"])
    if role=="Hunter":
        st.markdown("- Flusso di analisi front-end esistente (no modifiche)")
    else:
        st.markdown("**SEZIONE CLOSER**")
        prod = st.selectbox("Da quale prodotto di front-end proviene il cliente?",
                            ["Strategico","Tecnica","Social"])
        if prod=="Strategico":
            obj = st.selectbox("Quale obiettivo ha tra questi tre?",
                               ["Vendita","Incrementare volume","Moltiplicare"])
            if obj=="Vendita":
                st.markdown("**Pacchetto Start — €1.200/mese**")
            elif obj=="Incrementare volume":
                st.markdown("**Pacchetto Top — €1.500/mese**")
            else:
                st.markdown("**Pacchetto Performance — €2.000/mese**")
        elif prod=="Tecnica":
            obj = st.selectbox("Quale obiettivo ha tra questi tre?",
                               ["Creazione sito","Vendere","Incrementare volume"])
            if obj=="Creazione sito":
                st.markdown("**Pacchetto Restyling — €1.500/mese**")
            elif obj=="Vendere":
                st.markdown("**Pacchetto Start — €1.200/mese**")
            else:
                st.markdown("**Pacchetto Top — €1.500/mese**")
        else:
            obj = st.selectbox("Quale obiettivo ha tra questi tre?",
                               ["Visibilità","Vendere","Incrementare volume"])
            if obj=="Visibilità":
                st.markdown("**Pacchetto Social & Go — €1.000/mese**")
            elif obj=="Vendere":
                st.markdown("**Pacchetto Start — €1.200/mese**")
            else:
                st.markdown("**Pacchetto Top — €1.500/mese**")

with col2:
    st.markdown("# 🔍 Analizza il sito eCommerce")
    url = st.text_input("Inserisci URL", "")
    if st.button("🚀 Avvia Analisi"):
        if not url.startswith("http"):
            st.warning("URL non valido")
        else:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            st.success("Analisi completata")
            title = soup.title.string if soup.title else "—"
            desc_tag = soup.find("meta", {"name":"description"})
            desc = desc_tag.get("content","—") if desc_tag else "—"
            problems = []
            if not soup.find("button"):
                problems.append("⚠️ Nessuna CTA")
            if not soup.find(class_="review"):
                problems.append("❌ Nessuna recensione")
            footer = soup.find("footer")
            if not footer:
                problems.append("❌ Footer mancante")
            else:
                if "privacy" not in footer.text.lower():
                    problems.append("⚠️ Footer senza Privacy")
            if not soup.find(text=lambda t: t and "chi siamo" in t.lower()):
                problems.append("⚠️ Mancanza storytelling")
            if not any(k in soup.text.lower() for k in ["reso","garanzia","spedizione"]):
                problems.append("⚠️ Manca badge fiducia")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Descrizione:** {desc}")
            st.markdown("**Problemi:**")
            for p in problems:
                st.write(f"- {p}")
