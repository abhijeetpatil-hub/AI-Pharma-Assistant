import streamlit as st
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


st.set_page_config(page_title="AI Pharma Assistant", page_icon="💊", layout="centered")
st.title("💊 AI Pharma Assistant")
st.write("Ask me detailed drug information!")

# Load drug names for autocomplete
try:
    india_df = pd.read_csv("data/drugs_india.csv")
    usa_df = pd.read_csv("data/drugs_usa_fda.csv")
    drug_list = sorted(list(set(india_df['brand_name'].dropna().tolist() + usa_df['generic_name'].dropna().tolist())))
except:
    drug_list = []

user_query = st.selectbox("Select or type drug name 👇", options=drug_list, index=None, placeholder="Example: Augmentin")

if st.button("Get Drug Information") and user_query:
    with st.spinner("Fetching verified clinical data..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content":
                 "You are a medical pharmacist. Always provide accurate drug info. Include:\n"
                 "1️⃣ Drug details\n2️⃣ Mechanism\n3️⃣ Dosage (adult + pediatric)\n"
                 "4️⃣ Side effects\n5️⃣ Interactions\n6️⃣ Pregnancy category\n"
                 "7️⃣ Renal/hepatic impairment notes\n"
                 "⚠️ Include emoji alerts for risks:\n"
                 "⚠ safety alert\n🚫 contraindication\n❗ caution\n"
                 },
                {"role": "user", "content": user_query}
            ]
        )
        st.success(response.choices[0].message.content)
else:
    st.info("💡 Tip: Start typing medicine name to see suggestions!")
