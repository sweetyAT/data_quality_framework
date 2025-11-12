# ------------ STREAMLIT APP (WORKING VERSION) ------------
# This version works on Windows, Streamlit, and your folder structure.

import sys
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Fix Python import path so we can import modules in the same folder
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Now safe to import local modules
from validator import validate
from notifier import alert_if_needed

# ---------------- UI -------------------

st.title("Data Quality & Validation Framework")

st.write("Upload a CSV file or use the default sample_data.csv located in /data.")

# File upload option
uploaded = st.file_uploader("Upload CSV file", type=["csv"])

# Where to read data from
if uploaded:
    # Save uploaded file
    uploaded_path = os.path.join(os.path.dirname(CURRENT_DIR), "data", "uploaded_tmp.csv")
    with open(uploaded_path, "wb") as f:
        f.write(uploaded.getbuffer())
    data_path = uploaded_path
else:
    # Default sample file
    data_path = os.path.join(os.path.dirname(CURRENT_DIR), "data", "sample_data.csv")
    st.info("Using default /data/sample_data.csv")

# Validation parameters
st.subheader("Validation Settings")
null_thresh = st.slider("Null threshold (%)", 0.0, 0.5, 0.05, step=0.01)
z_thresh = st.slider("Outlier Z-score threshold", 1.0, 5.0, 3.0, step=0.5)

# Expected schema for your sample data
expected_schema = {
    "id": "int",
    "user_id": "int",
    "price": "float",
    "quantity": "int",
    "country": "object",
    "order_date": "object"
}

# Run validation
if st.button("Run Validation"):
    summary = validate(data_path, expected_schema, null_thresh, z_thresh)

    st.subheader("Validation Summary")
    st.json(summary)

    st.subheader("Outliers")
    outlier_df = pd.DataFrame.from_dict(
        summary["outliers"]["outliers_count"],
        orient="index",
        columns=["count"]
    )
    st.table(outlier_df)

    # Optional Alerts
    send_alert = st.checkbox("Send Slack / Email Alerts if problems found")
    if send_alert:
        alert_if_needed(summary)

    st.success("Validation Completed!")
