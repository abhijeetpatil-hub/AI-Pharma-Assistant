import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Pharma Assistant", page_icon="💊", layout="centered")
st.title("💊 AI Pharma Assistant")
st.write("Ask me about any medicine!")

# User Input
user_query = st.text_input("Enter Drug Name or Question")

if st.button("Get Information") and user_query:
    with st.spinner("Fetching medical data..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical pharmacist. Provide accurate drug info only."},
                {"role": "user", "content": user_query}
            ]
        )
        st.success(response.choices[0].message.content)
else:
    st.info("💡 Example: What is the dose of Paracetamol for adults?")
