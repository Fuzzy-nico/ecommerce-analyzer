import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Config
FZY_COLOR = "#87efff"
CLOSER_BTN = "CLOSER"

st.set_page_config(page_title="Fuzzy Marketing Analyzer", layout="wide")

def login():
    st.markdown(f"<div style='background-color:{FZY_COLOR};padding:50px;border-radius:10px'><h1 style='color:white;text-align:center'>Fuzzy Marketing</h1><h3 style='color:white;text-align:center'>Login</h3></div>", unsafe_allow_html=True)
    email = st.text_input("Email")
    if st.button("Accedi"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.experimental_rerun()
        else:
            st.error("Inserisci un'email valida")
    st.stop()

def analyze_site(url):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Homepage
        cta = "Trovata CTA 'Acquista'" if soup.find('a', string=lambda t: t and 'acquista' in t.lower()) else "Nessuna CTA 'Acquista'"
        reviews = "Recensioni visibili" if soup.find(string=lambda t: 'recension' in t.lower()) else "Recensioni mancanti"
        footer = "Footer OK" if soup.find('footer') else "Footer mancante o incompleto"
        storytelling = "Storytelling presente" if soup.find(string=lambda t: 'chi siamo' in t.lower()) else "Storytelling mancante"
        trust = "Trust elements OK (garanzie/resi)" if soup.find(string=lambda t: 'garanzia' in t.lower()) else "Trust elements mancanti"
        return dict(cta=cta, reviews=reviews, footer=footer, storytelling=storytelling, trust=trust)
    except Exception as e:
        st.error(f"Errore analisi: {e}")
        return None

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()

# Main
st.markdown(f"<div style='background-color:{FZY_COLOR};padding:10px;border-radius:5px'><h1 style='color:white'>Fuzzy Marketing</h1></div>", unsafe_allow_html=True)
st.markdown("### Analizza il sito e ti dirò cosa proporre")

url = st.text_input("Inserisci URL")
if st.button("Analizza"):
    if url.startswith("http"):
        data = analyze_site(url)
        if data:
            st.subheader("Homepage Analysis")
            for k,v in data.items():
                st.write(f"- **{k.capitalize()}:** {v}")
            st.subheader("Proposta Hunter")
            st.info("**Intervento Tecnico (2h) - €350**: sistemiamo CTA, recensioni, footer, storytelling e trust per aumentare la conversione.")
    else:
        st.warning("URL non valido")

st.markdown("---")
st.sidebar.header("CLOSER")
origin = st.sidebar.selectbox("Da quale prodotto front-end proviene il cliente?", ["","Strategico","Tecnica","Content"])
if origin:
    st.sidebar.markdown(f"### Hai scelto: {origin}")
    if origin=="Strategico":
        obj = st.sidebar.selectbox("Obiettivo?", ["","Vendita","Incrementare volume","Moltiplicare"])
        if obj:
            desc = {
                "Vendita":"**Pacchetto Start (€1.200):** primo approccio ADV + email per generare vendite immediate.",
                "Incrementare volume":"**Pacchetto Top (€1.500):** ADV + Newsletter + Social per più touchpoint e lead.",
                "Moltiplicare":"**Performance (€2.000):** Flows email + Blog + ADV per crescita esponenziale."
            }
            st.sidebar.write(desc[obj])
    elif origin=="Tecnica":
        obj = st.sidebar.selectbox("Obiettivo?", ["","Creazione sito","Vendere","Incrementare volume"])
        if obj:
            desc = {
                "Creazione sito":"**Restyling (€1.500):** nuova UX/UI ottimizzata per vendite e brand story.",
                "Vendere":"**Start (€1.200):** ADV + email su landing ottimizzate.",
                "Incrementare volume":"**Top (€1.500):** ADV + Newsletter + Social."
            }
            st.sidebar.write(desc[obj])
    else:
        obj = st.sidebar.selectbox("Obiettivo?", ["","Visibilità","Vendere","Incrementare volume"])
        if obj:
            desc = {
                "Visibilità":"**Content (€1.000):** video, social e blog per awareness.",
                "Vendere":"**Start (€1.200):** ADV + email base.",
                "Incrementare volume":"**Top (€1.500):** ADV + Newsletter + Social."
            }
            st.sidebar.write(desc[obj])