
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", layout="wide")

def login():
    st.title("Fuzzy Marketing - Ecommerce Analyzer")
    email = st.text_input("Inserisci la tua email:")
    if st.button("Accedi"):
        if email.endswith("@fuzzymarketing.it"):
            st.success(f"Benvenuto {email}!")
        else:
            st.error("Email non valida")
            return False
    else:
        st.stop()
    return True

if not login():
    st.stop()

col1, col2 = st.columns([1,3])
with col1:
    st.subheader("🧑‍💼 Hunter")
    role = st.radio("Cosa hai proposto?", ["Hunter","Closer"])
    if role=="Hunter":
        st.markdown("Flusso Hunter invariato")
    else:
        st.subheader("🔑 Closer")
        prod = st.selectbox("Da quale front-end?", ["Strategico","Tecnica","Social"])
        if prod=="Strategico":
            obj = st.selectbox("Obiettivo?", ["Vendita","Incrementare volume","Moltiplicare"])
            if obj=="Vendita": st.markdown("Pacchetto Start — €1.200")
            elif obj=="Incrementare volume": st.markdown("Pacchetto Top — €1.500")
            else: st.markdown("Pacchetto Performance — €2.000")
        elif prod=="Tecnica":
            obj = st.selectbox("Obiettivo?", ["Creazione sito","Vendere","Incrementare volume"])
            if obj=="Creazione sito": st.markdown("Pacchetto Restyling — €1.500")
            elif obj=="Vendere": st.markdown("Pacchetto Start — €1.200")
            else: st.markdown("Pacchetto Top — €1.500")
        else:
            obj = st.selectbox("Obiettivo?", ["Visibilità","Vendere","Incrementare volume"])
            if obj=="Visibilità": st.markdown("Pacchetto Social&Go — €1.000")
            elif obj=="Vendere": st.markdown("Pacchetto Start — €1.200")
            else: st.markdown("Pacchetto Top — €1.500")

with col2:
    st.markdown("# 🔍 Analisi sito")
    url = st.text_input("URL ecommerce")
    if st.button("Analizza"):
        if not url.startswith("http"):
            st.warning("URL non valido")
        else:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                st.success("Analisi completata")
                title = soup.title.string if soup.title else "—"
                desc = soup.find("meta",{"name":"description"})
                desc = desc["content"] if desc else "—"
                problems=[]
                if not soup.find("button"): problems.append("No CTA")
                if not soup.find(class_="review"): problems.append("No recensioni")
                if not soup.find("footer"): problems.append("No footer")
                st.markdown(f"**Titolo**: {title}")
                st.markdown(f"**Desc**: {desc}")
                st.markdown("**Problemi:**")
                for p in problems: st.write(f"- {p}")
            except Exception as e:
                st.error(e)
