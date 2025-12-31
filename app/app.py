import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from datetime import datetime

# -----------------------------------------
# PAGE CONFIG + AUTO DARK MODE
# -----------------------------------------
current_hour = datetime.now().hour
auto_dark = current_hour >= 19 or current_hour < 6

st.set_page_config(
    page_title="MedCare Clinical AI Suite",
    page_icon="💊",
    layout="wide"
)

st.title("🏥 MedCare Clinical AI Suite")
st.markdown("### Clinical Accuracy. Powered by AI – Your AI Pharmacist 🔥")

# -----------------------------------------
# Load AI Client
# -----------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------
# LOAD CSV DATA
# -----------------------------------------
clinical_data = pd.read_csv("data/clinical_details.csv")
brand_data = pd.read_csv("data/brand_details.csv")
interaction_data = pd.read_csv("data/drug_interactions.csv")

possible_cols = ["drug", "generic_name", "brand_name", "Drug Name"]
drug_col = next((c for c in possible_cols if c in clinical_data.columns), None)

if not drug_col:
    st.error("Drug column not found in dataset ❌")
    st.stop()

drug_names = sorted(clinical_data[drug_col].dropna().astype(str).unique())

# -----------------------------------------
# LOAD EMBEDDINGS + INDEX
# -----------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("model/drug_embeddings.faiss")

def semantic_search(drug_query):
    vec = model.encode([drug_query]).astype("float32")
    _, idx = index.search(vec, 1)
    return clinical_data.iloc[idx[0][0]]


# -----------------------------------------
# ADMIN LOGIN
# -----------------------------------------
st.sidebar.header("🔐 Admin Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
pin = st.sidebar.text_input("PIN", type="password")

if st.sidebar.button("Login"):
    if username == "MedAdmin" and password == "MedCare@9066" and pin == "306090":
        st.session_state.logged_in = True
        st.sidebar.success("Admin Mode Enabled 🔐")
    else:
        st.sidebar.error("Invalid credentials ❌")

# -----------------------------------------
# TABS
# -----------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Clinical Info",
    "🪙 Brand Comparison",
    "⚠️ Drug Interactions",
    "🧮 Dose Calculator"
])

# -----------------------------------------
# TAB 1 - CLINICAL MONOGRAPH
# -----------------------------------------
with tab1:
    st.subheader("📄 Clinical Monograph Assistant")
    drug = st.selectbox("Select Drug", drug_names)

    if st.button("Get Clinical Info"):
        match = semantic_search(drug)

        with st.spinner("Fetching verified clinical data..."):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content":
                     "You are a clinical pharmacist. Provide safety-verified drug information."},
                    {"role": "user", "content": f"Drug name: {drug}"}
                ],
                max_tokens=500
            )

        ai_info = response.choices[0].message.content

        st.success(f"### {drug}")
        st.write(ai_info)

        st.download_button(
            "📄 Download Clinical Monograph",
            ai_info.encode("utf-8"),
            file_name=f"{drug}_monograph.pdf",
            mime="application/pdf"
        )


# -----------------------------------------
# TAB 2 - BRAND COMPARISON
# -----------------------------------------
with tab2:
    st.subheader("🪙 Brand Comparison")
    drug_bc = st.selectbox("Select medicine", drug_names, key="brand")

    if st.button("Compare Brands"):
        df = brand_data[brand_data[drug_col] == drug_bc]
        if df.empty:
            st.warning("No brand details available.")
        else:
            st.dataframe(df)


# -----------------------------------------
# TAB 3 - INTERACTION CHECKER
# -----------------------------------------
with tab3:
    st.subheader("⚠️ Drug Interaction Checker")
    d1 = st.selectbox("Drug A", drug_names)
    d2 = st.selectbox("Drug B", drug_names)

    if st.button("Check Interaction"):
        match = interaction_data[
            (interaction_data[drug_col] == d1) &
            (interaction_data["interacts_with"] == d2)
        ]

        if match.empty:
            st.success("No significant interaction found ✔")
        else:
            row = match.iloc[0]
            st.error(f"⚠️ {row['severity']} Interaction")
            st.write(row["description"])


# -----------------------------------------
# TAB 4 - DOSE CALCULATOR
# -----------------------------------------
with tab4:
    st.subheader("🧮 Dose Calculator")
    weight = st.number_input("Weight (kg)", 1, 200, 60)
    mgkg = st.number_input("Dose (mg/kg)", 1, 50, 10)

    if st.button("Calculate"):
        st.success(f"Recommended Dose: {weight * mgkg} mg 💊")
