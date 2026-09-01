import streamlit as st
import pandas as pd
import os
import time

# 1. Setup page configuration
st.set_page_config(page_title="Loan Performance AI", page_icon="🏦", layout="centered", initial_sidebar_state="collapsed")

# 2. Modern UI CSS (Targeting the exact Aaabadcode layout)
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
        margin-top: 1rem;
        font-weight: 500;
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
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
    
    /* Floating Cards Tabs (Exact visual match) */
    div[data-testid="stTabs"] {
        margin-top: 2rem;
    }
    
    /* Space out the tabs */
    div[data-baseweb="tab-list"], div[data-testid="stTabs"] > div > div > div {
        gap: 15px !important;
        justify-content: center !important;
        border-bottom: none !important;
        padding-bottom: 2rem !important;
    }

    /* Style the buttons to be floating white boxes */
    button[data-baseweb="tab"], div[data-testid="stTabs"] button {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        height: 100px !important;
        width: 125px !important;
        padding: 15px 5px !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Hover effect */
    button[data-baseweb="tab"]:hover, div[data-testid="stTabs"] button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid #CBD5E0 !important;
    }

    /* Selected Tab state - minimal border like the reference */
    button[data-baseweb="tab"][aria-selected="true"], div[data-testid="stTabs"] button[aria-selected="true"] {
        border: 1.5px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Force text to stack nicely and mimic the icon-over-text layout */
    button[data-baseweb="tab"] p, div[data-testid="stTabs"] button p {
        font-size: 0.90rem !important;
        font-weight: 600 !important;
        color: #4A5568 !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 8px !important;
        line-height: 1.2 !important;
        white-space: pre-wrap !important;
    }
    
    /* Hide the default bottom line on tabs */
    div[data-baseweb="tab-highlight"], div[data-testid="stTabs"] > div > div > div > div {
        display: none !important;
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

def generate_mock_llm_response(query):
    prompt = query.lower()
    if "anomaly" in prompt or "anomalies" in prompt:
        return "Based on the Isolation Forest model, I've detected a significant number of data-mismatch anomalies where the current balance exceeds the original balance, which violates standard validation rules."
    elif "default" in prompt or "risk" in prompt:
        return "Our HistGradientBoosting model currently projects a spike in default probability if unemployment rises by 3.5% in our Adverse Credit stress scenario."
    elif "shap" in prompt or "explain" in prompt:
        return "According to the SHAP analysis, credit score band and remaining term are the strongest global predictors of default in the current portfolio."
    else:
        return "I am the Loan Intelligence Engine's AI Copilot. I analyze the portfolio for defaults, prepayments, and anomalies. I can query our SHAP explanations or summarize the latest stress-test scenarios for you! What would you like to explore?"

# 5. ChatGPT-like Interactive Chat Input
if "messages" not in st.session_state:
    st.session_state.messages = []

# The pill-shaped input box
user_query = st.chat_input("Ask me anything about the loan portfolio...")

# Display chat history if active
if len(st.session_state.messages) > 0:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"]=="assistant" else "👤"):
            st.markdown(msg["content"])

# Process new query with streaming effect
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)
        
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        mock_reply = generate_mock_llm_response(user_query)
        for chunk in mock_reply.split(" "):
            full_response += chunk + " "
            time.sleep(0.05) 
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
st.divider()

# 6. Centralized Navigation (Mapped to the Hackathon Reports)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋\nModel Card", 
    "🧠\nExplain", 
    "📉\nScenarios", 
    "🚨\nAnomalies", 
    "📊\nData Intel"
])

# --- TAB 1: MODEL CARD ---
with tab1:
    st.markdown("### 📋 Project Details (Model Card)")
    st.markdown("Objective, data, features, model type, validation method, metrics, limitations, leakage controls, and known failure modes.")
    st.markdown(load_md("model_card.md"))
    
    st.divider()
    st.markdown("### 📥 Final Predictions (`submission.csv`)")
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

# --- TAB 2: EXPLAINABILITY ---
with tab2:
    st.markdown("### 🧠 Explainability Report")
    st.markdown("Global feature importance, local examples, false positives, false negatives, and model uncertainty.")
    st.markdown(load_md("reports/explainability_report.md"))
    st.divider()
    display_image("reports/task6_global_shap_summary.png", "Global Feature Importance")
    st.divider()
    display_image("reports/task6_local_shap_waterfall.png", "Local Explanation (Waterfall)")
    st.divider()
    display_image("reports/task3_kaplan_meier_baseline.png", "Time-to-Event (Kaplan-Meier Baseline)")

# --- TAB 3: SCENARIOS ---
with tab3:
    st.markdown("### 📉 Scenario Simulator")
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

# --- TAB 4: ANOMALIES ---
with tab4:
    st.markdown("### 🚨 Reviewer-Ready Anomalies")
    st.markdown("Records flagged for immediate human review based on hybrid scoring.")
    if os.path.exists("reviewer_ready_anomalies.csv"):
        df_anomalies = pd.read_csv("reviewer_ready_anomalies.csv")
        if 'hybrid_risk_score' in df_anomalies.columns:
            df_anomalies['hybrid_risk_score'] = df_anomalies['hybrid_risk_score'].round(4)
        st.dataframe(df_anomalies, use_container_width=True, hide_index=True)

# --- TAB 5: DATA INTEL ---
with tab5:
    st.markdown("### 📊 Data Intelligence Report")
    st.markdown("Profiling, missingness, outliers, drift, and relationship checks.")
    st.markdown(load_md("reports/data_intelligence_report.md"))
