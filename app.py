
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Page config
st.set_page_config(page_title="Fuzzy Marketing Analyzer", layout="wide")
FZY_COLOR = "#87efff"
CLOSER_BTN = "CLOSER"

# Login function
def login():
    st.markdown(
        f"""<div style='background-color:{FZY_COLOR};padding:50px;border-radius:10px'>
        <h1 style='color:white;text-align:center'>Fuzzy Marketing</h1>
        <h3 style='color:white;text-align:center'>Login</h3>
        </div>""", 
        unsafe_allow_html=True
    )
    email = st.text_input("Email")
    if st.button("Accedi"):
        if email:
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Inserisci un'email valida")
    st.stop()

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# If not logged in, show login
if not st.session_state.logged_in:
    login()

# Main interface
st.markdown(f"<div style='background-color:{FZY_COLOR};padding:10px;border-radius:5px'><h1 style='color:white'>Fuzzy Marketing</h1></div>", unsafe_allow_html=True)
st.markdown("### Analizza il sito e ti dirò cosa proporre")
url = st.text_input("Inserisci URL")
if st.button("Analizza"):
    if url.startswith("http"):
        try:
            page = requests.get(url, timeout=5)
            html = page.text
            soup = BeautifulSoup(html, 'html.parser')
            # Homepage analysis
            st.subheader("🏠 Homepage Analysis")
            cta = "OK" if soup.find('a', string=lambda t: t and 'acquista' in t.lower()) else "Mancante"
            reviews = "OK" if soup.find(string=lambda t: 'recension' in t.lower()) else "Mancanti"
            footer = "OK" if soup.find('footer') else "Mancante"
            story = "OK" if soup.find(string=lambda t: 'chi siamo' in t.lower()) else "Mancante"
            trust = "OK" if soup.find(string=lambda t: 'garanzia' in t.lower()) else "Mancante"
            google_pixel = "Presente" if "googletagmanager.com/gtm.js" in html or "gtag('config'" in html else "Assente"
            meta_pixel = "Presente" if "connect.facebook.net" in html or "fbq(" in html else "Assente"
            google_ads = "Attive" if "adsbygoogle.js" in html or "pagead" in html else "Assenti"
            meta_ads = "Attive" if "fbq('track'" in html else "Assenti"
            tech = []
            if 'Shopify' in html:
                tech.append("Shopify")
            if 'wp-content' in html:
                tech.append("WordPress")
            if "ga('create'" in html or 'gtag(' in html:
                tech.append("Google Analytics")
            st.write(f"- **CTA:** {cta}")
            st.write(f"- **Recensioni:** {reviews}")
            st.write(f"- **Footer:** {footer}")
            st.write(f"- **Storytelling:** {story}")
            st.write(f"- **Trust elements:** {trust}")
            st.write(f"- **Pixel Google:** {google_pixel}")
            st.write(f"- **Pixel Meta:** {meta_pixel}")
            st.write(f"- **Google Ads:** {google_ads}")
            st.write(f"- **Meta Ads:** {meta_ads}")
            st.write(f"- **Tecnologie rilevate:** {', '.join(tech) if tech else 'Nessuna'}")
            # Product page
            st.subheader("🛍️ Product Page Analysis")
            prod_url = url if 'product' in url else url.rstrip('/') + '/products/sample'
            prod_page = requests.get(prod_url, timeout=5).text
            psoup = BeautifulSoup(prod_page, 'html.parser')
            desc = psoup.find('meta', {'name': 'description'}) or psoup.find('p')
            st.write(f"- **Descrizione:** {'Presente' if desc else 'Mancante'}")
            st.write(f"- **Recensioni:** {'Presenti' if psoup.find(string=lambda t: 'recension' in t.lower()) else 'Mancanti'}")
            st.write(f"- **Garanzie:** {'Presenti' if psoup.find(string=lambda t: 'garanzia' in t.lower()) else 'Mancanti'}")
            st.write(f"- **Prodotti correlati:** {'Presenti' if psoup.find('a', href=lambda x: x and 'related' in x) else 'Mancanti'}")
            st.write(f"- **Storytelling/Trust:** {'OK' if desc and trust == 'OK' else 'Insufficiente'}")
            # Hunter proposal
            st.subheader("🎯 Proposta Hunter")
            st.info("Intervento Tecnico (2h) - €350: ottimizziamo homepage, product page, pixel e campagne attive per massimizzare le conversioni.")
        except Exception as e:
            st.error(f"Errore analisi: {e}")
    else:
        st.warning("URL non valido")

st.markdown("---")
# CLOSER
st.sidebar.header("CLOSER")
origin = st.sidebar.selectbox("Da quale prodotto front-end proviene il cliente?", ["", "Strategico", "Tecnica", "Content"])
if origin:
    st.sidebar.subheader(f"Intervento: {origin}")
    if origin == "Strategico":
        opt = st.sidebar.selectbox("Obiettivo?", ["", "Vendita", "Incrementare volume", "Moltiplicare"])
        mapping = {
            "Vendita": "**Start (1.200€)**: ADV + email per vendite rapide",
            "Incrementare volume": "**Top (1.500€)**: ADV + Newsletter + Social",
            "Moltiplicare": "**Performance (2.000€)**: Flows email + Blog + ADV"
        }
        if opt:
            st.sidebar.write(mapping[opt])
    elif origin == "Tecnica":
        opt = st.sidebar.selectbox("Obiettivo?", ["", "Creazione sito", "Vendere", "Incrementare volume"])
        mapping = {
            "Creazione sito": "**Restyling (1.500€)**: UX/UI e storytelling",
            "Vendere": "**Start (1.200€)**: ADV + email su landing",
            "Incrementare volume": "**Top (1.500€)**: ADV + Newsletter + Social"
        }
        if opt:
            st.sidebar.write(mapping[opt])
    else:
        opt = st.sidebar.selectbox("Obiettivo?", ["", "Visibilità", "Vendere", "Incrementare volume"])
        mapping = {
            "Visibilità": "**Content (1.000€)**: video, social e blog",
            "Vendere": "**Start (1.200€)**: ADV + email base",
            "Incrementare volume": "**Top (1.500€)**: ADV + Newsletter + Social"
        }
        if opt:
            st.sidebar.write(mapping[opt])
