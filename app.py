import streamlit as st
import pandas as pd
import os

# 1. Setup page configuration
st.set_page_config(page_title="Loan Performance AI", page_icon="🏦", layout="centered", initial_sidebar_state="collapsed")

# 2. Custom CSS to exactly mimic the Aaabadcode portfolio layout
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
    
    /* Custom Tabs Styling to look like Floating Cards */
    .stTabs {
        margin-top: 3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        justify-content: center;
        border-bottom: none;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        height: 85px;
        width: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 5px;
        white-space: pre-wrap;
        font-size: 0.9rem;
        color: #4A5568;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .stTabs [aria-selected="true"] {
        border: 2px solid #3182CE;
        color: #3182CE !important;
        background-color: #FAFCFF;
        box-shadow: 0 10px 15px -3px rgba(31, 130, 206, 0.15);
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
    "🤖\nCopilot", 
    "📈\nScenarios", 
    "🚨\nAnomalies", 
    "🧠\nExplain", 
    "📋\nModel"
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
    st.markdown("### 📈 Scenario Projections")
    if os.path.exists("scenario_report.csv"):
        df_scenario = pd.read_csv("scenario_report.csv")
        st.dataframe(df_scenario, use_container_width=True, hide_index=True)
        st.divider()
        st.markdown("**Projected Default Probability**")
        st.bar_chart(df_scenario.pivot(index="state", columns="scenario", values="proj_default_prob"))
    else:
        st.warning("`scenario_report.csv` not found.")

# --- TAB 3: DATA & ANOMALIES ---
with tab3:
    st.markdown("### 🚨 Top Anomalies")
    if os.path.exists("reviewer_ready_anomalies.csv"):
        df_anomalies = pd.read_csv("reviewer_ready_anomalies.csv")
        if 'hybrid_risk_score' in df_anomalies.columns:
            df_anomalies['hybrid_risk_score'] = df_anomalies['hybrid_risk_score'].round(4)
        st.dataframe(df_anomalies, use_container_width=True, hide_index=True)
    st.divider()
    st.markdown("### 📊 Drift Profile")
    st.markdown(load_md("reports/data_intelligence_report.md"))

# --- TAB 4: EXPLAINABILITY ---
with tab4:
    st.markdown("### 🧠 Responsible AI Insights")
    st.markdown(load_md("reports/explainability_report.md"))
    st.divider()
    display_image("reports/task6_global_shap_summary.png", "Global Feature Importance")
    st.divider()
    display_image("reports/task6_local_shap_waterfall.png", "Local Explanation (Waterfall)")

# --- TAB 5: MODEL CARD ---
with tab5:
    st.markdown("### 📋 Production Model Card")
    st.markdown(load_md("model_card.md"))
