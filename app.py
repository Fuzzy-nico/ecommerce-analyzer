import streamlit as st
import requests
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# CONFIGURAZIONE DELLA PAGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="🔍 Ecommerce Analyzer",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------
# CARICAMENTO LOGO
# ------------------------------------------------------------
with st.sidebar:
    st.image("logo.png", width=200)  # regola "width" come preferisci

# ------------------------------------------------------------
# HEADER PRINCIPALE
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
        margin-top: 10px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🔍 Ecommerce Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analizza un sito e-commerce e ottieni insight utili in pochi secondi</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# SEZIONE 1: INPUT EMAIL E RUOLO
# ------------------------------------------------------------
st.subheader("👤 Accedi al sistema")

# Input per l'email
user_email = st.text_input(
    "Inserisci la tua email per accedere:",
    placeholder="nome.cognome@esempio.com"
)

if user_email and "@" in user_email:
    st.success(f"✅ Benvenuto {user_email.split('@')[0]}")
    st.write("Chi sei?")
    role = st.radio(
        label="",
        options=["Hunter", "Responsabile"],
        index=0
    )
    st.markdown("---")
else:
    st.warning("🚨 Devi inserire un’email valida per continuare.")
    st.stop()

# ------------------------------------------------------------
# SEZIONE 2: INPUT URL E BOTTONE ANALIZZA
# ------------------------------------------------------------
st.subheader("🖇️ Inserisci il link dell'e-commerce da analizzare")
ecom_url = st.text_input(
    "",
    placeholder="https://www.tuo-ecommerce.com"
)

if st.button("🔎 Analizza"):
    if not ecom_url.startswith("http"):
        st.error("⚠️ Inserisci un URL valido che inizi con http o https.")
        st.stop()
    else:
        try:
            response = requests.get(ecom_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "Nessun titolo trovato"
            desc_tag = soup.find("meta", attrs={"name": "description"})
            meta_desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "Nessuna descrizione trovata"
            h1_tags = soup.find_all("h1")
            h1_count = len(h1_tags)

            fb_pixel = False
            if soup.find("script", string=lambda x: x and "facebook.com/tr" in x):
                fb_pixel = True

            ga_pixel = False
            if soup.find("script", string=lambda x: x and "gtag(" in x):
                ga_pixel = True

            cms_shopify = False
            meta_gen = soup.find("meta", attrs={"name": "generator"})
            if meta_gen and "Shopify" in meta_gen.get("content", ""):
                cms_shopify = True

            st.success("✅ Analisi completata")
            st.markdown("## 📈 SEO & Contenuti")
            st.markdown(f"**Titolo:** {title}")
            st.markdown(f"**Meta Description:** {meta_desc}")
            st.markdown(f"**Tag H1 trovati:** {h1_count}")
            st.markdown("---")

            st.markdown("## 🎯 Pixel e Tracciamenti")
            st.markdown(f"- Meta Pixel Facebook: {'✅ Rilevato' if fb_pixel else '❌ Non rilevato'}")
            st.markdown(f"- Google Analytics (gtag): {'✅ Rilevato' if ga_pixel else '❌ Non rilevato'}")
            st.markdown("---")

            st.markdown("## 🛠️ CMS utilizzato")
            st.markdown(f"- Shopify: {'✅ Sì' if cms_shopify else '❌ No'}")
            st.markdown("---")

            st.markdown("## 💼 Cosa proporre al cliente")
            if not fb_pixel:
                st.info("💡 **Suggerimento:** Proponi il Pacchetto Tecnico")
                st.markdown("> ✍️ **Motivo:** Manca il Meta Pixel, quindi il sito non può tracciare chi visita e chi acquista.")
            else:
                st.info("💡 **Suggerimento:** Proponi il Pacchetto Strategico")
                st.markdown("> ✍️ **Motivo:** Hai già il Pixel attivo, conviene ottimizzare le campagne e migliorare la strategia.")
            st.markdown("---")

        except Exception as e:
            st.error(f"Errore nell'analisi del sito: {e}")
            st.stop()

else:
    st.info("📌 Premi 'Analizza' per iniziare l’analisi dell’e-commerce.")
    st.stop()

# ------------------------------------------------------------
# SEZIONE 3: CHAT ASSISTENTE (OBIEZIONI COMUNI)
# ------------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("💬 Chat assistente Fuzzy: risposte a obiezioni")
try:
    msg = st.text_input("Scrivi l'obiezione ricevuta dal cliente")
    if msg:
        if "troppo caro" in msg.lower():
            risposta = (
                "Capisco che il prezzo possa sembrare elevato, "
                "ma considera che faremo interventi mirati e personalizzati "
                "che porteranno un ritorno sull’investimento nel medio-breve termine. "
                "In più, forniamo report dettagliati e supporto continuo per massimizzare i risultati."
            )
        elif "non ho tempo" in msg.lower():
            risposta = (
                "È comprensibile; proprio per questo il nostro intervento "
                "è studiato per essere rapido e super mirato. In due ore risolviamo "
                "i problemi principali e ti consegniamo un report con gli step successivi."
            )
        else:
            risposta = "Grazie per la tua obiezione. Ti contatteremo a breve per approfondire."
        st.markdown(f"**Risposta Fuzzy:** {risposta}")
except Exception as e:
    st.error(f"Errore nella sezione chat: {e}")

# ------------------------------------------------------------
# FINE DEL FILE
# ------------------------------------------------------------
