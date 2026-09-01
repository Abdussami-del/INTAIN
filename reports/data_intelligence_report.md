# Data Intelligence Report

## 1. Data Quality Overview
* **Average Record-Level Quality Score:** 0.9457
* **Records with Balance > Original:** 13693

## 2. Missingness Analysis
Top missing fields requiring imputation:
loss_severity_band    99.888316
exception_type        79.277299

## 3. Train vs. Test Distribution Drift
Evaluated using Kolmogorov-Smirnov (KS) statistic on `current_balance`.
* **KS Statistic:** 0.0195
* **P-Value:** 0.0000
* **Status:** Drift Detected

## 4. Top Feature Correlations
remaining_term_months  month_index           1.000000
                       loan_age_months       1.000000
loan_age_months        month_index           1.000000
dq_score               exception_required    0.996623
current_balance        original_balance      0.945008
