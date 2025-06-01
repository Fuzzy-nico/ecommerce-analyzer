import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", page_icon="🛒", layout="centered")

# Logo e header
st.markdown("""<h1 style='color:#2196f3;'>Fuzzy Ecommerce Analyzer</h1>""", unsafe_allow_html=True)

# Ruolo
ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"])

# Input
url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare")

if st.button("Analizza"):
    if not url:
        st.warning("Inserisci un URL valido.")
    else:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')

            # Dati SEO
            title = soup.title.string.strip() if soup.title else "Titolo non trovato"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else "Nessuna descrizione trovata"

            h1_tags = soup.find_all("h1")
            h1_count = len(h1_tags)

            # Pixel check
            pixel_present = "facebook.com/tr?id=" in r.text
            analytics_present = "www.google-analytics.com" in r.text

            # CMS check
            shopify = "cdn.shopify.com" in r.text

            # Sezioni obbligatorie (check superficiale)
            homepage_text = soup.get_text().lower()
            homepage_problems = []
            if "chi siamo" not in homepage_text: homepage_problems.append("❌ Sezione 'Chi siamo' assente")
            if "recensioni" not in homepage_text and "testimonianze" not in homepage_text: homepage_problems.append("❌ Mancano recensioni/testimonianze")
            if "contatti" not in homepage_text and "footer" not in homepage_text: homepage_problems.append("❌ Dati aziendali non visibili")

            st.success("✅ Analisi completata")

            st.markdown("### 📋 SEO & Contenuti")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta Description:** {description}")
            st.markdown(f"**Tag H1 trovati:** {h1_count}")

            st.markdown("### 🎯 Pixel e Tracciamenti")
            st.markdown("✅ Google Analytics rilevato" if analytics_present else "❌ Google Analytics assente")
            st.markdown("✅ Meta Pixel rilevato" if pixel_present else "❌ Meta Pixel assente")

            st.markdown("### 🛠️ CMS utilizzato")
            st.markdown("✅ Shopify rilevato" if shopify else "❌ Shopify non rilevato")

            st.markdown("### 📎 Struttura Homepage")
            for issue in homepage_problems:
                st.markdown(issue)
            if not homepage_problems:
                st.markdown("✅ La homepage contiene elementi chiave per la vendita")

            st.markdown("---")

            st.markdown("## 💡 Cosa proporre al cliente")

            # Decidere servizio da proporre
            servizio = None
            motivazione = ""
            pitch = ""

            if ruolo == "Hunter":
                if homepage_problems:
                    servizio = "Intervento Tecnico"
                    motivazione = "La homepage non comunica autorevolezza o fiducia. Mancano elementi chiave per vendere."
                    pitch = "Partiamo sistemando le basi di vendita: racconto del brand, fiducia, credibilità, recensioni, e layout."

                elif not pixel_present:
                    servizio = "Intervento Tecnico"
                    motivazione = "Senza pixel non possiamo tracciare chi visita o compra."
                    pitch = "Senza tracciamento, stai volando alla cieca. Iniziamo da qui."

                elif h1_count <= 1:
                    servizio = "SEO + Tecnico"
                    motivazione = "Le pagine non sono strutturate per Google. Poco traffico organico."
                    pitch = "Ottimizziamo struttura e contenuti per portare traffico senza ADV."

                else:
                    servizio = "Intervento Strategico"
                    motivazione = "Il sito sembra completo ma serve capire gli obiettivi per creare una strategia di vendita."
                    pitch = "Facciamo chiarezza su cosa vuoi ottenere online: vendite, lead o traffico."

            elif ruolo == "Responsabile":
                if "chi siamo" not in homepage_text and not pixel_present:
                    servizio = "Restyling + Tecnico"
                    motivazione = "Il sito va rifatto. Mancano le basi."
                    pitch = "Serve una nuova immagine + tracciamento per iniziare a vendere."

                elif shopify and not analytics_present and not pixel_present:
                    servizio = "Tecnico + Strategico"
                    motivazione = "Il sito è online ma non misura nulla. Non possiamo scalare."
                    pitch = "Mettiamo ordine: tracciamenti + obiettivi + struttura."

                elif "blog" not in homepage_text and "articoli" not in homepage_text:
                    servizio = "Intervento Content"
                    motivazione = "Manca contenuto di supporto alla vendita. Nessuna autorevolezza."
                    pitch = "Aggiungiamo contenuti che dimostrano esperienza, risolvono dubbi e portano fiducia."

                else:
                    servizio = "Intervento Strategico"
                    motivazione = "Serve definire funnel, offerte e messaggi coerenti."
                    pitch = "Impostiamo una strategia su misura per far crescere le vendite."

            st.markdown(f"👉 **Proponi:** {servizio}")
            st.markdown(f"**Perché:** {motivazione}")
            st.info(f"💬 Pitch: {pitch}")

        except Exception as e:
            st.error(f"Errore nell'analisi del sito: {e}")
