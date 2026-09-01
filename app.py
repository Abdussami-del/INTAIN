import streamlit as st
import pandas as pd
import os

# 1. Setup page configuration (must be first)
st.set_page_config(page_title="Loan Performance AI", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom CSS for a modern, sleek "interactive portfolio" aesthetic
st.markdown("""
    <style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Title Gradient */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #A0AEC0;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    /* Custom Tabs Styling to look like a modern navigation bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        font-size: 1.1rem;
        font-weight: 600;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom: 3px solid #FF416C;
        color: #FF416C !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Hero Section
st.markdown('<div class="hero-title">Loan Performance Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Interactive ML forecasting, anomaly detection, and an AI-powered Copilot.</div>', unsafe_allow_html=True)

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

# 5. Centralized Navigation (Replaces Sidebar)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 AI Copilot", 
    "📈 Stress Scenarios", 
    "🚨 Anomalies", 
    "🧠 Explainability", 
    "📋 Model Card"
])

# --- TAB 1: AI COPILOT ---
with tab1:
    st.markdown("### 👋 Hey, I'm the AI Reviewer Copilot")
    st.markdown("I analyze policy exceptions and provide **zero-hallucination explanations** based on the official data dictionary.")
    
    if os.path.exists("llm_prompt_logs_rag.csv"):
        df_logs = pd.read_csv("llm_prompt_logs_rag.csv")
        for idx, row in df_logs.iterrows():
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**Automated Decision:**")
                st.info(row['output'])
                with st.expander("🔍 View Traceability & RAG Prompt"):
                    st.text(row['prompt'])
    else:
        st.warning("`llm_prompt_logs_rag.csv` not found.")

# --- TAB 2: MACRO SCENARIOS ---
with tab2:
    st.markdown("### 📉 Macro Scenario Simulator")
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
    st.markdown("### 📊 Data Intelligence & Drift")
    st.markdown(load_md("reports/data_intelligence_report.md"))
    
    st.divider()
    st.subheader("🚨 Reviewer-Ready Anomalies")
    if os.path.exists("reviewer_ready_anomalies.csv"):
        df_anomalies = pd.read_csv("reviewer_ready_anomalies.csv")
        if 'hybrid_risk_score' in df_anomalies.columns:
            df_anomalies['hybrid_risk_score'] = df_anomalies['hybrid_risk_score'].round(4)
        st.dataframe(df_anomalies, use_container_width=True, hide_index=True)

# --- TAB 4: EXPLAINABILITY ---
with tab4:
    st.markdown("### 🧠 Responsible AI & SHAP Explainability")
    st.markdown(load_md("reports/explainability_report.md"))
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Global Feature Importance**")
        display_image("reports/task6_global_shap_summary.png")
    with col2:
        st.markdown("**Local Explanation (Waterfall)**")
        display_image("reports/task6_local_shap_waterfall.png")
        
    st.divider()
    st.markdown("### ⏳ Survival Modeling (Time-to-Default)")
    display_image("reports/task3_kaplan_meier_baseline.png")

# --- TAB 5: MODEL CARD ---
with tab5:
    st.markdown("### 📋 Production Model Card")
    st.markdown(load_md("model_card.md"))
