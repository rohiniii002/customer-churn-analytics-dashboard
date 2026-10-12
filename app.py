import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Customer Churn Dashboard", page_icon="📊", layout="wide")
st.title("📊 Customer Churn & Customer Intelligence")
st.caption("Portfolio dashboard | Python • pandas • NumPy • SQL-derived dataset")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "cleaned_customer_churn.csv"
if not DATA_PATH.exists():
    st.error("Cleaned dataset not found. Keep the output folder beside app.py.")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["is_churned"] = df["is_churned"].astype(str).str.lower().isin(["true", "1", "yes"])
for col in ["monthly_charges", "cltv", "churn_score", "tenure_days", "complaint_count", "escalation_count", "avg_csat_score", "revenue_at_risk"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

st.sidebar.header("Filters")
plans = sorted(df["plan_type"].dropna().astype(str).unique()) if "plan_type" in df else []
selected_plans = st.sidebar.multiselect("Plan type", plans, default=plans)
contracts = sorted(df["contract_type"].dropna().astype(str).unique()) if "contract_type" in df else []
selected_contracts = st.sidebar.multiselect("Contract type", contracts, default=contracts)
states = sorted(df["state"].dropna().astype(str).unique()) if "state" in df else []
selected_states = st.sidebar.multiselect("State", states, default=states)
filtered = df.copy()
if "plan_type" in filtered: filtered = filtered[filtered["plan_type"].astype(str).isin(selected_plans)]
if "contract_type" in filtered: filtered = filtered[filtered["contract_type"].astype(str).isin(selected_contracts)]
if "state" in filtered: filtered = filtered[filtered["state"].astype(str).isin(selected_states)]

n = len(filtered)
churned = int(filtered["is_churned"].sum()) if n else 0
churn_rate = 100 * churned / n if n else 0
retention_rate = 100 - churn_rate
active = filtered[~filtered["is_churned"]]
avg_tenure = filtered["tenure_days"].dropna().mean()
complaints = int((filtered.get("complaint_count", pd.Series(0,index=filtered.index)).fillna(0) > 0).sum())
escalations = int((filtered.get("escalation_count", pd.Series(0,index=filtered.index)).fillna(0) > 0).sum())
revenue_at_risk = filtered.get("revenue_at_risk", pd.Series(0,index=filtered.index)).fillna(0).sum()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Customers", f"{n:,}")
c2.metric("Churned", f"{churned:,}")
c3.metric("Churn rate", f"{churn_rate:.2f}%")
c4.metric("Retention rate", f"{retention_rate:.2f}%")
c5.metric("Avg tenure", f"{avg_tenure:,.0f} days" if pd.notna(avg_tenure) else "N/A")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Churn status")
    status = pd.DataFrame({"Status":["Retained / active","Churned"],"Customers":[n-churned,churned]})
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=status, x="Status", y="Customers", hue="Status", legend=False, ax=ax)
    ax.set_xlabel(""); ax.set_ylabel("Customers")
    st.pyplot(fig); plt.close(fig)
with right:
    st.subheader("Churn rate by contract")
    if n and "contract_type" in filtered:
        by_contract = filtered.groupby("contract_type", dropna=False)["is_churned"].mean().mul(100).reset_index(name="Churn rate (%)")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(data=by_contract, x="contract_type", y="Churn rate (%)", hue="contract_type", legend=False, ax=ax)
        ax.set_xlabel("Contract type"); ax.tick_params(axis="x", rotation=15)
        st.pyplot(fig); plt.close(fig)
    else: st.info("No rows match the selected filters.")

left, right = st.columns(2)
with left:
    st.subheader("Churn rate by plan")
    if n and "plan_type" in filtered:
        by_plan = filtered.groupby("plan_type", dropna=False)["is_churned"].mean().mul(100).reset_index(name="Churn rate (%)")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(data=by_plan, x="plan_type", y="Churn rate (%)", hue="plan_type", legend=False, ax=ax)
        ax.set_xlabel("Plan type"); ax.tick_params(axis="x", rotation=15)
        st.pyplot(fig); plt.close(fig)
    else: st.info("No rows match the selected filters.")
with right:
    st.subheader("Cancellation reasons")
    churn_rows = filtered[filtered["is_churned"]]
    if len(churn_rows) and "cancellation_reason" in churn_rows:
        reason = churn_rows["cancellation_reason"].fillna("Not recorded").value_counts().rename_axis("Reason").reset_index(name="Customers")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(data=reason, y="Reason", x="Customers", hue="Reason", legend=False, ax=ax)
        st.pyplot(fig); plt.close(fig)
    else: st.info("No churned customers in this filtered selection.")

st.subheader("Support and risk")
a,b,c = st.columns(3)
a.metric("Customers with complaints", complaints)
b.metric("Customers with escalations", escalations)
c.metric("Active monthly charges at risk", f"{revenue_at_risk:,.2f}")
st.caption("Revenue-at-risk uses the project's current rule: active customers with churn_score > 70. A zero result is reported as-is, not replaced with an estimate.")

st.subheader("Customer detail")
cols = [c for c in ["customerid","state","plan_type","contract_type","monthly_charges","is_churned","cancellation_reason","churn_score","risk_tier","complaint_count","escalation_count","avg_csat_score"] if c in filtered.columns]
st.dataframe(filtered[cols], use_container_width=True, hide_index=True)
st.download_button("Download filtered customer data (CSV)", filtered.to_csv(index=False).encode("utf-8"), "filtered_customer_churn.csv", "text/csv")

with st.expander("How to interpret this dashboard"):
    st.write("- Churn means a non-null cancellation date in the source data.")
    st.write("- Churn rate = churned customers / customers in the current filter selection.")
    st.write("- Use the sidebar to compare plans, contracts, and states.")
    st.write("- This dataset is small, so use results as portfolio analysis, not as statistically conclusive business evidence.")
