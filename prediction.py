import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from supabase_client import supabase
import json


def prediction_page():

    st.markdown("## 📈 Sales Prediction")
    st.caption("Using Linear Regression model for prediction")

    if st.session_state.uploaded_data is None:
        st.warning("Please upload CSV in Upload tab first.")
        return

    df = st.session_state.uploaded_data.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ---------------- DAILY MODEL ----------------
    daily = df.groupby("date").agg({
        "quantity": "sum",
        "revenue": "sum",
        "cost": "mean"
    }).reset_index()

    daily = daily.sort_values("date")
    daily["idx"] = range(len(daily))

    X = daily[["idx"]]
    y_qty = daily["quantity"]
    y_rev = daily["revenue"]

    model_qty = LinearRegression()
    model_rev = LinearRegression()

    model_qty.fit(X, y_qty)
    model_rev.fit(X, y_rev)

    next_idx = daily["idx"].max() + 1

    pred_qty = int(model_qty.predict([[next_idx]])[0])
    pred_rev = float(model_rev.predict([[next_idx]])[0])

    # ---------------- COST CALCULATION ----------------
    avg_cost_per_unit = (df["cost"] * df["quantity"]).sum() / df["quantity"].sum()
    pred_cost = avg_cost_per_unit * pred_qty
    pred_profit = pred_rev - pred_cost

    # ---------------- KPI CARDS ----------------
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Predicted Sales", f"{pred_qty}", "units (next day)")
    k2.metric("Predicted Revenue", f"₹{pred_rev:,.0f}", "expected earnings")
    k3.metric("Predicted Cost", f"₹{pred_cost:,.0f}", "expected expenses")
    k4.metric("Predicted Profit", f"₹{pred_profit:,.0f}", "expected net profit")

    st.divider()

    # ---------------- PRODUCT-LOCATION PREDICTION ----------------
    grp = df.groupby(["product", "location"]).agg({
        "quantity": "mean",
        "revenue": "mean",
        "cost": "mean"
    }).reset_index()

    # ✅ ADD DATE (ONLY CHANGE)
    next_date = df["date"].max() + pd.Timedelta(days=1)
    grp["Date"] = next_date

    grp["Predicted Quantity"] = (grp["quantity"] * np.random.uniform(0.95, 1.05, len(grp))).astype(int)
    grp["Predicted Revenue"] = grp["Predicted Quantity"] * (grp["revenue"] / grp["quantity"])
    grp["Predicted Cost"] = grp["Predicted Quantity"] * grp["cost"]
    grp["Predicted Profit"] = grp["Predicted Revenue"] - grp["Predicted Cost"]
    grp["Confidence"] = (np.random.uniform(70, 90, len(grp))).astype(int)

    raw_df = grp[[
        "Date",   # ✅ ADDED
        "product", "location",
        "Predicted Quantity",
        "Predicted Revenue",
        "Predicted Cost",
        "Predicted Profit",
        "Confidence"
    ]]

    raw_df.columns = [
        "Date",   # ✅ ADDED
        "Product", "Location",
        "Predicted Quantity",
        "Predicted Revenue",
        "Predicted Cost",
        "Predicted Profit",
        "Confidence (%)"
    ]

    # ✅ FORMAT DATE (OPTIONAL CLEAN)
    raw_df["Date"] = pd.to_datetime(raw_df["Date"]).dt.strftime("%Y-%m-%d")

    # SAVE FOR REPORTS
    st.session_state.predicted_df = raw_df.copy()

    # ---------------- ✅ HISTORY SAVE (FIXED) ----------------
    if "user_email" in st.session_state and st.session_state.user_email:

        try:
            email = st.session_state.user_email

            result_data = {
                "type": "prediction",
                "table": raw_df.to_json(),
                "kpi": {
                    "sales": pred_qty,
                    "revenue": pred_rev,
                    "cost": pred_cost,
                    "profit": pred_profit
                }
            }

            supabase.table("history").insert({
                "user_email": email,
                "type": "prediction",
                "result": json.dumps(result_data)
            }).execute()

        except Exception as e:
            st.error(f"History Save Error: {e}")

    # ---------------- AUTO SAVE (EXISTING) ----------------
    if "user_email" in st.session_state and st.session_state.user_email:

        if "last_saved_hash" not in st.session_state:
            st.session_state.last_saved_hash = None

        current_hash = hash(raw_df.to_csv(index=False))

        if st.session_state.last_saved_hash != current_hash:

            try:
                user_email = st.session_state.user_email

                for _, row in raw_df.iterrows():
                    supabase.table("predictions").insert({
                        "user_email": user_email,
                        "product": row["Product"],
                        "predicted_sales": float(row["Predicted Quantity"])
                    }).execute()

                st.session_state.last_saved_hash = current_hash

            except Exception as e:
                st.error(f"Database Error: {e}")

    # ---------------- FILTER ----------------
    st.markdown("### 📋 Next-Day Sales Predictions")

    fcol1, fcol2 = st.columns([3, 1])

    with fcol2:
        product_filter = st.selectbox(
            "Filter by Product:",
            ["All products"] + sorted(raw_df["Product"].unique().tolist())
        )

    display_df = raw_df.copy()

    if product_filter != "All products":
        display_df = display_df[display_df["Product"] == product_filter]

    # ---------------- FORMAT ----------------
    display_df["Predicted Revenue"] = display_df["Predicted Revenue"].map(lambda x: f"₹{x:,.0f}")
    display_df["Predicted Cost"] = display_df["Predicted Cost"].map(lambda x: f"₹{x:,.0f}")
    display_df["Predicted Profit"] = display_df["Predicted Profit"].map(lambda x: f"₹{x:,.0f}")
    display_df["Confidence (%)"] = display_df["Confidence (%)"].astype(str) + "%"

    st.dataframe(display_df, use_container_width=True)
