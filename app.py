
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="centered")

# Login semplice via email
email = st.text_input("Inserisci la tua email per accedere:")
if email:
    st.success(f"✅ Benvenuto {email.split('@')[0].capitalize()}")

    ruolo = st.radio("Chi sei?", ["Hunter", "Responsabile"])

    url = st.text_input("🔗 Inserisci il link dell'ecommerce da analizzare")

    if st.button("Analizza") and url:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else "Titolo non trovato"
            meta_desc_tag = soup.find("meta", attrs={"name": "description"})
            description = meta_desc_tag.get("content").strip() if meta_desc_tag and meta_desc_tag.get("content") else "Nessuna description trovata"
            h1_count = len(soup.find_all("h1"))
            pixel = "Meta Pixel" if "https://connect.facebook.net" in r.text else "Non rilevato"
            ga = "Google Analytics" if "gtag(" in r.text else "Non rilevato"
            cms = "Shopify" if "cdn.shopify" in r.text else "Non rilevato"

            st.success("✅ Analisi completata")
            st.subheader("📊 SEO & Contenuti")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta Description:** {description}")
            st.markdown(f"**Tag H1 trovati:** {h1_count}")

            st.subheader("🎯 Pixel e Tracciamenti")
            st.markdown(f"{'✅' if pixel != 'Non rilevato' else '❌'} {pixel}")
            st.markdown(f"{'✅' if ga != 'Non rilevato' else '❌'} {ga}")

            st.subheader("🛠️ CMS utilizzato")
            st.markdown(f"{'✅' if cms != 'Non rilevato' else '❌'} {cms}")

            st.subheader("💼 Cosa proporre al cliente")

            suggerimento = ""
            motivo = ""

            if ruolo == "Hunter":
                if pixel == "Non rilevato":
                    suggerimento = "Proponi il Pacchetto Tecnico"
                    motivo = "Perché manca il Meta Pixel, quindi il sito non può tracciare chi visita e chi acquista."
                elif description == "Nessuna description trovata" or h1_count == 0:
                    suggerimento = "Proponi il Pacchetto SEO"
                    motivo = "Perché il sito non è indicizzato e le pagine non portano traffico."
                elif cms == "Shopify" and pixel == "Non rilevato":
                    suggerimento = "Proponi il Pacchetto Strategico"
                    motivo = "Perché il sito è attivo ma senza tracciamenti né struttura di vendita."

            if ruolo == "Responsabile":
                if "chi siamo" not in r.text.lower() or "recensioni" not in r.text.lower():
                    suggerimento = "Proponi un Intervento Tecnico"
                    motivo = "Perché la homepage non comunica credibilità, fiducia e autorità."
                elif pixel == "Non rilevato" and ga == "Non rilevato":
                    suggerimento = "Proponi un Intervento Strategico"
                    motivo = "Perché il sito va lanciato ma mancano tracciamenti e controllo delle visite."
                elif "wordpress" in r.text.lower() and len(soup.find_all("p")) < 5:
                    suggerimento = "Proponi un Intervento Content"
                    motivo = "Perché i contenuti sono poveri o inesistenti."

            if suggerimento:
                st.success(f"💬 Suggerimento: {suggerimento}")
                st.markdown(f"✍️ **Motivo:** {motivo}")
            else:
                st.warning("Nessun pacchetto consigliato automaticamente.")

        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")
