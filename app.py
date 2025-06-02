
import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

if "utente_loggato" not in st.session_state:
    st.session_state.utente_loggato = False
if "storico_analisi" not in st.session_state:
    st.session_state.storico_analisi = []

if not st.session_state.utente_loggato:
    st.markdown("### 🍏 Benvenuto nel Fuzzy Ecommerce Analyzer")
    st.markdown("_Il tuo assistente di vendita per ecommerce, firmato Fuzzy Marketing._")
    email = st.text_input("Inserisci la tua email per accedere:")
    if st.button("Accedi"):
        if "@" in email and "." in email:
            nome = email.split("@")[0].split(".")[0].capitalize()
            st.session_state.nome_utente = nome
            st.session_state.email_utente = email
            st.session_state.utente_loggato = True
        else:
            st.warning("Inserisci una email valida.")
    st.stop()

st.markdown(f"### 👋 Benvenuto {st.session_state.nome_utente}")
st.caption("Analizza. Comprendi. Vendi. – Powered by Fuzzy")

ruolo = st.radio("Sei un Hunter o un Responsabile?", ["Hunter", "Responsabile"], horizontal=True)

st.markdown("#### 🔍 Analizza un sito ecommerce")
url = st.text_input("Inserisci il link del sito")
if st.button("Avvia analisi"):
    if not url.startswith("http"):
        st.warning("Inserisci un URL valido (con http).")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            html = r.text.lower()
            risultati = []
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            if "connect.facebook.net" not in html:
                risultati.append(("Tecnico", "Pixel Meta assente"))

            if not soup.find("h1"):
                risultati.append(("SEO", "Nessun H1 rilevato"))

            if soup.title and "home" in soup.title.text.lower():
                risultati.append(("Strategico", "Titolo pagina non ottimizzato"))

            if "shopify" in html and "alt" not in html:
                risultati.append(("Content", "Pagine senza contenuti o descrizioni efficaci"))

            st.success("✅ Analisi completata")
            for pacchetto, motivo in risultati:
                if ruolo == "Hunter" and pacchetto not in ["Tecnico", "SEO", "Strategico", "Content"]:
                    continue
                st.subheader(f"👉 Proponi: Intervento {pacchetto}")
                st.markdown(f"**Perché:** {motivo}")
                st.markdown("**Pitch:** " + {
                    "Tecnico": "Il sito non è strutturato per vendere. Sistemiamo pixel, struttura e fiducia.",
                    "SEO": "Senza SEO sei invisibile. Portiamo traffico gratuito e duraturo.",
                    "Strategico": "Serve una struttura chiara per vendere. Costruiamo un funnel su misura.",
                    "Content": "Il sito deve raccontare, non solo mostrare. Usiamo i contenuti per emozionare.",
                }[pacchetto])

            st.session_state.storico_analisi.append({
                "utente": st.session_state.email_utente,
                "data": now,
                "url": url,
                "ruolo": ruolo,
                "proposte": [p[0] for p in risultati]
            })

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")

st.markdown("---")
st.markdown("### 💬 Chat assistente Fuzzy (supporto in call)")
chat_input = st.text_input("Scrivi l'obiezione del cliente:")

if chat_input:
    if "costa" in chat_input.lower():
        st.success("Rispondi: 'Capisco. Ma sistemare ora evita di buttare soldi su un sito che non converte.'")
    elif "ci penso" in chat_input.lower():
        st.success("Rispondi: 'Ogni giorno che aspetti perdi dati. Interveniamo prima che sia tardi.'")
    elif "faccio da solo" in chat_input.lower():
        st.success("Rispondi: 'Ti capisco, ma farlo da soli richiede tempo e rischi. Noi abbiamo un metodo collaudato.'")
    else:
        st.info("Stiamo aggiornando il sistema per rispondere a questa nuova obiezione.")

st.markdown("---")
if st.session_state.email_utente in ["nicolo.amodio@fuzzymarketing.it"]:
    st.markdown("### 📊 Esporta analisi (solo Master)")
    if st.button("Scarica report"):
        df = pd.DataFrame(st.session_state.storico_analisi)
        df.to_csv("report_analisi_fuzzy.csv", index=False)
        with open("report_analisi_fuzzy.csv", "rb") as f:
            st.download_button("📥 Download CSV", f, file_name="report_analisi_fuzzy.csv")
