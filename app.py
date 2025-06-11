
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Config
FZY_COLOR = "#87efff"

st.set_page_config(page_title="Fuzzy Marketing Analyzer", layout="wide")

# --- LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown(f"<div style='background-color:{FZY_COLOR};padding:40px;border-radius:10px'><h1 style='color:white;text-align:center'>Fuzzy Marketing</h1><h3 style='color:white;text-align:center'>Login</h3></div>", unsafe_allow_html=True)
    email = st.text_input("Email", key="email")
    if st.button("Accedi"):
        if email:
            st.session_state.logged_in = True
        else:
            st.error("Inserisci un'email valida")
    st.stop()

# --- MAIN Interface ---
st.markdown(f"<div style='background-color:{FZY_COLOR};padding:10px;border-radius:5px'><h1 style='color:white'>Fuzzy Marketing</h1></div>", unsafe_allow_html=True)
st.markdown("### 🔍 Analizza il sito e ti dirò cosa proporre")
url = st.text_input("🌐 URL del sito eCommerce")

if st.button("🚀 Avvia Analisi"):
    if not url.startswith("http"):
        st.warning("❗ Inserisci un URL valido")
    else:
        try:
            html = requests.get(url, timeout=5).text
            soup = BeautifulSoup(html, 'html.parser')
            # Homepage
            st.subheader("🏠 Homepage Analysis")
            st.write(f"- ✅ CTA: {'Presente' if soup.find('a',string=lambda t:t and 'acquista' in t.lower()) else 'Mancante'}")
            st.write(f"- ✅ Recensioni: {'Presente' if soup.find(string=lambda t:'recension' in t.lower()) else 'Mancanti'}")
            st.write(f"- ✅ Footer: {'Presente' if soup.find('footer') else 'Mancante'}")
            st.write(f"- ✅ Storytelling: {'Presente' if soup.find(string=lambda t:'chi siamo' in t.lower()) else 'Mancante'}")
            st.write(f"- ✅ Trust: {'Presente' if soup.find(string=lambda t:'garanzia' in t.lower()) else 'Mancante'}")

            # Pixel & Ads
            st.subheader("📊 Pixel & ADV")
            st.write(f"- Google Pixel: {'Presente' if 'gtm.js' in html or 'gtag(' in html else 'Assente'}")
            st.write(f"- Meta Pixel: {'Presente' if 'connect.facebook.net' in html or 'fbq(' in html else 'Assente'}")
            st.write(f"- Google Ads: {'Attive' if 'pagead' in html else 'Assenti'}")
            st.write(f"- Meta Ads: {'Attive' if "fbq('track'" in html else 'Assenti'}")

            # Tech
            st.subheader("⚙️ Tecnologie")
            tech = []
            if 'Shopify' in html: tech.append("Shopify")
            if 'wp-content' in html: tech.append("WordPress")
            if 'jquery' in html.lower(): tech.append("jQuery")
            if "gtag('config'" in html: tech.append("Google Analytics")
            st.write(", ".join(tech) or "Nessuna")

            # Product Page
            st.subheader("🛍️ Product Page")
            links = [a['href'] for a in soup.find_all('a',href=True) if '/products/' in a['href']]
            if links:
                prod_url = urljoin(url, links[0])
                ph = requests.get(prod_url, timeout=5).text
                psoup = BeautifulSoup(ph,'html.parser')
                st.write(f"- Descrizione: {'Presente' if psoup.find('meta',attrs={'name':'description'}) or psoup.find('p') else 'Mancante'}")
                st.write(f"- Recensioni: {'Presenti' if psoup.find(string=lambda t:'recension' in t.lower()) else 'Mancanti'}")
                st.write(f"- Garanzie: {'Presenti' if psoup.find(string=lambda t:'garanzia' in t.lower()) else 'Mancanti'}")
                st.write(f"- Correlati: {'Presenti' if psoup.find('a', href=lambda x:x and 'related' in x) else 'Mancanti'}")
            else:
                st.error("‼️ Nessun prodotto trovato")

            # Proposal
            st.subheader("🎯 Proposta Hunter")
            st.info(
                "Intervento Tecnico (2h) - €350\n"
                "• Sistema CTA, recensioni, footer, trust\n"
                "• Installa pixel e verifica ADV\n"
                "• Ottimizza UI/UX per convertire"
            )
        except Exception as e:
            st.error(f"Errore: {e}")

st.markdown("---")

# CLOSER
st.sidebar.header("🔑 CLOSER")
sel = st.sidebar.selectbox("COSA HAI PROPOSTO?", ["","Tecnico","Strategico","Content"])
if sel=="Tecnico":
    st.sidebar.markdown("### 🛠️ Intervento Tecnico")
    st.sidebar.write("**Quando:** siti con CTA mancanti, recensioni assenti, footer scarno, trust debole.")
    st.sidebar.write("**Argomentazione:** Prima di marketing, sistema il sito per convertire.")
elif sel=="Strategico":
    st.sidebar.markdown("### 📈 Intervento Strategico")
    st.sidebar.write("**Quando:** start ADV senza pixel/analytics, KPI non chiari, ecommerce in lancio.")
    st.sidebar.write("**Argomentazione:** Prima di budget, imposta tracciamenti e dashboard.")
elif sel=="Content":
    st.sidebar.markdown("### 🎨 Intervento Social/Content")
    st.sidebar.write("**Quando:** assenza social, branding debole, mancanza contenuti.")
    st.sidebar.write("**Argomentazione:** I social creano relazione e valore del brand.")
