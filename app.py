
import streamlit as st
import csv
import os

st.set_page_config(page_title="Fuzzy Marketing - Ecommerce Analyzer", page_icon="📊", layout="centered")

st.markdown(
    f"""
    <div style='text-align: center;'>
        <h1 style='color: #002B5B;'>Fuzzy Marketing</h1>
        <p style='font-size: 20px;'>Analizza il sito e ti dirò cosa devi proporre</p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """<style>
    body {
        background-color: #87efff;
    }
    </style>""", unsafe_allow_html=True
)

st.markdown("## 🔍 Analisi del sito")

role = st.radio("Chi sei?", ["Hunter", "Responsabile"])
url = st.text_input("Inserisci l'URL della home page:")
email = st.text_input("Inserisci la tua email:")

if st.button("Analizza Sito") and url and email:
    # Simulated logic
    analysis = {
        "problemi": "Homepage senza CTA, senza recensioni, footer non a norma",
        "motivazione": "Per aumentare la fiducia e la conversione serve sistemare questi aspetti.",
        "prodotto": "Intervento Tecnico"
    }

    st.success("✅ Analisi completata")

    st.markdown("### 🚨 Problemi trovati")
    st.markdown(f"- {analysis['problemi']}")

    st.markdown("### 🎯 Motivazione commerciale")
    st.markdown(f"{analysis['motivazione']}")

    st.markdown("### 💼 Prodotto da proporre")
    st.markdown(f"**{analysis['prodotto']}**")

    if "storage" not in st.session_state:
        st.session_state["storage"] = []

    st.session_state["storage"].append([email, url, analysis["prodotto"]])

if st.button("📁 Esporta Analisi"):
    if "storage" in st.session_state:
        csv_path = "/mnt/data/export_fuzzy_analisi.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Email", "Sito", "Cosa Proporre"])
            writer.writerows(st.session_state["storage"])
        st.success("File esportato con successo!")
        st.download_button(label="📥 Scarica il file", data=open(csv_path, "rb"), file_name="analisi_export.csv")

