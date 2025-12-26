import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

st.set_page_config(page_title="AI Pharma Assistant", page_icon="💊", layout="centered")
st.title("💊 AI Pharma Assistant")
st.write("Ask me detailed drug information!")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load drug names
try:
    india_df = pd.read_csv("data/drugs_india.csv")
    usa_df = pd.read_csv("data/drugs_usa_fda.csv")
    drug_list = sorted(list(set(
        india_df['brand_name'].dropna().tolist() +
        usa_df['generic_name'].dropna().tolist()
    )))
except Exception as e:
    st.error(f"Error loading data: {e}")
    drug_list = []

drug = st.selectbox("Select or type drug name 👇", drug_list, index=None, placeholder="Example: Augmentin")

if st.button("Get Drug Information") and drug:
    with st.spinner("Fetching verified clinical data..."):
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content":
                 "You are a clinical pharmacist. Provide:\n"
                 "✔ Drug monograph\n"
                 "✔ Mechanism\n"
                 "✔ Adult & Pediatric dose\n"
                 "✔ Side effects\n"
                 "✔ Interactions\n"
                 "✔ Pregnancy & Renal warnings\n"
                 "⚠️ safety | 🚫 contraindication | ❗ caution"},
                {"role": "user", "content": drug}
            ],
            max_tokens=600
        )
        
        result = response.choices[0].message.content
        st.success(result)
else:
    st.info("💡 Start typing to see medicine name suggestions!")
