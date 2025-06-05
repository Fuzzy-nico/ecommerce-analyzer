
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import csv
import os
import time

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")
st.markdown("<style>body { background-color: #87efff; }</style>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "analisi_storage" not in st.session_state:
    st.session_state.analisi_storage = []

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

st.markdown("## 🔍 Analisi del sito ecommerce")
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"])
url = st.text_input("Inserisci l'URL del sito")

if st.button("Analizza Sito") and url:
    try:
        start_time = time.time()
        r = requests.get(url, timeout=10)
        load_time = round(time.time() - start_time, 2)
        soup = BeautifulSoup(r.text, "html.parser")

        problemi = []
        motivi = []
        punteggio = 100

        def penalizza(condizione, problema, motivo, punti, score):
            if condizione:
                problemi.append(problema)
                motivi.append(motivo)
                score -= punti
            return score

        punteggio = penalizza(load_time > 3, "⚠️ Homepage lenta", "Esperienza utente negativa", 10, punteggio)
        punteggio = penalizza(not soup.find("footer"), "❌ Footer mancante", "Nessun riferimento aziendale", 15, punteggio)
        punteggio = penalizza(not soup.find(string=lambda x: x and "recension" in x.lower()), "❌ Nessuna recensione visibile", "Manca prova sociale", 15, punteggio)
        punteggio = penalizza(not soup.find("h1"), "⚠️ Manca H1", "Struttura poco chiara", 5, punteggio)
        punteggio = penalizza(not soup.find(string=lambda x: x and "chi siamo" in x.lower()), "⚠️ Nessuna sezione 'Chi siamo'", "Non trasmette identità", 10, punteggio)
        punteggio = penalizza(not soup.find(string=lambda x: x and ("acquista" in x.lower() or "compra" in x.lower())), "⚠️ Nessuna CTA trovata", "L’utente non è guidato", 10, punteggio)
        punteggio = penalizza(not soup.find(string=lambda x: x and "garanzia" in x.lower()), "⚠️ Nessuna garanzia o badge fiducia", "Manca rassicurazione", 10, punteggio)
        punteggio = penalizza(not soup.find(string=lambda x: x and "privacy" in x.lower()), "⚠️ Manca link a privacy", "Footer non conforme", 10, punteggio)

        servizio = "💡 Intervento Tecnico" if ruolo == "Hunter" else "💼 Restyling Avanzato o Automation"

        st.success("✅ Analisi completata")
        st.markdown(f"### Fuzzy Score: **{punteggio}/100**")
        st.markdown("### Problemi rilevati:")
        for p in problemi:
            st.markdown(f"- {p}")
        st.markdown("### Motivazioni Commerciali:")
        for m in motivi:
            st.markdown(f"- {m}")
        st.markdown("### Servizio consigliato:")
        st.markdown(servizio)

        st.session_state.analisi_storage.append([st.session_state.user_email, url, servizio])
    except Exception as e:
        st.error(f"Errore durante l'analisi: {e}")

if st.session_state.user_email == "nicolo.amodio@fuzzymarketing.it":
    if st.button("📁 Esporta Analisi"):
        with open("/mnt/data/analisi_export.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Email", "Sito", "Servizio"])
            writer.writerows(st.session_state.analisi_storage)
        st.success("Esportazione completata")
        with open("/mnt/data/analisi_export.csv", "rb") as f:
            st.download_button("📥 Scarica CSV", f, "analisi_export.csv")

st.markdown("---")
st.markdown("## 💬 LIVE CHAT COMMERCIALE")
st.markdown("_Ti aiuterò con obiezioni, domande tecniche e molto altro._")

if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    domanda = st.text_area("Scrivi qui la tua domanda")
    if st.button("Invia"):
        try:
            risp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Agisci come assistente commerciale Fuzzy Marketing."},
                          {"role": "user", "content": domanda}],
                max_tokens=300
            )
            st.markdown(f"**Risposta:** {risp.choices[0].message.content}")
        except Exception as e:
            st.error(f"Errore nella chat: {e}")
else:
    st.info("Imposta OPENAI_API_KEY per attivare la chat.")
