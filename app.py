import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import csv

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

# Background color
st.markdown(
    "<style>body { background-color: #87efff; }</style>",
    unsafe_allow_html=True
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "analisi_storage" not in st.session_state:
    st.session_state.analisi_storage = []

# Login
def do_login():
    email = st.session_state.get("email_input", "").strip()
    if email and "@" in email:
        st.session_state.logged_in = True
        st.session_state.user_email = email
    else:
        st.error("Inserisci una email valida.")

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Fuzzy Marketing</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Analizza il sito e ti dirò cosa devi proporre</p>", unsafe_allow_html=True)
    st.text_input("Email", key="email_input", placeholder="es. nome@azienda.it")
    st.button("Accedi", on_click=do_login)
    st.stop()

# Analisi sito
st.markdown("## 🔍 Analisi del sito ecommerce")
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"])
url = st.text_input("Inserisci l'URL del sito")

if st.button("Analizza Sito") and url:
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        problemi = []
        motivi = []
        servizio = ""

        if not soup.find("footer"):
            problemi.append("Footer non a norma: mancano i dati aziendali.")
            motivi.append("Il sito non trasmette fiducia.")
        if not soup.find(string=lambda x: x and "recension" in x.lower()):
            problemi.append("Nessuna sezione recensioni trovata.")
            motivi.append("Mancanza di prova sociale.")
        if not soup.find("a", string=lambda x: x and "compra" in x.lower()):
            problemi.append("Nessuna call to action nella homepage.")
            motivi.append("Non viene guidata l'azione dell'utente.")
        if not soup.find_all("h1"):
            problemi.append("Mancanza tag H1.")
            motivi.append("Struttura del sito poco chiara.")
        if not soup.find_all("section", class_="product"):
            problemi.append("Sezioni prodotto assenti.")
            motivi.append("Non si capisce cosa si vende.")

        if ruolo == "Hunter":
            servizio = "💡 Proposta: Intervento Tecnico"
        else:
            servizio = "💼 Proposta: Restyling o Sales Page"

        st.success("✅ Analisi completata")
        st.markdown("### 🚨 Problemi trovati")
        for p in problemi:
            st.markdown(f"- {p}")
        st.markdown("### 🎯 Motivazioni Commerciali")
        for m in motivi:
            st.markdown(f"- {m}")
        st.markdown("### 🛠 Servizio da proporre")
        st.markdown(servizio)

        st.session_state.analisi_storage.append([st.session_state.user_email, url, servizio])

    except Exception as e:
        st.error(f"Errore durante l'analisi: {e}")

# Esportazione CSV solo per master
if st.session_state.user_email == "nicolo.amodio@fuzzymarketing.it":
    if st.button("📁 Esporta Analisi in CSV"):
        csv_path = "/mnt/data/analisi_fuzzy_export.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Email", "Sito", "Cosa Proporre"])
            writer.writerows(st.session_state.analisi_storage)
        st.success("CSV creato.")
        with open(csv_path, "rb") as f:
            st.download_button("📥 Scarica il CSV", f, "analisi_export.csv")

# Chat GPT
st.markdown("---")
st.markdown("## 💬 LIVE CHAT COMMERCIALE")
st.markdown("_Ti aiuterò con obiezioni, domande tecniche e molto altro._")

if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = st.text_area("Scrivi qui la tua domanda")
    if st.button("Invia"):
        try:
            r = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Agisci come assistente commerciale Fuzzy Marketing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            st.markdown(f"**Risposta:** {r.choices[0].message.content}")
        except Exception as e:
            st.error(f"Errore chat: {e}")
else:
    st.info("Per usare la chat, imposta OPENAI_API_KEY")
