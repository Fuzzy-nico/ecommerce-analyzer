
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
                risultati.append(("Tecnico", "Manca il pixel Meta: non puoi tracciare le azioni sul sito."))
            if not soup.find("h1"):
                risultati.append(("SEO", "Assenza di H1: struttura poco chiara per Google."))
            if not soup.find("meta", {"name": "description"}):
                risultati.append(("SEO", "Meta description mancante o assente."))
            if soup.title and "home" in soup.title.text.lower():
                risultati.append(("Strategico", "Titolo della homepage generico, senza identità."))
            if "shopify" in html and "alt=" not in html:
                risultati.append(("Content", "Pagine prodotto con immagini non descritte."))
            if "chi siamo" not in html and "about" not in html:
                risultati.append(("Tecnico", "Manca la sezione 'Chi siamo': il brand non si racconta."))
            if "recensioni" not in html and "testimonianze" not in html:
                risultati.append(("Tecnico", "Assenza di recensioni: mancano leve di fiducia."))
            if "p.iva" not in html and "privacy" not in html:
                risultati.append(("Tecnico", "Footer incompleto: mancano dati legali visibili."))
            if "contattaci" not in html and "contact" not in html:
                risultati.append(("Tecnico", "Manca una call-to-action o pagina contatti chiara."))

            st.success("✅ Analisi completata")
            for pacchetto, motivo in risultati:
                if ruolo == "Hunter" and pacchetto not in ["Tecnico", "SEO", "Strategico", "Content"]:
                    continue
                elif ruolo == "Responsabile" and pacchetto == "Tecnico":
                    pacchetto = "Restyling"

                st.subheader(f"👉 Proponi: Intervento {pacchetto}")
                st.markdown(f"**Perché:** {motivo}")
                st.markdown("**Pitch consigliato:** " + {
                    "Tecnico": "Il sito non è pronto per vendere. Prima sistemiamo struttura, fiducia e tracciamenti.",
                    "SEO": "Senza SEO sei invisibile. Ottimizziamo struttura e contenuti per portare traffico gratuito.",
                    "Strategico": "Costruiamo una strategia per testare il prodotto e tracciare i risultati.",
                    "Content": "Miglioriamo i testi, le schede prodotto e la narrazione del brand.",
                    "Restyling": "Il sito è obsoleto o inefficace. Rifacciamolo con un design moderno e vendibile."
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
st.markdown("### 💬 Chat Assistente Fuzzy (obiezioni in call)")

msg = st.text_input("Scrivi l'obiezione o domanda del cliente:")

if msg:
    msg = msg.lower()
    risposta = None
    if "costa" in msg or "soldi" in msg or "prezzo" in msg:
        risposta = "Capisco. Ma sistemare ora ti evita di sprecare soldi in traffico che non converte. Meglio fare ordine prima di investire."
    elif "ci penso" in msg or "devo riflettere" in msg:
        risposta = "Ogni giorno che aspetti perdi dati, soldi e clienti. Questo è il momento giusto per sistemare e partire."
    elif "faccio da solo" in msg or "me la vedo io" in msg:
        risposta = "Puoi farlo, ma rischi di perdere tempo in test. Noi abbiamo già un metodo collaudato e veloce."
    elif "ho già qualcuno" in msg or "lo segue il mio team" in msg:
        risposta = "Ottimo. Ma il nostro intervento è complementare: ti creiamo le basi che il tuo team poi potrà gestire."
    else:
        risposta = "Obiezione non ancora registrata. Rispondi con empatia e cerca di riportare il focus sul valore che offriamo."

    st.success(f"💬 Risposta suggerita:

{risposta}")

# Area esportazione per utenti master
st.markdown("---")
master_emails = ["nicolo.amodio@fuzzymarketing.it"]
if st.session_state.email_utente in master_emails:
    st.markdown("### 📊 Esporta storico analisi")
    if st.button("Scarica CSV"):
        df = pd.DataFrame(st.session_state.storico_analisi)
        df.to_csv("storico_fuzzy.csv", index=False)
        with open("storico_fuzzy.csv", "rb") as f:
            st.download_button("📥 Download CSV", f, file_name="storico_fuzzy.csv")
