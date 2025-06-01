
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

# Logo
st.image("logo_fuzzy_corretto.png", width=200)
st.markdown("<h1 style='color:#007BFF;'>Fuzzy Ecommerce Analyzer</h1>", unsafe_allow_html=True)

# Scelta ruolo
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"], horizontal=True)

# Inserimento URL
url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare")

if st.button("Analizza"):
    if not url.startswith("http"):
        st.warning("Inserisci un URL valido che inizi con http o https.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')

            st.success("✅ Analisi completata")

            # SEO base
            st.subheader("📈 SEO & Contenuti")
            title = soup.title.string.strip() if soup.title else "❌ Titolo mancante"
            st.markdown(f"**Titolo:** {title}")

            meta_desc = soup.find("meta", attrs={"name": "description"})
            st.markdown("**Meta Description:** " + (meta_desc["content"].strip() if meta_desc else "❌ Non presente"))

            h1_tags = soup.find_all("h1")
            st.markdown(f"**Tag H1 trovati:** {len(h1_tags)}" if h1_tags else "❌ Nessun H1 presente")

            # Pixel & tracking
            st.subheader("🎯 Pixel e Tracciamenti")
            html = str(soup)
            pixel_fb = "🟢 Meta Pixel rilevato" if "connect.facebook.net" in html else "❌ Meta Pixel assente"
            pixel_gg = "🟢 Google Analytics rilevato" if "gtag(" in html or "google-analytics" in html else "❌ Google Analytics assente"
            st.markdown(pixel_fb)
            st.markdown(pixel_gg)

            # CMS detection (base)
            st.subheader("🛠️ CMS utilizzato")
            if "cdn.shopify.com" in html or "myshopify.com" in html:
                st.markdown("✅ **Shopify** rilevato")
            elif "woocommerce" in html:
                st.markdown("✅ **WooCommerce** rilevato")
            elif "wordpress" in html:
                st.markdown("✅ **WordPress** rilevato")
            else:
                st.markdown("❌ CMS non rilevato automaticamente")

            # Suggerimenti vendita (ruolo-based)
            st.subheader("💼 Cosa proporre al cliente")

            suggerimenti = []

            if ruolo == "Hunter":
                if not meta_desc: suggerimenti.append("👉 Proponi Intervento Content (manca meta description)")
                if not h1_tags: suggerimenti.append("👉 Proponi Pacchetto SEO (mancano H1)")
                if "connect.facebook.net" not in html: suggerimenti.append("👉 Proponi Pacchetto Tecnico (pixel assente)")
                if "cdn.shopify.com" in html and "gtag(" not in html: suggerimenti.append("👉 Proponi Pacchetto Strategico per impostare tracking)")

            if ruolo == "Responsabile":
                if "gtag(" not in html: suggerimenti.append("👉 Proponi Setup ADV Google")
                if "connect.facebook.net" not in html: suggerimenti.append("👉 Proponi ADV Meta")
                if len(h1_tags) == 0: suggerimenti.append("👉 Proponi Restyling SEO-Friendly")
                if not meta_desc: suggerimenti.append("👉 Proponi revisione contenuti e schema strategico")

            if suggerimenti:
                for s in suggerimenti:
                    st.markdown(s)
            else:
                st.success("✅ Il sito è configurato bene. Ottimo per spingere upgrade strategici!")

            st.markdown("---")
            st.markdown("🔗 [Fuzzy Marketing](https://fuzzymarketing.it) — Strumento interno per supporto commerciale.")

        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")
