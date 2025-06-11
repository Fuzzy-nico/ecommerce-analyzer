import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Config
FZY_COLOR = "#87efff"
CLOSER_BTN = "CLOSER"

st.set_page_config(page_title="Fuzzy Marketing Analyzer", layout="centered")

# Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Fuzzy Marketing")
    st.subheader("Login")
    email = st.text_input("Email")
    if st.button("Accedi"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.experimental_rerun()
        else:
            st.error("Inserisci un'email valida")
    st.stop()

# Main UI
st.markdown(f"<h1 style='color:{FZY_COLOR}'>Fuzzy Marketing</h1>", unsafe_allow_html=True)
st.markdown("**Analizza il sito e ti dirò cosa proporre**")
url = st.text_input("Inserisci URL")
if st.button("Analizza"):
    if url.startswith("http"):
        try:
            resp = requests.get(url, timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')
            st.markdown("### Homepage Analysis")
            cta = "OK" if soup.find('a', string=lambda t: t and 'acquista' in t.lower()) else "Mancante"
            reviews = "OK" if soup.find(string=lambda t: 'recension' in t.lower()) else "Mancanti"
            footer = "OK" if soup.find('footer') else "Mancante"
            story = "OK" if soup.find(string=lambda t: 'chi siamo' in t.lower()) else "Mancante"
            trust = "OK" if soup.find(string=lambda t: 'garanzia' in t.lower()) else "Mancante"
            st.write(f"- CTA: {cta}")
            st.write(f"- Recensioni: {reviews}")
            st.write(f"- Footer: {footer}")
            st.write(f"- Storytelling: {story}")
            st.write(f"- Trust elements: {trust}")
            st.markdown("### Product Page Analysis")
            prod_resp = requests.get(url if 'product' in url else url + '/products/sample', timeout=5)
            psoup = BeautifulSoup(prod_resp.text, 'html.parser')
            desc = psoup.find('meta', {'name':'description'}) or psoup.find('p')
            st.write(f"- Descrizione: {'Presente' if desc else 'Mancante'}")
            st.write(f"- Recensioni: {'Presenti' if psoup.find(string=lambda t: 'recension' in t.lower()) else 'Mancanti'}")
            st.write(f"- Garanzie: {'Presenti' if psoup.find(string=lambda t: 'garanzia' in t.lower()) else 'Mancanti'}")
            st.write(f"- Prodotti correlati: {'Presenti' if psoup.find('a', href=lambda x: x and 'related' in x) else 'Mancanti'}")
            st.markdown("### Proposta Hunter")
            st.info("Intervento Tecnico (2h) a €350 per ottimizzare usabilità e conversioni.")
        except Exception as e:
            st.error(f"Errore: {e}")
    else:
        st.warning("URL non valido")

st.markdown("---")

# CLOSER
st.subheader("CLOSER")
origin = st.selectbox("Da quale prodotto front-end proviene il cliente?", ["", "Strategico","Tecnica","Content"])
if origin:
    objective = st.selectbox("Quale obiettivo ha?", ["", 
        "Vendita", "Incrementare volume d'affari", "Moltiplicare entrate"] if origin=="Strategico" else
        ["", "Creazione sito", "Vendere", "Incrementare volume"] if origin=="Tecnica" else
        ["", "Visibilità", "Vendere", "Incrementare volume"]
    )
    if objective:
        mapping = {}
        if origin=="Strategico":
            mapping = {"Vendita":"Start: €1.200", "Incrementare volume d'affari":"Top: €1.500", "Moltiplicare entrate":"Performance: €2.000"}
        elif origin=="Tecnica":
            mapping = {"Creazione sito":"Restyling: €1.500", "Vendere":"Start: €1.200", "Incrementare volume":"Top: €1.500"}
        else:
            mapping = {"Visibilità":"Content: €1.000", "Vendere":"Start: €1.200", "Incrementare volume":"Top: €1.500"}
        st.success(mapping.get(objective, ""))