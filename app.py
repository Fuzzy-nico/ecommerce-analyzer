
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: white !important;
        color: #000 !important;
    }
    .stButton>button {
        background-color: #0055A4 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Fuzzy Marketing - Ecommerce Analyzer")

if 'email' not in st.session_state:
    email = st.text_input("Inserisci la tua email per iniziare:", key="login_email")
    if st.button("Accedi"):
        if email and "@" in email:
            st.session_state.email = email
            st.experimental_rerun()
        else:
            st.error("Inserisci un'email valida.")
else:
    st.subheader(f"Benvenuto, {st.session_state.email}!")
    st.markdown("---")

    st.header("🔍 Analisi Completa del Sito eCommerce")
    home_url = st.text_input("URL Home Page:")
    review_url = st.text_input("URL Pagina Recensioni (opzionale):")
    product_url = st.text_input("URL Pagina Prodotto (opzionale):")
    footer_url = st.text_input("URL Pagina Footer (opzionale):")
    if st.button("Esegui Analisi"):
        def analyze_page(url, name):
            try:
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.string if soup.title else "Nessun titolo"
                desc_tag = soup.find("meta", attrs={"name": "description"})
                desc = desc_tag["content"] if desc_tag else "Nessuna descrizione"
                issues = []
                if r.status_code != 200:
                    issues.append(f"Pagina {name}: Status code {r.status_code}")
                if not title or len(title) < 10:
                    issues.append(f"Pagina {name}: Titolo poco descrittivo")
                if not desc or len(desc) < 50:
                    issues.append(f"Pagina {name}: Meta description mancante o breve")
                return title, desc, issues
            except Exception as e:
                return None, None, [f"Errore nel caricare {name}: {e}"]

        analysis_results = {}
        for (url, label) in [(home_url, "Home"), (review_url, "Recensioni"),
                             (product_url, "Prodotto"), (footer_url, "Footer")]:
            if url:
                title, desc, issues = analyze_page(url, label)
                analysis_results[label] = {"title": title, "description": desc, "issues": issues}

        for label, data in analysis_results.items():
            st.subheader(f"📄 Pagina {label}")
            st.write(f"**Titolo:** {data['title']}")
            st.write(f"**Meta Description:** {data['description']}")
            if data['issues']:
                st.write("**Problemi rilevati:**")
                for issue in data['issues']:
                    st.write(f"- {issue}")
            else:
                st.write("Nessun problema rilevato.")
            st.markdown("---")

    st.header("💬 Chat Interattiva con Assistente Fuzzy (GPT-4)")
    st.write("Per usare la chat, configura la variabile d'ambiente OPENAI_API_KEY.")

    user_prompt = st.text_input("Parla con Fuzzy:", key="chat_input")
    if user_prompt:
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            st.error("Variabile OPENAI_API_KEY non configurata.")
        else:
            try:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Sei Fuzzy, un assistente di marketing esperto."},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=400
                )
                text = response.choices[0].message.content
                st.markdown(f"**Fuzzy:** {text}")
            except Exception as e:
                st.error(f"Errore nella chat: {e}")
