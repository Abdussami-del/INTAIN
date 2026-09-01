import streamlit as st
import pandas as pd
import os

# 1. Setup page configuration
st.set_page_config(page_title="Loan Performance AI", page_icon="🏦", layout="centered", initial_sidebar_state="collapsed")

# 2. Aggressive Custom CSS to force the floating card UI
st.markdown("""
    <style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Styles */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Hero Title Section */
    .hero-pretitle {
        font-size: 1.25rem;
        color: #4A5568;
        text-align: center;
        margin-top: 2rem;
        font-weight: 500;
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        color: #000000;
        text-align: center;
        line-height: 1.1;
        margin-bottom: 2rem;
    }
    
    /* Avatar / Emoji */
    .avatar-container {
        font-size: 8rem;
        text-align: center;
        margin-bottom: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Custom Tabs Styling to force Floating Cards */
    .stTabs {
        margin-top: 2rem;
    }
    
    /* Force the tab list container to have spacing and no bottom border */
    div[data-baseweb="tab-list"] {
        gap: 16px !important;
        justify-content: center !important;
        border-bottom: none !important;
        padding-bottom: 2rem !important;
    }

    /* Style the individual tab buttons to look like floating white cards */
    button[data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        height: 90px !important;
        min-width: 110px !important;
        padding: 10px !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
    }

    /* Hover effect */
    button[data-baseweb="tab"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important;
    }

    /* Selected Tab state */
    button[data-baseweb="tab"][aria-selected="true"] {
        border: 2px solid #3182CE !important;
        background-color: #FAFCFF !important;
        box-shadow: 0 10px 15px -3px rgba(31, 130, 206, 0.15) !important;
    }
    
    /* Remove the weird blue bottom border indicator Streamlit uses natively */
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* Try to force inline emojis to stack above text if Streamlit allows flex wrap */
    button[data-baseweb="tab"] p {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 4px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #4A5568 !important;
        line-height: 1.2 !important;
    }
    
    /* Watermark text at the bottom */
    .watermark {
        position: fixed;
        bottom: -5vh;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 15vw;
        font-weight: 900;
        color: rgba(0,0,0,0.02);
        z-index: -1;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Hero Section
st.markdown('<div class="hero-pretitle">Hey, I\'m Loan Intel 👋</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">AI Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="avatar-container">🏦</div>', unsafe_allow_html=True)
st.markdown('<div class="watermark">Engine</div>', unsafe_allow_html=True)

# 4. Helper functions
def load_md(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"*File not found: {file_path}*"

def display_image(file_path, caption=""):
    if os.path.exists(file_path):
        st.image(file_path, caption=caption, use_container_width=True)
    else:
        st.warning(f"Image not found: {file_path}")

# 5. Interactive Chat Input (Pill shaped by default in Streamlit)
user_query = st.chat_input("Ask me anything about the loan portfolio...")

# 6. Centralized Navigation (Floating Cards)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Copilot", 
    "📈 Scenarios", 
    "🚨 Anomalies", 
    "🧠 Explain", 
    "📋 Model & Sub"
])

# Handle Chat Interaction immediately above tabs content if triggered
if user_query:
    st.info(f"**You asked:** {user_query}")
    st.success("I am connected to the model! In a live environment, I would summarize this via the Gemini API.")
    st.divider()

# --- TAB 1: AI COPILOT ---
with tab1:
    st.markdown("### 🤖 Reviewer Notes (RAG)")
    if os.path.exists("llm_prompt_logs_rag.csv"):
        df_logs = pd.read_csv("llm_prompt_logs_rag.csv")
        for idx, row in df_logs.iterrows():
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**System Exception:**")
                st.info(row['output'])
                with st.expander("🔍 View Internal RAG Prompt"):
                    st.text(row['prompt'])
    else:
        st.warning("`llm_prompt_logs_rag.csv` not found.")

# --- TAB 2: MACRO SCENARIOS ---
with tab2:
    st.markdown("### 📈 Scenario Report")
    st.markdown("Base, adverse, and high-prepayment scenario outputs.")
    if os.path.exists("scenario_report.csv"):
        df_scenario = pd.read_csv("scenario_report.csv")
        st.dataframe(df_scenario, use_container_width=True, hide_index=True)
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Projected Default Probability**")
            st.bar_chart(df_scenario.pivot(index="state", columns="scenario", values="proj_default_prob"))
        with col2:
            st.markdown("**Projected Prepayment Probability**")
            st.bar_chart(df_scenario.pivot(index="state", columns="scenario", values="proj_prepay_prob"))
    else:
        st.warning("`scenario_report.csv` not found.")

# --- TAB 3: DATA & ANOMALIES ---
with tab3:
    st.markdown("### 📊 Data Intelligence Report")
    st.markdown("Profiling, missingness, outliers, drift, relationship checks, and top anomalies.")
    st.markdown(load_md("reports/data_intelligence_report.md"))
    st.divider()
    st.markdown("### 🚨 Top Anomalies")
    if os.path.exists("reviewer_ready_anomalies.csv"):
        df_anomalies = pd.read_csv("reviewer_ready_anomalies.csv")
        if 'hybrid_risk_score' in df_anomalies.columns:
            df_anomalies['hybrid_risk_score'] = df_anomalies['hybrid_risk_score'].round(4)
        st.dataframe(df_anomalies, use_container_width=True, hide_index=True)

# --- TAB 4: EXPLAINABILITY ---
with tab4:
    st.markdown("### 🧠 Explainability Report")
    st.markdown("Global feature importance, local examples, false positives, false negatives, and model uncertainty.")
    st.markdown(load_md("reports/explainability_report.md"))
    st.divider()
    display_image("reports/task6_global_shap_summary.png", "Global Feature Importance")
    st.divider()
    display_image("reports/task6_local_shap_waterfall.png", "Local Explanation (Waterfall)")
    st.divider()
    display_image("reports/task3_kaplan_meier_baseline.png", "Time-to-Event (Kaplan-Meier Baseline)")

# --- TAB 5: MODEL CARD & SUBMISSION ---
with tab5:
    st.markdown("### 📋 Model Card")
    st.markdown("Objective, data, features, model type, validation method, metrics, limitations, leakage controls, and known failure modes.")
    st.markdown(load_md("model_card.md"))
    
    st.divider()
    st.markdown("### 📥 Final Predictions (`submission.csv`)")
    st.markdown("Predictions in the required format.")
    if os.path.exists("submission.csv"):
        df_sub = pd.read_csv("submission.csv")
        st.dataframe(df_sub, use_container_width=True, hide_index=True)
        
        with open("submission.csv", "rb") as file:
            st.download_button(
                label="Download submission.csv",
                data=file,
                file_name="submission.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.warning("`submission.csv` not found.")
