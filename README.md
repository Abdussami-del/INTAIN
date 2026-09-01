# Loan Performance Intelligence Engine 🚀

**Intain Campus FinTech Challenge 2026 - AI Track**

This repository contains the complete end-to-end Machine Learning pipeline and required deliverables for the Loan Performance Intelligence Engine challenge. The project focuses on data intelligence, time-aware multi-outcome loan prediction, survival modeling, scenario simulation, and a robust LLM-assisted reviewer copilot.

🔗 **[View the Live Kaggle Notebook](https://www.kaggle.com/code/abdussaminalbund/notebooked6f9f2ed6)**
🔗 **[View the dashoard(synthetic dataset)](https://intain-aazadx2egpuzkjm9te8ofg.streamlit.app/)**


---

## 📁 Repository Structure

### Core Deliverables
- `loan_performance_engine.ipynb`: The main reproducible Jupyter Notebook containing the full pipeline.
- `model_card.md`: Professional Model Card documenting the architecture, validation strategies, metrics, and limitations.
- `ai_development_log.md`: Detailed log of AI tools utilized, governance, rejected outputs, and prompt strategies.
- `submission.csv`: Final predictions containing delinquency/default probabilities, next state, anomaly drivers, and reviewer actions.

### Generated Reports & Assets
- **`reports/`**
  - `data_intelligence_report.md`: Data profiling, missingness, and train/test drift (KS test) analysis.
  - `explainability_report.md`: Error analysis, model confidence, and false-positive/negative breakdown.
  - `task3_kaplan_meier_baseline.png`: Survival curve visualization for time-to-default.
  - `task6_global_shap_summary.png`: Global SHAP feature importance.
  - `task6_local_shap_waterfall.png`: Local SHAP explanation for a specific flagged loan.
- **Root CSV Outputs:**
  - `reviewer_ready_anomalies.csv`: Top 25 anomaly examples with ML risk scores and deterministic policy exceptions.
  - `scenario_report.csv`: Stress-tested portfolio projections under Base, Adverse-Credit, and High-Prepayment scenarios.
  - `llm_prompt_logs_rag.csv`: Traceability log for the LLM Reviewer Copilot, capturing prompts, temperatures, and generated notes.

---

## ⚙️ How to Run the Pipeline

The codebase is self-contained and originally executed on Kaggle Notebooks. 

### 1. Data Generation vs. Ingestion
* **Cell 1** dynamically simulates the `111,028` train and `27,226` test records, saving them to the `data/` directory along with `data_dictionary.md` and `validation_rules.json`.
* *Note for Judges:* If you intend to run this notebook on an official, pre-supplied hidden dataset, simply upload those files to the `data/` folder and **skip running Cell 1**. The rest of the pipeline flexibly ingests whatever data is present in that folder.

### 2. Time-Aware Validation
The pipeline avoids random row-level splitting (`train_test_split`). Instead, it executes a strict **chronological time-aware split** at the 80th percentile of the `reporting_month` to guarantee zero target leakage from future macroeconomic conditions.

---

## 🤖 LLM Reviewer Copilot & RAG Engine

Task 7 of the pipeline integrates a **Grounded LLM Reviewer Copilot** designed to map anomalies to the official data dictionary and generate human-readable review notes without hallucination.

### API Integration
* **Model:** Google Gemini 3.6 Flash (via `google-generativeai`).
* **Settings:** `temperature = 0.0` to force maximum determinism.
* **Authentication:** The pipeline utilizes `kaggle_secrets` to securely fetch the `GEMINI_API_KEY`. 

### Running Locally
If you are running this outside of Kaggle, you will need to authenticate the Gemini API differently. Replace the Kaggle Secrets block with a local environment variable:
```python
import os
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
```

### Deterministic Offline Fallback
To ensure the pipeline is robust and does not crash if API keys are missing or rate-limited, the system includes a **Deterministic Fallback Mechanism**. If the `GEMINI_API_KEY` is not found, the system catches the exception and falls back to a rules-based string concatenation engine that mimics the LLM's structure based on the RAG context.

All LLM outputs are explicitly flagged with `[SYSTEM NOTE: Human decision required]` to enforce human-in-the-loop AI governance.
