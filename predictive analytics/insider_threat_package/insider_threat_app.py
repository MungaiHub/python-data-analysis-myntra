
import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(layout="centered", page_title="Insider Threat Predictor Demo")

st.title("Insider Threat Predictor (Demo)")
st.write("Upload a CSV with the same columns as the synthetic dataset, or use the included sample.")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is None:
    st.info("Using included sample dataset (synthetic).")
    df = pd.read_csv("insider_threat_demo/synthetic_user_behaviour.csv")
else:
    df = pd.read_csv(uploaded)

st.write("Sample rows:")
st.dataframe(df.head())

rf = joblib.load("insider_threat_demo/rf_model.joblib")
lr = joblib.load("insider_threat_demo/lr_model.joblib")
scaler = joblib.load("insider_threat_demo/scaler.joblib")

features = [
    "avg_login_hour","failed_logins_per_day","files_accessed_diff","sensitive_file_accesses",
    "vpn_use_ratio","privileged_cmds_count","avg_session_minutes","unusual_location_flag"
]

if not set(features).issubset(df.columns):
    st.error("Uploaded CSV is missing required columns: " + ", ".join(features))
else:
    X = df[features]
    X_scaled = scaler.transform(X)

    df["rf_risk_score"] = rf.predict_proba(X)[:,1].round(3)
    df["lr_risk_score"] = lr.predict_proba(X_scaled)[:,1].round(3)

    st.write("Predicted risk scores:")
    st.dataframe(df[["rf_risk_score","lr_risk_score"]].head(20))

    threshold = st.slider("RF threshold", 0.0, 1.0, 0.5)
    df["rf_flag"] = (df["rf_risk_score"] >= threshold).astype(int)

    st.write(f"Flagged accounts: {df['rf_flag'].sum()}")
    st.dataframe(df[df["rf_flag"]==1])
