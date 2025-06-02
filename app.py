
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
    st.image("logo_fuzzy_corretto.png", width=200)
    st.markdown("## Benvenuto nel Fuzzy Ecommerce Analyzer")
    st.caption("_Il tuo assistente di vendita intelligente firmato Fuzzy Marketing_")
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
ruolo = st.radio("Sei un Hunter o un Responsabile?", ["Hunter", "Responsabile"], horizontal=True)

st.markdown("#### 🔍 Analizza un sito ecommerce")
url = st.text_input("Inserisci il link del sito da analizzare")

if st.button("Avvia analisi"):
    if not url.startswith("http"):
        st.warning("Inserisci un URL valido.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            html = r.text.lower()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            risultati = []

            if "connect.facebook.net" not in html:
                risultati.append(("Tecnico", "Pixel Meta assente, non puoi tracciare il comportamento utente."))

            if not soup.find("h1"):
                risultati.append(("SEO", "Nessun H1 rilevato: Google non capisce cosa vendi."))

            if soup.title and "home" in soup.title.text.lower():
                risultati.append(("Strategico", "Titolo generico: manca struttura e identità chiara."))

            if "shopify" in html and "alt" not in html:
                risultati.append(("Content", "Pagine poco descrittive, senza contenuti persuasivi."))

            st.success("✅ Analisi completata")

            for pacchetto, motivo in risultati:
                if ruolo == "Hunter" and pacchetto not in ["Tecnico", "SEO", "Strategico", "Content"]:
                    continue
                elif ruolo == "Responsabile" and pacchetto == "Tecnico":
                    pacchetto = "Restyling"

                st.subheader(f"👉 Proponi: Intervento {pacchetto}")
                st.markdown(f"**Perché:** {motivo}")
                st.markdown("**Pitch consigliato:** " + {
                    "Tecnico": "Il sito non è pronto a vendere. Mancano fiducia, struttura e tracciamenti. Sistemiamolo prima di investire in traffico.",
                    "SEO": "Senza SEO sei invisibile. Portiamo traffico gratuito e duraturo ottimizzando struttura e contenuti.",
                    "Strategico": "Serve una strategia chiara per capire il mercato, tracciare i dati e testare il prodotto.",
                    "Content": "Il sito deve emozionare e raccontare. Senza contenuti forti, le persone non si fidano.",
                    "Restyling": "Il sito attuale è obsoleto o poco efficace. Rifacciamolo con un layout moderno e orientato alla vendita."
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
st.markdown("### 💬 Chat Assistente Fuzzy (scrivi obiezioni o dubbi del cliente)")

msg = st.text_input("Inserisci qui l'obiezione o domanda ricevuta in call:")

if msg:
    msg = msg.lower()
    if "costa" in msg:
        st.success("Rispondi: 'Capisco. Ma sistemare ora evita di sprecare soldi in ADV che non converte. Prima sistemiamo, poi spingiamo.'")
    elif "ci penso" in msg:
        st.success("Rispondi: 'Ogni giorno che aspetti perdi dati e opportunità. Questo è il momento giusto per partire.'")
    elif "faccio da solo" in msg:
        st.success("Rispondi: 'Farlo da soli richiede tempo e test. Noi abbiamo già un metodo che funziona e ti fa risparmiare tempo.'")
    elif "ho già qualcuno" in msg:
        st.success("Rispondi: 'Ottimo! Ma il nostro intervento iniziale è complementare, non sostitutivo. Serve a dare una struttura che poi anche il tuo team può seguire.'")
    else:
        st.info("Risposta in elaborazione. La nostra AI sta assimilando nuove obiezioni.")

st.markdown("---")
if st.session_state.email_utente == "nicolo.amodio@fuzzymarketing.it":
    st.markdown("### 📊 Esporta le analisi effettuate")
    if st.button("Scarica CSV"):
        df = pd.DataFrame(st.session_state.storico_analisi)
        df.to_csv("report_fuzzy.csv", index=False)
        with open("report_fuzzy.csv", "rb") as f:
            st.download_button("📥 Download Report", f, file_name="report_fuzzy.csv")
