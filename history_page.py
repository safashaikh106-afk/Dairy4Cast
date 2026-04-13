import streamlit as st
from supabase_client import supabase
import pandas as pd
import plotly.express as px
import json
from datetime import datetime, timedelta  # (kept as is)

def history_page():

    st.title("📜 History Dashboard")

    email = st.session_state.get("user_email")

    if not email:
        st.warning("User not logged in")
        return

    # ---------------- 🔽 DROPDOWN (EXISTING) ----------------
    filter_type = st.selectbox(
        "Filter History:",
        ["All", "Analysis", "Prediction"]
    )

    response = supabase.table("history") \
        .select("*") \
        .eq("user_email", email) \
        .order("created_at", desc=True) \
        .execute()

    data = response.data

    if not data:
        st.info("No history found")
        return

    # ---------------- 🔽 DATE DROPDOWN (FIRST COLUMN OF PREDICTION TABLE) ----------------
    dates = []

    for item in data:
        try:
            result = json.loads(item["result"])

            if result.get("type") == "prediction":
                df = pd.read_json(result["table"])

                # 👉 take FIRST column (your prediction date column)
                if df.shape[1] >= 1:
                    date_col = df.columns[0]
                    dates.extend(df[date_col].astype(str).unique().tolist())

        except:
            continue

    unique_dates = sorted(list(set(dates)), reverse=True)

    date_filter = st.selectbox(
        "Filter Prediction Date:",
        ["All"] + unique_dates
    )

    # ---------------- 🔽 APPLY TYPE FILTER (EXISTING) ----------------
    if filter_type != "All":
        filtered_data = []

        for item in data:
            try:
                result = json.loads(item["result"])
                if result.get("type", "").lower() == filter_type.lower():
                    filtered_data.append(item)
            except:
                continue

        data = filtered_data

    # ---------------- 🔽 APPLY DATE FILTER (FIRST COLUMN MATCH) ----------------
    if date_filter != "All":
        filtered_data = []

        for item in data:
            try:
                result = json.loads(item["result"])

                if result.get("type") == "prediction":
                    df = pd.read_json(result["table"])

                    if df.shape[1] >= 1:
                        date_col = df.columns[0]

                        if date_filter in df[date_col].astype(str).values:
                            filtered_data.append(item)

                else:
                    # keep analysis visible
                    filtered_data.append(item)

            except:
                continue

        data = filtered_data

    # ---------------- ORIGINAL LOOP (UNCHANGED) ----------------
    for item in data:

        st.markdown("---")
        st.subheader(f"🕒 {item['created_at']}")

        try:
            result = json.loads(item["result"])

            # ---------------- ANALYSIS ----------------
            if result.get("type") == "analysis":

                st.markdown("### 📊 Analysis Dashboard")

                df = pd.read_json(result["data"])
                kpi = result["kpi"]

                k1, k2, k3, k4, k5, k6 = st.columns(6)
                k1.metric("💰 Revenue", f"₹{kpi['revenue']:,.0f}")
                k2.metric("📈 Profit", f"₹{kpi['profit']:,.0f}")
                k3.metric("📦 Quantity", f"{kpi['quantity']:,}")
                k4.metric("🏆 Product", kpi["best_product"])
                k5.metric("📍 City", kpi["top_city"])
                k6.metric("📅 Best Day", kpi["best_day"])

                prod = df.groupby("product")["quantity"].sum().reset_index()
                fig1 = px.pie(prod, names="product", values="quantity", hole=0.4)

                city = df.groupby("location")["revenue"].sum().reset_index()
                fig2 = px.pie(city, names="location", values="revenue")

                c1, c2 = st.columns(2)
                c1.plotly_chart(fig1, use_container_width=True)
                c2.plotly_chart(fig2, use_container_width=True)

                df["day_name"] = pd.to_datetime(df["date"]).dt.day_name()

                order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

                day_sales = (
                    df.groupby("day_name")["revenue"]
                    .sum()
                    .reindex(order)
                    .reset_index()
                )

                fig3 = px.bar(day_sales, x="day_name", y="revenue")

                profit_df = df.groupby("product").sum(numeric_only=True).reset_index()
                profit_df["profit"] = profit_df["revenue"] - profit_df["cost"]
                profit_df = profit_df[profit_df["profit"] > 0]

                c3, c4 = st.columns(2)

                c3.plotly_chart(fig3, use_container_width=True)

                if profit_df.empty:
                    c4.info("No profit data available.")
                else:
                    fig4 = px.pie(profit_df, names="product", values="profit", hole=0.4)
                    c4.plotly_chart(fig4, use_container_width=True)

            # ---------------- PREDICTION ----------------
            elif result.get("type") == "prediction":

                st.markdown("### 📈 Prediction Result")

                df = pd.read_json(result["table"])
                kpi = result["kpi"]

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Sales", kpi["sales"])
                k2.metric("Revenue", f"₹{kpi['revenue']:,.0f}")
                k3.metric("Cost", f"₹{kpi['cost']:,.0f}")
                k4.metric("Profit", f"₹{kpi['profit']:,.0f}")

                st.dataframe(df, use_container_width=True)

            else:
                st.warning("⚠️ Old history format (cannot show dashboard)")

        except Exception as e:
            st.error(f"Error loading history: {e}")
