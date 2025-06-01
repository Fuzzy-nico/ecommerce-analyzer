
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")
st.image("logo_fuzzy_corretto.png", width=180)

st.title("Fuzzy Ecommerce Analyzer")

# Ruolo utente
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"], horizontal=True)

# Inserimento URL
url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare")

# Output analisi e suggerimento automatico
if st.button("Analizza"):
    if not url.startswith("http"):
        st.warning("Inserisci un URL valido.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            html = r.text.lower()

            st.success("✅ Analisi completata")

            # Dummy logic per esempio (estendibile)
            suggerimenti = []

            if "connect.facebook.net" not in html:
                suggerimenti.append(("Tecnico", "Manca il Meta Pixel. Serve tracciamento per vendere."))

            if not soup.find("h1"):
                suggerimenti.append(("SEO", "Nessun H1 rilevato. Google non capisce cosa vendi."))

            if soup.title and "home" in soup.title.text.lower():
                suggerimenti.append(("Strategico", "Titolo generico: manca una struttura strategica."))

            if "shopify" in html and "alt" not in html:
                suggerimenti.append(("Content", "Schede prodotto non valorizzate: mancano testi persuasivi."))

            if suggerimenti:
                for serv, motivo in suggerimenti:
                    if ruolo == "Hunter" and serv not in ["Tecnico", "Strategico", "SEO", "Content"]:
                        continue
                    st.subheader(f"👉 Proponi: Intervento {serv}")
                    st.markdown(f"**Perché:** {motivo}")
                    if serv == "Tecnico":
                        st.info("💬 Pitch: Il sito non è strutturato per vendere. Partiamo sistemando le basi tecniche: pixel, analytics, fiducia.")
                    elif serv == "Strategico":
                        st.info("💬 Pitch: Senza una struttura strategica, il traffico non converte. Costruiamo un funnel chiaro.")
                    elif serv == "SEO":
                        st.info("💬 Pitch: La SEO ti aiuta a non dipendere per sempre dall'ADV. Ti portiamo traffico gratuito e stabile.")
                    elif serv == "Content":
                        st.info("💬 Pitch: Le persone comprano ciò che capiscono. Miglioriamo i testi e le emozioni del sito.")

            else:
                st.success("✅ Nessun errore critico rilevato. Ottimo per passare alla fase successiva.")

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")

# Chat simulata per obiezioni
st.markdown("---")
st.subheader("💬 Chat Assistente Fuzzy")
user_msg = st.text_input("Scrivi un'obiezione o una domanda ricevuta in call")

if user_msg:
    if "costa" in user_msg.lower():
        st.success("Rispondi così: 'Capisco. Ma sistemando ora eviti di buttare soldi in traffico che non converte.'")
    elif "ci penso" in user_msg.lower():
        st.success("Rispondi così: 'Ogni giorno che aspetti perdi dati e opportunità. Questo è il momento di intervenire.'")
    elif "faccio da solo" in user_msg.lower():
        st.success("Rispondi così: 'Farlo da soli richiede tempo e test. Noi abbiamo già un metodo collaudato e veloce.'")
    else:
        st.info("Suggerimento in arrivo… Stiamo aggiornando il sistema con nuove risposte.")
