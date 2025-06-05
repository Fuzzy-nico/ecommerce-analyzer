import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="centered")

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
        "<h1 style='text-align: center; color: white;'>Fuzzy Marketing - Ecommerce Analyzer</h1>",
        unsafe_allow_html=True
    )
    st.text_input("Email", key="email_input", placeholder="es. nome@azienda.it")
    if st.button("Accedi"):
        do_login()
    st.stop()

st.markdown(f"<h2 style='color:white;'>Benvenuto, {st.session_state.user_email}</h2>", unsafe_allow_html=True)

st.markdown("## 🔍 Analisi del sito ecommerce")
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
            cta = soup.find("a", string=lambda x: x and "compra" in x.lower())
            reviews = soup.find(string=lambda x: x and "recension" in x.lower())
            product_sections = soup.find_all("section", class_="product")

            pitch = []

            # UI/UX and trust analysis (non-SEO focused)
            if not footer:
                pitch.append("❌ Il sito non ha un footer visibile: questo riduce la fiducia. ➜ Proponi un **Intervento Tecnico** per aggiungere recapiti, policy e info legali.")
            if not cta:
                pitch.append("❌ Nessuna CTA chiara trovata nella homepage. ➜ Proponi una **Sales Page a Risposta Diretta** per aumentare le conversioni.")
            if not reviews:
                pitch.append("⚠️ Nessuna recensione o prova sociale rilevata. ➜ Proponi un **Intervento Content** per costruire fiducia con social, blog o testimonianze.")
            if not h1_tags:
                pitch.append("⚠️ Mancano titoli chiari. Il sito può risultare confuso per l’utente. ➜ Proponi un **Intervento Tecnico**.")
            if len(product_sections) == 0:
                pitch.append("❌ Non ho trovato sezioni prodotto evidenti. ➜ Proponi un **Intervento Strategico** per definire gli obiettivi e struttura del funnel.")
            if len(pitch) == 0:
                pitch.append("✅ Il sito presenta una struttura solida. ➜ Puoi proporre **SEO avanzata**, **ADV** o **Automation**.")

            st.success("Analisi completata:")
            st.markdown(f"**Titolo:** {title}")
            for p in pitch:
                st.markdown(p)

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")

# Chat GPT (manuale via OPENAI_API_KEY)
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
                        {"role": "system", "content": "Agisci come un esperto commerciale Fuzzy Marketing, focalizzato su ecommerce."},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=400
                )
                answer = response.choices[0].message.content
                st.markdown(f"**Risposta:** {answer}")
            except Exception as e:
                st.error(f"Errore GPT: {e}")
else:
    st.info("Per usare la chat, imposta la variabile OPENAI_API_KEY nel tuo ambiente.")
