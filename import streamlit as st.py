import streamlit as st
import pandas as pd

def expiry_page():

    st.title("⚠️ Expiry Detection")

    if st.session_state.uploaded_data is None:
        st.warning("Please upload dataset first.")
        return

    df = st.session_state.uploaded_data.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Assume dairy expires in 5 days
    df["expiry_date"] = df["date"] + pd.Timedelta(days=5)

    today = pd.Timestamp.today()

    df["status"] = df["expiry_date"].apply(
        lambda x: "Expiring Soon ⚠️" if (x - today).days <= 2 else "Safe ✅"
    )

    result = df[["product", "expiry_date", "status"]]

    result.columns = ["Product", "Expiry Date", "Status"]

    st.dataframe(result, use_container_width=True)
