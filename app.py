
import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

# Logo alto a sinistra fisso
st.markdown(
    "<div style='position: fixed; top: 10px; left: 10px;'><img src='https://fuzzymarketing.it/logo-fuzzy.png' width='150'></div>",
    unsafe_allow_html=True
)

# Autenticazione via email
if "utente" not in st.session_state:
    st.title("🔵 Fuzzy Ecommerce Analyzer")
    email = st.text_input("Inserisci la tua email per iniziare")
    if st.button("Accedi"):
        if "@" in email and "." in email:
            st.session_state.utente = email
            st.rerun()
        else:
            st.error("Inserisci una email valida.")
    st.stop()

nome = st.session_state.utente.split("@")[0].capitalize()
st.title(f"👋 Benvenuto {nome}")

# Ruolo
ruolo = st.radio("Sei un Hunter o un Responsabile?", ["Hunter", "Responsabile"], horizontal=True)

# Analisi
url = st.text_input("🔍 Inserisci il link del sito da analizzare")
if st.button("Analizza"):
    if not url.startswith("http"):
        st.warning("Inserisci un URL valido.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            html = r.text.lower()

            st.subheader("📊 Analisi tecnica:")
            risultati = []

            if "connect.facebook.net" not in html:
                risultati.append(("Pixel Meta assente", "Tecnico", "Senza Pixel non puoi tracciare chi visita il sito e chi compra."))
            if not soup.find("meta", {"name": "description"}):
                risultati.append(("Meta description mancante", "SEO", "Google non capisce cosa vende il sito, e il CTR è più basso."))
            if len(soup.find_all("h1")) <= 1:
                risultati.append(("0–1 H1 trovati", "SEO + Tecnico", "Le pagine non sono strutturate per Google. Si perde posizionamento."))
            if "shopify" in html and "connect.facebook.net" not in html:
                risultati.append(("Shopify + no pixel", "Tecnico", "Hai un sito attivo ma non puoi misurare nulla."))
            if "wordpress" in html and len(soup.find_all("p")) < 5:
                risultati.append(("Contenuti poveri", "Content", "Le schede prodotto sono deboli. Niente storytelling = poche conversioni."))
            if "chi siamo" not in html and "about" not in html:
                risultati.append(("Manca 'Chi siamo'", "Tecnico", "Homepage senza storia o fiducia, non trasmette autorità."))
            if "recensioni" not in html and "testimonianze" not in html:
                risultati.append(("Mancano recensioni", "Tecnico", "Senza prova sociale, l’utente non si fida."))
            if "p.iva" not in html or "privacy" not in html:
                risultati.append(("Footer incompleto", "Tecnico", "Mancano riferimenti legali, il sito sembra non professionale."))

            for voce, servizio, motivazione in risultati:
                if ruolo == "Hunter" and servizio not in ["Tecnico", "SEO", "Strategico", "Content"]:
                    continue
                st.markdown(f"🧩 **Problema rilevato:** {voce}")
                st.markdown(f"🎯 **Servizio da proporre:** {servizio}")
                st.markdown(f"💬 **Motivazione:** {motivazione}")
                pitch = {
                    "Tecnico": "Partiamo con un intervento tecnico: due ore operative dove sistemiamo i punti critici e rendiamo il sito pronto per vendere.",
                    "SEO": "Serve visibilità organica: miglioriamo struttura e contenuti per comparire su Google e ridurre la dipendenza da ADV.",
                    "Strategico": "Ti serve una base solida: analizziamo tutto e costruiamo un piano personalizzato per iniziare a vendere.",
                    "Content": "Le persone comprano dalle persone: creiamo contenuti che raccontano il tuo brand e migliorano la conversione.",
                    "SEO + Tecnico": "Sito non leggibile da Google e con struttura debole: sistemiamo entrambi in un intervento mirato."
                }
                st.markdown(f"📢 **Pitch suggerito:** {pitch.get(servizio, 'Proponi questo servizio come primo passo concreto per far crescere le vendite.')}")

# Chat: obiezioni comuni
st.markdown("---")
st.subheader("💬 Chat assistente Fuzzy: risposte a obiezioni")
msg = st.text_input("Scrivi l'obiezione ricevuta dal cliente")

if msg:
    msg = msg.lower()
    if "prezzo" in msg or "costa" in msg or "soldi" in msg:
        risposta = "Capisco perfettamente. Ma sistemare il sito ora ti evita di buttare soldi in pubblicità inefficace. Questo è un investimento minimo con effetto immediato."
    elif "ci penso" in msg or "fammi sapere" in msg:
        risposta = "Nessun problema. Intanto blocchiamo un follow-up e ti invio un recap. Così puoi valutare tutto con calma ma con le idee chiare."
    elif "ho già qualcuno" in msg or "ho già un’agenzia" in msg:
        risposta = "Ottimo. Il nostro intervento è complementare: facciamo pulizia e strategia, poi il tuo team lavora meglio e con meno sprechi."
    elif "faccio da solo" in msg or "me la vedo io" in msg:
        risposta = "Certo. Ma se vuoi evitare mesi di test inutili, il nostro metodo ti porta risultati concreti in pochi giorni."
    elif "voglio parlare col socio" in msg or "parlo con mia moglie" in msg:
        risposta = "Capito. Blocchiamo una call breve insieme anche a lui. Così evitiamo di rifare tutto da capo e prendete una decisione insieme."
    else:
        risposta = "Questa obiezione non è ancora mappata. Rispondi riportando il focus sul problema che il cliente ti ha appena confermato."

    st.success(f"✅ Risposta suggerita:

{risposta}")

# Download CSV solo per Master
if st.session_state.utente == "nicolo.amodio@fuzzymarketing.it":
    st.markdown("---")
    st.subheader("📥 Esporta storico analisi (solo Master)")
    if "storico" not in st.session_state:
        st.session_state.storico = []
    if url and risultati:
        st.session_state.storico.append({
            "email": st.session_state.utente,
            "ruolo": ruolo,
            "url": url,
            "problemi": ", ".join([r[0] for r in risultati]),
            "proposte": ", ".join([r[1] for r in risultati]),
            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    if st.button("Scarica CSV"):
        df = pd.DataFrame(st.session_state.storico)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📩 Scarica report", csv, file_name="report_fuzzy.csv", mime="text/csv")
