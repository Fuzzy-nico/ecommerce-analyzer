import streamlit as st
import requests
from bs4 import BeautifulSoup

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# Custom CSS for background gradient and styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #ffffff;
    }
    .stApp {
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        color: #000000;
    }
    .stButton>button {
        background-color: #ffffff;
        color: #4facfe;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login interface
if not st.session_state.logged_in:
    st.title("🔑 Fuzzy Marketing")
    st.write("Accedi con la tua email per iniziare")
    email = st.text_input("Email", "")
    if st.button("Accedi"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            # Extract name before @ if possible
            username = email.split('@')[0]
            st.experimental_rerun()
        else:
            st.warning("Inserisci un'email valida.")
else:
    # Welcome message
    username = st.session_state.user_email.split('@')[0]
    st.title(f"👋 Benvenuto, {username}!")
    st.subheader("Ecommerce Analyzer")

    # Input URL
    url = st.text_input("Inserisci l'URL del sito ecommerce da analizzare", "https://")

    if st.button("Analizza"):
        if url.startswith("http"):
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.title.string if soup.title else "Nessun titolo trovato"
                description = soup.find("meta", attrs={"name": "description"})
                description = description["content"] if description else "Nessuna descrizione trovata"

                # Check for homepage storytelling
                homepage_text = soup.get_text().lower()
                storytelling_flag = any(keyword in homepage_text for keyword in ["chi siamo", "who we are", "about us"])

                # Check for product pages (looking for '/product/' URLs or 'add to cart' buttons)
                product_elements = soup.select("a, button")
                product_flag = any("product" in (el.get("href") or "").lower() or "add to cart" in el.text.lower() for el in product_elements)

                # Check footer for company info
                footer = soup.find("footer")
                footer_text = footer.get_text().lower() if footer else ""
                footer_flag = any(keyword in footer_text for keyword in ["©", "contatti", "privacy", "terms", "address", "p.iva"])

                # Check for reviews or testimonials
                reviews_flag = any(keyword in homepage_text for keyword in ["recensioni", "testimonials", "reviews"])

                st.success("Analisi completata ✅")
                st.markdown(f"**Titolo:** {title}")
                st.markdown(f"**Meta description:** {description}")

                st.markdown("### 📋 Risultati dettagliati:")
                if not storytelling_flag:
                    st.markdown("- ❌ Homepage senza ‘Chi siamo’ o storytelling del brand.")
                else:
                    st.markdown("- ✅ Presenta storytelling del brand.")

                if not product_flag:
                    st.markdown("- ❌ Pagine prodotto non ottimizzate (manca CTA 'add to cart' o URL 'product').")
                else:
                    st.markdown("- ✅ Pagine prodotto rilevate.")

                if not footer_flag:
                    st.markdown("- ❌ Footer privo di informazioni aziendali (©, contatti, privacy, ecc.).")
                else:
                    st.markdown("- ✅ Footer con informazioni aziendali.")

                if not reviews_flag:
                    st.markdown("- ❌ Mancano recensioni/testimonianze sul sito.")
                else:
                    st.markdown("- ✅ Recensioni/testimonianze rilevate.")

                st.markdown("---")
                st.info("🚀 Per soluzioni personalizzate, consulta l'Assistente Fuzzy Marketing qui sotto.")

                # Chat placeholder
                st.markdown("## 💬 Assistente Fuzzy Marketing")
                user_question = st.text_input("Fai una domanda al nostro Assistente...")
                if st.button("Invia"):
                    # Simple rule-based responses based on keywords
                    q_lower = user_question.lower()
                    if "tecnico" in q_lower:
                        st.markdown("**Intervento Tecnico:**
Consigliamo questo servizio quando la homepage manca di storytelling, le pagine prodotto non hanno CTA e il footer è privo di informazioni aziendali. Include ottimizzazioni immediate per credibilità, fiducia e autorità.")
                    elif "strategico" in q_lower:
                        st.markdown("**Intervento Strategico:**
Ideale per chi lancia il sito, vuole validare il mercato, fa ADV ma non ha analytics o pixel installati. Permette di impostare obiettivi chiari e metriche di performance.")
                    elif "seo" in q_lower:
                        st.markdown("**Intervento SEO:**
Necessario quando il sito non è indicizzato, le pagine prodotto non generano traffico organico e si vuole ridurre dipendenza dalle adv.")
                    elif "content" in q_lower:
                        st.markdown("**Intervento Content:**
Perfetto per chi vuole fare personal branding, aumentare l’engagement sui social e portare traffico qualificato allo store.")
                    else:
                        st.markdown("Mi dispiace, non ho capito. Prova a chiedere di un servizio specifico: Tecnico, Strategico, SEO o Content.")

            except Exception as e:
                st.error(f"Errore nell'analisi: {e}")
        else:
            st.warning("Inserisci un URL valido.")