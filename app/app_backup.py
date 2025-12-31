import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(page_title="MedCare Clinical AI Suite", page_icon="💊", layout="wide")
st.title("🏥 MedCare Clinical AI Suite")
st.markdown("### Clinical Accuracy. Powered by AI. Your AI Pharmacist — Always On 💊")

# -------------------
# AUTO DARK MODE SETUP
# -------------------
current_hour = datetime.now().hour
auto_dark = current_hour >= 19 or current_hour < 6

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = auto_dark

theme = st.sidebar.radio("🌓 Theme Mode", ["Light", "Dark"],
                         index=1 if st.session_state.dark_mode else 0)
st.session_state.dark_mode = (theme == "Dark")

# Apply UI theme styles
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .main { background-color: #1E1E1E; color: #FFFFFF; }
        .stTabs [role="tab"] { background-color: #333333; color: white; }
        .stTabs [role="tab"][aria-selected="true"] { background-color: #0078FF !important; }
        </style>
    """, unsafe_allow_html=True)

# -------------------
# LOAD DATA FILES
# -------------------
try:
    clinical_data = pd.read_csv("data/clinical_details.csv")
    brand_data = pd.read_csv("data/brand_details.csv")
    interaction_data = pd.read_csv("data/drug_interactions.csv")
except Exception:
    st.error("❌ Missing data files in 'data/' folder.")
    st.stop()

# Detect correct drug name column
possible_cols = ["drug", "generic_name", "Drug Name", "name"]
drug_col = next((col for col in possible_cols if col in clinical_data.columns), None)
if not drug_col:
    st.error("Drug name column missing!")
    st.stop()

drug_names = sorted(clinical_data[drug_col].dropna().unique().tolist())

# -------------------
# ADMIN LOGIN
# -------------------
st.sidebar.header("🔐 Admin Login")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

u = st.sidebar.text_input("Username")
p = st.sidebar.text_input("Password", type="password")
pin = st.sidebar.text_input("PIN", type="password")

if st.sidebar.button("Login"):
    if u == "MedAdmin" and p == "MedCare@9066" and pin == "306090":
        st.session_state.logged_in = True
        st.sidebar.success("🟢 Admin Mode Enabled")
    else:
        st.sidebar.error("Invalid credentials ❌")

# -------------------
# TABS UI
# -------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Clinical Info",
    "🪙 Brand Comparison",
    "⚠️ Drug Interactions",
    "🧮 Dose Calculator"
])

# -------------------------------------------------
# TAB-1: Clinical Info
# -------------------------------------------------
with tab1:
    st.subheader("📄 Clinical Monograph")
    drug = st.selectbox("Select Medicine", drug_names)

    if st.button("Get Clinical Info"):
        info = clinical_data[clinical_data[drug_col] == drug].iloc[0]

        st.success(f"### {drug}")
        pdf_data = f"Drug Monograph: {drug}\n\n"

        for col in clinical_data.columns:
            if col != drug_col:
                label = col.replace("_", " ").title()
                value = info.get(col, "Not Available")
                st.write(f"**{label}:** {value}")
                pdf_data += f"{label}: {value}\n\n"

        st.download_button(
            label="📄 Download PDF Monograph",
            data=pdf_data.encode("utf-8"),
            file_name=f"{drug}_Monograph.pdf",
            mime="application/pdf"
        )


# -------------------------------------------------
# TAB-2: Brand Comparison
# -------------------------------------------------
with tab2:
    st.subheader("🪙 Brand Comparison")
    drug = st.selectbox("Drug for Brand Comparison", drug_names, key="brand")
    if st.button("Compare Brands"):
        df = brand_data[brand_data[drug_col] == drug]
        st.dataframe(df if not df.empty else "No brand data found")


# -------------------------------------------------
# TAB-3: Drug Interaction Safety
# -------------------------------------------------
with tab3:
    st.subheader("⚠️ Interaction Checker")
    d1 = st.selectbox("Drug A", drug_names, key="DI1")
    d2 = st.selectbox("Drug B", drug_names, key="DI2")

    if st.button("Check Interaction"):
        df = interaction_data[
            (interaction_data[drug_col] == d1) &
            (interaction_data["interacts_with"] == d2)
        ]

        if df.empty:
            st.success("🟢 Safe — No known significant interactions ✔")
        else:
            row = df.iloc[0]
            desc = row["description"]

            # severity detection
            if "avoid" in desc.lower() or "contra" in desc.lower():
                sev = "🔴 Contraindicated — Do NOT combine!"
                st.error(sev)
            elif "serious" in desc.lower():
                sev = "🟠 Major — High clinical risk"
                st.error(sev)
            elif "monitor" in desc.lower():
                sev = "🟡 Moderate — Monitor closely"
                st.warning(sev)
            elif "safe" in desc.lower():
                sev = "🟢 Safe — No worry"
                st.info(sev)
            else:
                sev = "⚪ Minor — Likely safe"
                st.info(sev)

            st.write(f"**Details:** {desc}")


# -------------------------------------------------
# TAB-4: Dose Calculator
# -------------------------------------------------
with tab4:
    st.subheader("🧮 Pediatric Dose Calculator")
    weight = st.number_input("Weight (kg)", 1, 200, 50)
    mgkg = st.number_input("Dose (mg/kg)", 1, 50, 10)

    if st.button("Calculate"):
        st.success(f"Recommended Dose: **{weight * mgkg} mg**")
