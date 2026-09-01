import streamlit as st
import pandas as pd
import os
from PIL import Image

# Setup page configuration
st.set_page_config(page_title="Loan Performance Engine", page_icon="🏦", layout="wide")

st.title("🏦 Loan Performance Intelligence Engine")
st.markdown("Interactive dashboard for loan-data profiling, multi-outcome predictions, anomaly detection, and LLM Copilot review.")

# Sidebar navigation
st.sidebar.title("Navigation")
tabs = st.sidebar.radio("Go to:", [
    "📋 Model Card", 
    "📊 Data Intelligence & Anomalies", 
    "📉 Macro Scenarios",
    "🧠 Explainability & Survival", 
    "🤖 LLM Reviewer Copilot"
])

# Helper function to load markdown safely
def load_md(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"*File not found: {file_path}*"

# Helper function to load images safely
def display_image(file_path, caption=""):
    if os.path.exists(file_path):
        st.image(Image.open(file_path), caption=caption, use_column_width=True)
    else:
        st.warning(f"Image not found: {file_path}")

# ---------------------------------------------------------
# TAB 1: MODEL CARD
# ---------------------------------------------------------
if tabs == "📋 Model Card":
    st.header("📋 Model Card")
    st.markdown(load_md("model_card.md"))

# ---------------------------------------------------------
# TAB 2: DATA INTELLIGENCE & ANOMALIES
# ---------------------------------------------------------
elif tabs == "📊 Data Intelligence & Anomalies":
    st.header("📊 Data Intelligence & Profiling")
    
    # Split into columns to show markdown and table side-by-side
    st.markdown(load_md("reports/data_intelligence_report.md"))
    
    st.divider()
    st.subheader("🚨 Reviewer-Ready Anomalies")
    st.markdown("Below are the top hybrid-risk records requiring human review, identified via Isolation Forest and deterministic policy rules.")
    
    if os.path.exists("reviewer_ready_anomalies.csv"):
        df_anomalies = pd.read_csv("reviewer_ready_anomalies.csv")
        # Format the risk score for better display
        if 'hybrid_risk_score' in df_anomalies.columns:
            df_anomalies['hybrid_risk_score'] = df_anomalies['hybrid_risk_score'].round(4)
        
        st.dataframe(df_anomalies, use_container_width=True, hide_index=True)
    else:
        st.warning("`reviewer_ready_anomalies.csv` not found.")

# ---------------------------------------------------------
# TAB 3: MACRO SCENARIOS
# ---------------------------------------------------------
elif tabs == "📉 Macro Scenarios":
    st.header("📉 Scenario & Stress Simulation")
    st.markdown("Projections of default and prepayment probabilities under different macroeconomic conditions (Base, Adverse Credit, High Prepayment).")
    
    if os.path.exists("scenario_report.csv"):
        df_scenario = pd.read_csv("scenario_report.csv")
        
        # Display the raw data
        with st.expander("View Raw Scenario Data"):
            st.dataframe(df_scenario, use_container_width=True, hide_index=True)
        
        # Visualizations
        st.subheader("Visualization by State & Scenario")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Projected Default Probability**")
            pivot_def = df_scenario.pivot(index="state", columns="scenario", values="proj_default_prob")
            st.bar_chart(pivot_def)
            
        with col2:
            st.markdown("**Projected Prepayment Probability**")
            pivot_pre = df_scenario.pivot(index="state", columns="scenario", values="proj_prepay_prob")
            st.bar_chart(pivot_pre)
            
    else:
        st.warning("`scenario_report.csv` not found.")

# ---------------------------------------------------------
# TAB 4: EXPLAINABILITY & SURVIVAL
# ---------------------------------------------------------
elif tabs == "🧠 Explainability & Survival":
    st.header("🧠 Explainability & Responsible AI")
    st.markdown(load_md("reports/explainability_report.md"))
    
    st.divider()
    st.subheader("Model Drivers (SHAP)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Global Feature Importance**")
        display_image("reports/task6_global_shap_summary.png")
    with col2:
        st.markdown("**Local Explanation (Waterfall)**")
        display_image("reports/task6_local_shap_waterfall.png")
            
    st.divider()
    st.subheader("⏳ Time-to-Event (Survival) Baseline")
    display_image("reports/task3_kaplan_meier_baseline.png", "Kaplan-Meier Survival Curve for Time-to-Default")

# ---------------------------------------------------------
# TAB 5: LLM COPILOT
# ---------------------------------------------------------
elif tabs == "🤖 LLM Reviewer Copilot":
    st.header("🤖 LLM-Assisted Reviewer Copilot")
    st.markdown("Grounded natural-language analysis explaining anomalies using Retrieval-Augmented Generation (Zero Hallucination).")
    
    if os.path.exists("llm_prompt_logs_rag.csv"):
        df_logs = pd.read_csv("llm_prompt_logs_rag.csv")
        
        for idx, row in df_logs.iterrows():
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**Timestamp:** `{row['timestamp']}` | **Model:** `{row['model']}` | **Temperature:** `{row['temperature']}`")
                st.markdown("**Generated Reviewer Note:**")
                st.info(row['output'])
                
                with st.expander("🔍 View Traceability / Prompt Log"):
                    st.text(row['prompt'])
    else:
        st.warning("`llm_prompt_logs_rag.csv` not found.")
