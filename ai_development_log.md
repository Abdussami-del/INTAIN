# AI Development Log

## 1. AI Tools & Environment

* **Code Generation & Architecture Planning:** Google Gemini (Chat Interface)
* **LLM Copilot / RAG Engine (Task 7):** Google Gemini 1.5 Flash (via `google-generativeai` API)
* **Environment:** Kaggle Notebooks (Python 3, Scikit-Learn, LightGBM, Lifelines, SHAP)
* **Approximate AI-Generated Code Share:** ~85% AI-generated boilerplate and pipeline logic, ~15% human debugging and architectural intervention.

## 2. Human Review & Governance Process

All AI-generated code and analytical outputs underwent strict human review to ensure compliance with the hackathon's "Benchmarking Lens". The review process focused on:

* **Leakage Prevention:** Manually enforcing the chronological 80th-percentile split over the AI's initial suggestion of `train_test_split`.
* **Placeholder Elimination:** Auditing the pipeline to ensure no `np.random` values or mock placeholders were used in the final `submission.csv`.
* **Copilot Governance:** Hardcoding a `[SYSTEM NOTE: Human decision required]` disclaimer into the LLM output pipeline and forcing `temperature=0.0` for maximum determinism.

## 3. Representative Prompts

**Prompt 1: Data Intelligence Pipeline (Task 1)**

> "Generate a Python script using pandas to profile a loan-level dataset. I need it to calculate missingness percentages, detect records where current_balance exceeds original_balance, and calculate a Kolmogorov-Smirnov (KS) test for train vs. test drift."

**Prompt 2: Survival Modeling (Task 3)**

> "Using the `lifelines` library, write a script to fit a Kaplan-Meier survival curve and a Cox Proportional Hazards model. The event is 12-month default. Show me how to extract the concordance index."

**Prompt 3: RAG Copilot (Task 7 - Application Code)**

> "You are an AI assistant for a loan reviewer. Base your response strictly on the data provided below. Do not invent information. [SYSTEM CONTEXT - DATA DICTIONARY]: {exception_type}: {retrieved_context}. Task: Write a concise, 2-sentence reviewer note summarizing why this loan was flagged based on the dictionary definition, and state what the human reviewer should verify."

## 4. Accepted and Rejected AI Outputs

### Rejected Output 1: RAG Context Parsing Failure (Vague / Literal Execution)

* **Scenario:** In early testing of Task 7, the Python text parser failed to extract the specific definition for `Document_Gap` from the markdown dictionary, feeding the LLM the text "Exception definition not found in dictionary."
* **AI Output:** *"Loan LOAN_002257 was flagged with a Document_Gap because the exception definition was not found in the dictionary. The human reviewer should verify the missing required documentation associated with this anomaly driver."*
* **Reason for Rejection:** While the LLM perfectly followed the instruction to "not invent information" (zero hallucination), the response was useless for a reviewer.
* **Human Correction:** Wrote a deterministic Python fallback dictionary to ensure the LLM always receives context even if file parsing fails.

### Rejected Output 2: Mocking Target Variables

* **Scenario:** When asking the AI to assemble the final `submission.csv` format, it initially provided code that generated random floats for the required targets.
* **AI Output:** `df_test['probability_delinquency_3m'] = np.random.rand(len(df_test))`
* **Reason for Rejection:** The rubric strictly disqualifies solutions that fabricate results.
* **Human Correction:** Forced the implementation of an actual calibrated `HistGradientBoostingClassifier` to generate real inference probabilities.

### Accepted Output: Properly Grounded RAG Note

* **Scenario:** After fixing the RAG context parser and setting `temperature=0.0`.
* **AI Output:** *"Loan LOAN_004001 was flagged for a Document_Gap driven by Missing Required Documentation. As per the data dictionary, this occurs when required documentation is missing from the system of record. The reviewer must verify the loan file to secure the missing documentation."*
* **Reason for Acceptance:** Highly factual, directly incorporates the rules engine, and provides clear instructions to the human reviewer without hallucinating external loan details.

## 5. Key Lessons Learned

1. **RAG Brittleness:** The LLM is only as good as the context injected into it. If the markdown parser fails, a low-temperature LLM will blindly adopt the error. Fallback dictionaries are essential for production resilience.
2. **SHAP Compatibility:** AI-generated suggestions for SHAP explanations often assume `TreeExplainer` works perfectly with all ensemble models. However, `HistGradientBoostingClassifier` caused environment crashes, necessitating a human pivot to a `RandomForestClassifier` surrogate.
3. **Prompt Engineering vs. Data Engineering:** Complex logical routing (like hybrid anomaly scoring) is much safer and cheaper to execute in deterministic Python (Scikit-Learn/Isolation Forest) than attempting to prompt an LLM to evaluate raw numerical tables. The LLM is best reserved purely for the final semantic summarization layer.
