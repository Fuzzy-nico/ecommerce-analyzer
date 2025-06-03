
import streamlit as st
import requests
from bs4 import BeautifulSoup

# CSS for background gradient and styling
st.set_page_config(page_title="Fuzzy Ecommerce Analyzer", layout="wide")

page_bg_css = '''
<style>
body {
  margin: 0;
  padding: 0;
}
.stApp {
  background: linear-gradient(135deg, #0072CE, #00AEEF);
  color: #ffffff;
}
header, footer {visibility: hidden;}
</style>
'''
st.markdown(page_bg_css, unsafe_allow_html=True)

# Display logo
st.image("logo.png", width=200)

st.title("🔍 Fuzzy Ecommerce Analyzer")

st.markdown("**Analizza un sito ecommerce per problemi di vendita, SEO e contenuti.**")

# URL input
url = st.text_input("Inserisci l'URL del sito ecommerce", "https://")

if st.button("Analizza"):
    issues = []
    if url.startswith("http"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Check title and meta description
            title = soup.title.string if soup.title else None
            if not title or title.strip() == "":
                issues.append("Titolo mancante o vuoto.")
            description = soup.find("meta", attrs={"name": "description"})
            if not description or not description.get("content", "").strip():
                issues.append("Meta description mancante o generica.")

            # Check for 'chi siamo' or 'about' on homepage
            body_text = soup.get_text(separator=" ").lower()
            if "chi siamo" not in body_text and "about" not in body_text:
                issues.append("Homepage senza sezione 'Chi siamo' o storia del brand.")

            # Check for footer info
            footer = soup.find("footer")
            if not footer:
                issues.append("Footer mancante.")
            else:
                footer_text = footer.get_text().lower()
                if "©" not in footer_text and "contatto" not in footer_text:
                    issues.append("Footer privo di dati aziendali e contatti.")

            # Check for product page links (sample)
            product_links = [a['href'] for a in soup.find_all('a', href=True) if 'product' in a['href'] or 'prodotto' in a['href']]
            sampled = product_links[:3]
            for link in sampled:
                sample_url = link if link.startswith("http") else url.rstrip("/") + "/" + link.lstrip("/")
                try:
                    r2 = requests.get(sample_url, timeout=5)
                    soup2 = BeautifulSoup(r2.text, "html.parser")
                    # Check H1
                    h1 = soup2.find("h1")
                    if not h1:
                        issues.append(f"Pagine prodotto ({sample_url}) senza H1.")
                    # Check for price only vs description: simplistic - look for elements with '€'
                    text2 = soup2.get_text().lower()
                    if "€" in text2 and len(text2) < 200:
                        issues.append(f"Pagine prodotto ({sample_url}) basata solo su prezzo, descrizione breve o mancante storytelling.")
                    # Check for reviews
                    if "recension" not in text2:
                        issues.append(f"Pagine prodotto ({sample_url}) senza recensioni o testimonianze.")
                except:
                    continue

            # Check for reviews site-wide
            if "recension" not in body_text:
                issues.append("Nessuna sezione recensioni/testimonianze trovata.")

            # Display results
            if issues:
                st.error("Problemi rilevati:")
                for i in issues:
                    st.markdown(f"- {i}")
            else:
                st.success("Nessun problema critico rilevato. Il sito sembra in buona ottica di vendita.")

        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")
    else:
        st.warning("Inserisci un URL valido.")

st.markdown("---")

# Chat functionality
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("💬 Chat Assistenza Fuzzy Marketing")
chat_input = st.text_input("Scrivi qui la tua domanda...", key="chat_input")

if st.button("Invia", key="send_button"):
    user_msg = chat_input.strip()
    if user_msg:
        st.session_state.history.append(("Tu", user_msg))
        # Simple rule-based responses
        msg_lower = user_msg.lower()
        if "intervento tecnico" in msg_lower:
            response = "L'intervento tecnico è utile quando il sito non è in ottica di vendita: homepage senza racconto del brand, pagine prodotto incomplete, footer privo di dati aziendali o recensioni. Il pacchetto front-end di 350€ include un'analisi e sistemazione delle principali aree critiche."
        elif "intervento strategico" in msg_lower:
            response = "L'intervento strategico si vende quando il sito deve essere lanciato o ottimizzato per campagne adv, ma manca di strumenti di tracciamento come Analytics o Pixel. Serve a definire obiettivi di vendita chiari e un piano operativo."
        elif "intervento seo" in msg_lower:
            response = "L'intervento SEO si vende quando il sito non ha indicizzazione, le pagine prodotto non portano traffico organico e si vuole ridurre la dipendenza dalle campagne a pagamento."
        elif "intervento content" in msg_lower or "content" in msg_lower:
            response = "L'intervento content è indicato quando si vuole far conoscere il brand tramite storytelling: serve a creare contenuti che portino engagement dai social e affermino la credibilità del marchio."
        else:
            response = "Sono l'Assistente di Fuzzy Marketing: come posso aiutarti? Puoi chiedermi informazioni sui nostri servizi front-end (Tecnico, Strategico, SEO, Content)."

        st.session_state.history.append(("Assistente", response))
    st.experimental_rerun()

for speaker, message in st.session_state.history:
    if speaker == "Tu":
        st.markdown(f"**Tu:** {message}")
    else:
        st.markdown(f"**Assistente:** {message}")
