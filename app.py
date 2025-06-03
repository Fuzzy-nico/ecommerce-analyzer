
import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# Impostazioni base di Streamlit
st.set_page_config(page_title="Ecommerce Analyzer", layout="wide")

# -----------------------------
# SEZIONE HEADER CON LOGO/FUOCO
# -----------------------------
st.markdown(
    """
    <style>
    /* Sfondo sfumato blu → azzurro */
    .stApp {
      background: linear-gradient(135deg, #004080, #40a0ff);
      color: white;
    }
    /* Rimuovo padding orizzontale per occupare tutto lo spazio */
    .main .block-container {
      padding-left: 2rem;
      padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Provo a caricare il logo.png solo se esiste
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.markdown("<h1 style='color: white;'>Fuzzy Marketing</h1>", unsafe_allow_html=True)

st.title("🔍 Ecommerce Analyzer")
st.markdown(
    "<p style='color: white; font-size: 16px;'>Analizza un sito eCommerce e ottieni insight utili in pochi secondi.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# SEZIONE INPUT URL
# -----------------------------
url = st.text_input("Inserisci l'URL del sito eCommerce da analizzare", "https://")

if st.button("Analizza Sito"):
    st.info("🚀 Avvio analisi...")
    if not url.startswith("http"):
        st.error("⚠️ Inserisci un URL valido che inizi con http o https")
    else:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            problemi = []

            # 1) Controllo <title>
            title_tag = soup.title.string.strip() if soup.title else ""
            if not title_tag:
                problemi.append("❌ Mancanza del tag <title> o titolo vuoto.")

            # 2) Controllo <meta name='description'>
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if not meta_desc or not meta_desc.get("content", "").strip():
                problemi.append("❌ Mancanza di meta description o campo vuoto.")

            # 3) Controllo se nel body c'è "about" o "chi siamo"
            body_text = soup.get_text(separator=" ").lower()
            if ("about" not in body_text) and ("chi siamo" not in body_text):
                problemi.append("❌ Nella homepage non ho trovato una sezione “Chi siamo” o “About”.")

            # 4) Controllo se è presente un footer (copyright o contatti)
            footer = soup.find("footer")
            has_footer = bool(footer and footer.get_text().strip())
            if not has_footer:
                # Provo a cercare una stringa "©" nel body
                if "©" not in body_text:
                    problemi.append("❌ Non è stato trovato un tag <footer> o simbolo © per i contatti.")

            # 5) Raccolgo fino a 3 URL contenenti "product" o "prodotto"
            product_links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if ("product" in href.lower() or "prodotto" in href.lower()) and href.startswith("http"):
                    if href not in product_links:
                        product_links.append(href)
                if len(product_links) >= 3:
                    break

            # 6) Per ciascuna pagina prodotto: controllo h1, descrizione e recensioni
            for idx, prod_url in enumerate(product_links, start=1):
                try:
                    r2 = requests.get(prod_url, timeout=7)
                    soup2 = BeautifulSoup(r2.text, "html.parser")
                    h1 = soup2.find("h1")
                    if not h1 or not h1.get_text().strip():
                        problemi.append(f"❌ [Prodotto {idx}] Mancanza di <h1> nella pagina {prod_url}")

                    # Controllo se c'è troppo testo “prezzo-centrico”
                    testo_totale = soup2.get_text(separator=" ")
                    if "€" in testo_totale:
                        if len(testo_totale) < 200:
                            problemi.append(f"⚠️ [Prodotto {idx}] Testo troppo corto (<200 caratteri) ma con simbolo €.")

                    # Controllo presenza recensioni/testimonianze
                    if "recension" not in testo_totale.lower():
                        problemi.append(f"⚠️ [Prodotto {idx}] Mancano recensioni/testimonianze (parola “recension”)")

                except Exception as e_prod:
                    problemi.append(f"⚠️ Errore nel caricare pagina prodotto: {prod_url} ({e_prod})")

            # ========================
            # OUTPUT DEI RISULTATI
            # ========================
            if len(problemi) == 0:
                st.success("🎉 Nessun problema riscontrato sulle sezioni controllate.")
            else:
                st.error("--- Risultati Analisi ---")
                for p in problemi:
                    st.write(p)

        except Exception as e:
            st.error(f"Errore nell'analisi: {e}")

st.markdown("---")

# ==================================
# SEZIONE CHAT “RISPOSTE A DOMANDE”
# ==================================
st.subheader("💬 Chat Assistant Fuzzy Marketing")
st.write(
    "Scrivi qui sotto la tua domanda (es. “Intervento tecnico”, “Intervento strategico”, “SEO”…) e premi Invio. "
    "L’assistente risponderà in modo sintetico."
)

# Campo di input e logica di risposta
if "history" not in st.session_state:
    st.session_state.history = []

msg = st.text_input("Scrivi la tua domanda qui (es. ‘Intervento tecnico’):")
if msg:
    st.session_state.history.append({"role": "user", "content": msg})
    lower = msg.lower()

    # Rule‐based semplici per risposte rapide
    if "intervento tecnico" in lower:
        reply = (
            "🔧 **Intervento Tecnico (€350)**:\n"
            "- 2 ore di supporto live via videocall con condivisione schermo\n"
            "- Risolvi configurazioni avanzate, ottimizzazioni di performance e bug\n"
            "- Ideale se il sito è lento, ha problemi di navigazione o integrazioni fallite\n"
            "→ Prenota un tecnico e ripulisci subito i problemi sotto il cofano."
        )
    elif "intervento strategico" in lower:
        reply = (
            "🧠 **Intervento Strategico (€500)**:\n"
            "- 2 ore di consulenza via videocall con analisi del funnel di vendita\n"
            "- Definizione di strategia marketing, ottimizzazione campagne ADV, analisi KPI\n"
            "- Ideale per rilanciare vendite, rinnovare posizionamento e pianificazione adv\n"
            "→ Prenota un consulente strategico per far decollare il tuo eCommerce."
        )
    elif "seo" in lower:
        reply = (
            "🔍 **Intervento SEO (da €500)**:\n"
            "- Audit con tool SBAM, ottimizzazione Title, Meta Description e strutture dati\n"
            "- Keyword research, link interni, velocità di caricamento e mobile‐friendly\n"
            "- Ideale se hai bassi volumi di traffico organico o posizionamento scarso\n"
            "→ Prenota un SEO specialist e fai volare il tuo ranking su Google."
        )
    else:
        reply = (
            "❓ Mi dispiace, non ho compreso la tua richiesta. Puoi provare con parole chiave "
            "come “Intervento tecnico”, “Intervento strategico” o “SEO”?"
        )

    st.session_state.history.append({"role": "assistant", "content": reply})

# Stampo a video la cronologia della chat
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**Tu:** {chat['content']}")
    else:
        st.markdown(f"**Fuzzy:** {chat['content']}")
