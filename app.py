import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Configurazione pagina
st.set_page_config(page_title="Ecommerce Analyzer - Fuzzy Marketing", layout="wide")

# CSS personalizzato per sfondo e colori
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #004a99, #00aaff);
        color: #ffffff;
    }
    .css-1d391kg {  /* Streamlit main text area */
        color: #ffffff;
    }
    .css-ffhzg2 p {
        color: #ffffff;
    }
    .css-h5rgaw {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titolo principale
st.markdown("<h1 style='color: #ffffff; text-align: center;'>Fuzzy Marketing - Ecommerce Analyzer</h1>", unsafe_allow_html=True)

# Login (simulato, basato su email)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    email = st.text_input("Inserisci la tua email per iniziare:", "")
    if email and st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.user = email
        st.experimental_rerun()
else:
    st.markdown(f"<h4 style='color: #ffffff;'>Benvenuto, {st.session_state.user}!</h4>", unsafe_allow_html=True)

    # Sezione di analisi eCommerce
    st.markdown("---")
    st.header("🔍 Analisi Completa del Sito eCommerce")
    homepage_url = st.text_input("URL Home Page:", "")
    reviews_url = st.text_input("URL Pagina Recensioni (opzionale):", "")
    product_url = st.text_input("URL Pagina Prodotto (opzionale):", "")
    footer_url = st.text_input("URL Pagina Footer (opzionale se diverso):", "")

    if st.button("Avvia Analisi Completa"):
        urls = {
            "Home Page": homepage_url,
            "Pagina Recensioni": reviews_url,
            "Pagina Prodotto": product_url,
            "Footer": footer_url
        }
        for section, url in urls.items():
            if url:
                st.subheader(f"Analisi di: {section}")
                try:
                    resp = requests.get(url, timeout=10)
                    html = resp.text
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.string if soup.title else "Nessun titolo trovato"
                    meta_desc = soup.find("meta", attrs={"name": "description"})
                    meta_desc = meta_desc["content"] if meta_desc else "Nessuna meta description"
                    h1 = soup.find("h1")
                    h1_text = h1.get_text().strip() if h1 else "Nessun H1"
                    h2_tags = soup.find_all("h2")
                    img_tags = soup.find_all("img")
                    images_without_alt = [img for img in img_tags if not img.get("alt")]
                    https_check = "HTTPS attivo" if url.startswith("https") else "Non utilizza HTTPS"
                    st.markdown(f"**Titolo pagina:** {title}")
                    st.markdown(f"**Meta Description:** {meta_desc}")
                    st.markdown(f"**H1:** {h1_text}")
                    st.markdown(f"**Numero di H2 presenti:** {len(h2_tags)}")
                    st.markdown(f"**Numero di immagini totali:** {len(img_tags)}")
                    st.markdown(f"**Immagini senza attributo alt:** {len(images_without_alt)}")
                    st.markdown(f"**Controllo HTTPS:** {https_check}")

                    # Consigli
                    st.markdown("**Consigli pratici:**")
                    if not url.startswith("https"):
                        st.markdown("- Attiva HTTPS per maggiore sicurezza e miglior ranking SEO.")
                    if not h1:
                        st.markdown("- Inserisci almeno un H1 descrittivo.")
                    if images_without_alt:
                        st.markdown(f"- Aggiungi attributi alt a tutte le immagini (mancano: {len(images_without_alt)}).")
                    if not meta_desc or meta_desc == "Nessuna meta description":
                        st.markdown("- Scrivi una meta description efficace per migliorare click-through.")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Errore nell'analisi di {section}: {e}")

    # Sezione Chat con GPT-4
    st.markdown("---")
    st.header("💬 Chat Interattiva con Assistente Fuzzy (GPT-4)")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        st.warning("Per usare la chat, imposta la variabile d'ambiente OPENAI_API_KEY.")
    else:
        openai.api_key = openai_api_key
        user_input = st.text_area("Scrivi qui la tua domanda o messaggio:", "")
        if st.button("Invia"):
            if user_input.strip():
                try:
                    with st.spinner("Fuzzy sta pensando..."):
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "Sei Fuzzy, assistente di Fuzzy Marketing. Rispondi con tono professionale e dettagliato."},
                                {"role": "user", "content": user_input}
                            ],
                            max_tokens=500,
                            temperature=0.7
                        )
                    reply = response.choices[0].message.content
                    st.markdown(f"**Assistente Fuzzy:** {reply}")
                except Exception as e:
                    st.error(f"Errore nella chat: {e}")
            else:
                st.warning("Inserisci un messaggio prima di inviare.")
