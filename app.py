import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def do_login():
    email = st.session_state.get("email_input", "").strip()
    if email and "@" in email:
        st.session_state.logged_in = True
        st.session_state.user_email = email
    else:
        st.error("Inserisci un indirizzo email valido.")

if not st.session_state.logged_in:
    st.markdown(
        "<div style='background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 40px; border-radius: 10px;'>"
        "<h1 style='color: white; text-align: center;'>Fuzzy Ecommerce Analyzer</h1>"
        "<p style='color: white; text-align: center;'>Inserisci la tua email per iniziare:</p></div>",
        unsafe_allow_html=True
    )
    st.text_input("Email", key="email_input", placeholder="es. nome@azienda.it")
    if st.button("Accedi"):
        do_login()
    st.stop()

st.markdown(f"<h2 style='color:white;'>Benvenuto, {st.session_state.user_email}</h2>", unsafe_allow_html=True)

user_role = st.radio("Chi sei?", ["Hunter", "Responsabile"], horizontal=True)

url_home = st.text_input("Inserisci l'URL della home page:", placeholder="https://www.nomesito.it")

if st.button("Analizza Sito"):
    if not url_home.strip().startswith("http"):
        st.error("URL non valido. Deve iniziare con http o https.")
    else:
        try:
            response = requests.get(url_home, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "Titolo non presente"
            h1_tags = soup.find_all("h1")
            footer = soup.find("footer")
            cta = soup.find("a", string=lambda x: x and ("compra" in x.lower() or "acquista" in x.lower()))
            reviews = soup.find(string=lambda x: x and "recension" in x.lower())
            product_sections = soup.find_all("section", class_="product")

            problemi = []
            motivazioni = []
            servizio = ""

            if not footer:
                problemi.append("❌ Footer non a norma: mancano dati aziendali fondamentali.")
                motivazioni.append("Il sito non trasmette fiducia e legalità.")
            if not cta:
                problemi.append("❌ Homepage senza call-to-action.")
                motivazioni.append("Il cliente non sa dove cliccare per acquistare.")
            if not reviews:
                problemi.append("⚠️ Nessuna recensione o prova sociale.")
                motivazioni.append("Riduce la fiducia nel brand.")
            if not h1_tags:
                problemi.append("⚠️ Mancano titoli principali (H1).")
                motivazioni.append("La struttura del sito è poco chiara per l’utente.")
            if len(product_sections) == 0:
                problemi.append("❌ Nessuna sezione prodotto evidente.")
                motivazioni.append("Non si capisce cosa vendi.")

            if "Hunter" in user_role:
                if problemi:
                    servizio = "💡 **Proposta Front-End: Intervento Tecnico**"
                else:
                    servizio = "✅ Nessun errore critico. Consiglia SEO o Flow Automatici."
            else:
                if problemi:
                    servizio = "💼 **Proposta Avanzata: Restyling, Automation o Sales Page**"
                else:
                    servizio = "✅ Nessun errore critico. Puoi proporre ADV o Growth Strategy."

            st.success("Analisi completata con successo ✅")
            st.markdown("---")
            st.markdown("### 🔍 Problemi rilevati:")
            for p in problemi:
                st.markdown(p)
            st.markdown("### 🎯 Motivazione commerciale:")
            for m in motivazioni:
                st.markdown(f"- {m}")
            st.markdown("### 🛠 Servizio da proporre:")
            st.markdown(servizio)

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")

st.markdown("## 💬 Chat GPT-4")
if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    question = st.text_area("Fai una domanda commerciale:")
    if st.button("Invia"):
        if question.strip():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Agisci come un esperto commerciale di Fuzzy Marketing, ecommerce strategist e closer."},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=500
                )
                st.markdown(f"**Risposta:** {response.choices[0].message.content}")
            except Exception as e:
                st.error(f"Errore GPT: {e}")
else:
    st.info("Per attivare la chat, imposta OPENAI_API_KEY nel tuo ambiente.")
