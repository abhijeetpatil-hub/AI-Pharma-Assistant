import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env from root folder
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Pharma Assistant", page_icon="💊", layout="centered")
st.title("💊 AI Pharma Assistant")
st.write("Ask me detailed drug information!")

# Load drug names for autocomplete
try:
    india_df = pd.read_csv("data/drugs_india.csv")
    usa_df = pd.read_csv("data/drugs_usa_fda.csv")
    drug_list = sorted(list(set(india_df['brand_name'].dropna().tolist() + usa_df['generic_name'].dropna().tolist())))
except Exception as e:
    st.error(f"Error loading data: {e}")
    drug_list = []

user_query = st.selectbox("Select or type drug name 👇", options=drug_list, index=None, placeholder="Example: Augmentin")

if st.button("Get Drug Information") and user_query:
    with st.spinner("Fetching verified clinical data..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                 "You are a highly accurate clinical pharmacist. Provide:\n"
                 "✔ Drug detailed monograph\n"
                 "✔ Mechanism\n"
                 "✔ Adult & Pediatric dosage\n"
                 "✔ Side effects\n"
                 "✔ Interactions\n"
                 "✔ Pregnancy & Lactation\n"
                 "✔ Renal/Hepatic safety\n"
                 "Include emojis:\n"
                 "⚠️ safety warning, 🚫 contraindication, ❗ caution"},
                {"role": "user", "content": user_query}
            ]
        )
        
        st.success(response["choices"][0]["message"]["content"])
else:
    st.info("💡 Tip: Start typing medicine name to see suggestions!")
