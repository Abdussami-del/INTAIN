# Model Card: Loan Performance Intelligence Engine

**Date:** September 2026  
**Project:** Intain Campus FinTech Challenge 2026 (AI Track)  
**Role:** Lead Machine Learning Engineer & AI Ethicist  

---

## 1. Objective
The Loan Performance Intelligence Engine is an ML-first system designed to profile messy loan-level data and provide robust, multi-outcome performance forecasting. Its primary objectives are to:
* Predict multi-outcome loan trajectories (default, prepayment, delinquency, and next-state transitions).
* Detect systemic anomalies and data integrity exceptions.
* Run macroeconomic scenario simulations (base, adverse-credit, high-prepayment).
* Provide transparent, grounded LLM-assisted explanations to human reviewers without fabricating or hallucinating data.

## 2. Model Types and Architecture
The system employs a multi-tiered architecture, prioritizing deterministic ML for predictive tasks and reserving generative AI exclusively for semantic summarization.

| Component | Architecture / Algorithm | Purpose |
| :--- | :--- | :--- |
| **Primary Predictive Models** | `HistGradientBoostingClassifier` | Multi-class state transitions and binary default/prepayment forecasting. Features native missing-value handling. |
| **Calibration** | Isotonic Regression | Post-processing calibration of boosting outputs to ensure probabilities reflect true likelihoods. |
| **Time-to-Event (Survival)**| Kaplan-Meier & Cox Proportional Hazards (`lifelines`) | Baseline survival estimation and right-censored hazard modeling based on credit score bands. |
| **Anomaly Engine** | `IsolationForest` + Deterministic Rules | Blends unsupervised statistical outlier detection with deterministic policy checks (e.g., Validation Rules JSON) for a hybrid risk score. |
| **Explainability Surrogate** | `RandomForestClassifier` + `shap.TreeExplainer` | Generates global feature importance and local waterfall plots. Used as a stable surrogate to prevent environment degradation. |
| **Reviewer Copilot (LLM)** | Google Gemini 1.5 Flash (via RAG) | Configured at `temperature=0.0`. Ingests `data_dictionary.md` to map anomalies to definitions and generate human-readable review notes. |

## 3. Data Profile & Features
* **Dataset Type:** Synthetic longitudinal panel data simulating real-world mortgage performance.
* **Training Volume:** 111,028 historical monthly records.
* **Inference/Test Volume:** 27,226 unlabelled performance records.
* **Feature Engineering:** Includes cross-column relationship ratios (e.g., `balance_ratio`), temporal tracking (`loan_age_months`, `remaining_term_months`), and dynamically encoded categorical attributes (LTV bands, DTI bands, state, servicer). 

## 4. Leakage Controls & Validation Method
To prevent look-ahead bias and target leakage, the system strictly enforces a **chronological time-aware split**.

* **Validation Method:** The dataset was partitioned at the **80th percentile** of the unique `reporting_month` variable.
* **Leakage Prevention:** Absolutely no random row-level splitting (`train_test_split`) was utilized. This ensures that the same loan is not simultaneously represented in both the training and validation sets across different chronological states, and guarantees that future macroeconomic conditions do not bleed into the historical training environment.

## 5. Performance Metrics
Evaluated on the out-of-time validation split. The models demonstrate strong discrimination and well-calibrated probability scores.

| Target Variable | ROC-AUC | F1 Score | Brier Score Loss |
| :--- | :--- | :--- | :--- |
| **12-Month Default** | ~ 0.99 | ~ 0.82 | ~ 0.001 |
| **12-Month Prepayment** | ~ 0.84 | ~ 0.22 | ~ 0.040 |

*(Note: The lower F1 score for prepayment reflects the highly imbalanced and volatile nature of early payoffs compared to terminal defaults.)*

## 6. Limitations & Known Failure Modes
While highly performant on the baseline distribution, the engine exhibits specific bounds of competence:

* **Macroeconomic Shock Sensitivity:** Model confidence degrades heavily under extreme, out-of-time macroeconomic shocks. Because the primary models are trained on historical performance, adverse credit stress tests or severe rate shocks require manual scenario multipliers rather than relying purely on the baseline inference engine.
* **RAG Pipeline Brittleness:** The LLM Copilot's accuracy is highly sensitive to the formatting of the underlying `data_dictionary.md` file. If the markdown parser fails to extract the correct definition, the RAG context degrades. 
* **Mitigation Strategy:** To counteract parsing failures, the system implements a deterministic fallback dictionary to guarantee context delivery, ensuring the LLM maintains zero-hallucination compliance. Furthermore, all LLM outputs are hardcoded with a `[SYSTEM NOTE: Human decision required]` disclaimer to enforce human-in-the-loop governance.
