# Customer Churn Analysis and Customer Intelligence

Portfolio project using SQLite, SQL, Python, pandas, NumPy, Matplotlib, and Seaborn.

## What's included
- `data/customer_churn.db`: SQLite source database
- `data/customer_churn_data_raw.xlsx`: original raw workbook
- `notebooks/customer_churn_analysis_updated.ipynb`: corrected, executed notebook
- `output/`: cleaned customer-level data, KPI summaries, quality report, findings, and charts
- `sql_queries.sql`: SQL examples
- `reports/reference_report.pdf`: supplied reference report

## Run
Install requirements with `pip install -r requirements.txt`, then open the updated notebook in Jupyter. Keep the folder structure unchanged.

## Fixes made
- Converted escalation flags `Y`/`N` into numeric 1/0 before aggregation.
- Aggregated support interactions per customer before joining to subscriptions.
- Added assertions to prevent duplicate row multiplication.
- Added data-quality checks and standardized gender labels.
- Removed the fully empty pincode column from the analysis output and documented missing fields.
- Added quality report, KPI CSV/JSON, and analysis findings exports.

## Interpretation notes
The sample has 21 subscriptions and 9 support interactions. The 28.57% churn rate and 71.43% retention rate are descriptive for this small dataset. Zero active high-risk customers means no active customer exceeds the chosen score threshold (>70); do not claim positive revenue at risk from this sample. The notebook uses 2024-09-30 as the tenure snapshot date.


## Interactive dashboard (Streamlit)
From the project root, install dependencies and launch:
```bash
pip install -r requirements.txt
streamlit run app.py
```
The dashboard reads `output/cleaned_customer_churn.csv` and provides filters for plan, contract, and state, KPI cards, charts, customer details, and CSV export.
