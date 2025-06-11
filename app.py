import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="wide")

# — LOGIN —
def login():
    st.title("🔑 Fuzzy Marketing - Ecommerce Analyzer")
    email = st.text_input("Inserisci la tua email aziendale:", key="login_email")
    if st.button("Accedi", key="login_button"):
        if email.endswith("@fuzzymarketing.it"):
            st.success(f"Benvenuto, {email}!")
        else:
            st.error("Email non valida. Usa @fuzzymarketing.it")
            return False
    else:
        st.stop()
    return True

if not login():
    st.stop()

# — LAYOUT —
col1, col2 = st.columns([1,3])

with col1:
    st.subheader("🧑‍💼 Hunter")
    st.markdown("**(Flusso Hunter invariato — analisi homepage & prodotto)**")

    st.subheader("🔑 Closer")
    prod = st.selectbox("Da quale pacchetto front-end proviene il cliente?",
                        ["Strategico","Tecnica","Social"], key="closer_product")
    if prod=="Strategico":
        obj = st.selectbox("Quale obiettivo ha?", ["Vendita","Incrementare volume","Moltiplicare"], key="closer_strategico")
        if obj=="Vendita":
            st.markdown("**Pacchetto Start — €1.200/mese**")
        elif obj=="Incrementare volume":
            st.markdown("**Pacchetto Top — €1.500/mese**")
        else:
            st.markdown("**Pacchetto Performance — €2.000/mese**")
    elif prod=="Tecnica":
        obj = st.selectbox("Quale obiettivo ha?", ["Creazione sito","Vendere","Incrementare volume"], key="closer_tecnica")
        if obj=="Creazione sito":
            st.markdown("**Pacchetto Restyling — €1.500/mese**")
        elif obj=="Vendere":
            st.markdown("**Pacchetto Start — €1.200/mese**")
        else:
            st.markdown("**Pacchetto Top — €1.500/mese**")
    else:
        obj = st.selectbox("Quale obiettivo ha?", ["Visibilità","Vendere","Incrementare volume"], key="closer_social")
        if obj=="Visibilità":
            st.markdown("**Pacchetto Social & Go — €1.000/mese**")
        elif obj=="Vendere":
            st.markdown("**Pacchetto Start — €1.200/mese**")
        else:
            st.markdown("**Pacchetto Top — €1.500/mese**")

with col2:
    st.markdown("# 🔍 Analizza il sito eCommerce")
    url = st.text_input("Inserisci URL (con http/https)", "", key="analysis_url")
    if st.button("🚀 Avvia Analisi", key="analyse_button"):
        if not url.startswith("http"):
            st.warning("Inserisci un URL valido.")
        else:
            try:
                resp = requests.get(url, timeout=10)
                soup = BeautifulSoup(resp.text, "html.parser")
                st.success("✅ Analisi completata")
                title = soup.title.string if soup.title else "—"
                desc_tag = soup.find("meta", {"name":"description"})
                desc = desc_tag.get("content","—") if desc_tag else "—"
                problems = []
                if not soup.find(lambda t: t.name in ["button","a"] and "buy" in t.text.lower()):
                    problems.append("⚠️ Nessuna CTA chiara")
                if not soup.find(class_="review"):
                    problems.append("❌ Nessuna recensione")
                footer = soup.find("footer")
                if not footer:
                    problems.append("❌ Footer mancante")
                else:
                    if "privacy" not in footer.text.lower():
                        problems.append("⚠️ Footer senza Privacy")
                if not soup.find(text=lambda t: t and "chi siamo" in t.lower()):
                    problems.append("⚠️ Manca sezione “Chi siamo”")
                if not any(k in soup.text.lower() for k in ["reso","garanzia","spedizione"]):
                    problems.append("⚠️ Manca badge fiducia (resi/garanzie)")
                st.markdown(f"""**Titolo:** {title}\n\n**Descrizione:** {desc}""")
                st.markdown("**Problemi homepage:**")
                for p in problems:
                    st.write(f"- {p}")
            except Exception as e:
                st.error(f"Errore analisi: {e}")
