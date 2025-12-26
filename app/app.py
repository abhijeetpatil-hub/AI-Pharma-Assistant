import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI

st.set_page_config(page_title="AI Pharma Assistant", page_icon="💊", layout="centered")
st.title("💊 AI Pharma Assistant")
st.write("Ask me detailed drug information!")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

drug = st.selectbox("Select a drug 👇", drug_list)

if st.button("Get Drug Information") and drug:
    st.spinner("Processing...")
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Provide detailed medical information."},
                {"role": "user", "content": drug}
            ]
        )
        st.success(response.choices[0].message.content)
    except Exception as e:
        st.error("Error fetching data: " + str(e))
