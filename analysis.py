import streamlit as st
import pandas as pd
import plotly.express as px
from supabase_client import supabase   # ✅ ADDED
import json   # ✅ ADDED


def analysis_page():

    st.markdown("## 📊 Sales Dashboard")

    # ---------- CHECK DATA ----------
    if st.session_state.uploaded_data is None:
        st.info("📂 Please upload CSV first from Upload Data section.")
        return

    df = st.session_state.uploaded_data.copy()

    # ---------- REQUIRED COLUMNS CHECK ----------
    required_cols = ["date", "product", "quantity", "revenue", "cost", "location"]

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing columns: {', '.join(missing_cols)}")
        st.stop()

    # ---------- CLEANING ----------
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ---------- KPIs ----------
    total_qty = df["quantity"].sum()
    total_revenue = df["revenue"].sum()
    total_cost = df["cost"].sum()
    profit = total_revenue - total_cost

    best_product = df.groupby("product")["quantity"].sum().idxmax()
    top_city = df.groupby("location")["revenue"].sum().idxmax()
    best_day = df.groupby(df["date"].dt.day_name())["revenue"].sum().idxmax()

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
    k2.metric("📈 Profit", f"₹{profit:,.0f}")
    k3.metric("📦 Quantity", f"{total_qty:,}")
    k4.metric("🏆 Product", best_product)
    k5.metric("📍 City", top_city)
    k6.metric("📅 Best Day", best_day)

    st.divider()

    # ---------- PRODUCT PERFORMANCE ----------
    prod = df.groupby("product")["quantity"].sum().reset_index()

    fig_prod = px.pie(
        prod,
        names="product",
        values="quantity",
        hole=0.45,
        title="Product Distribution",
        template="plotly"
    )

    # ---------- SALES BY CITY ----------
    city = df.groupby("location")["revenue"].sum().reset_index()

    fig_city = px.pie(
        city,
        names="location",
        values="revenue",
        title="Revenue by City",
        template="plotly"
    )

    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.plotly_chart(fig_prod, use_container_width=True)

    with r1c2:
        st.plotly_chart(fig_city, use_container_width=True)

    st.divider()

    # ---------- BEST SELLING DAY ----------
    df["day_name"] = df["date"].dt.day_name()

    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    day_sales = (
        df.groupby("day_name")["revenue"]
        .sum()
        .reindex(order)
        .reset_index()
    )

    fig_trend = px.bar(
        day_sales,
        x="day_name",
        y="revenue",
        title="Sales by Day",
        template="plotly"
    )

    # ---------- PROFIT BY PRODUCT ----------
    profit_df = df.groupby("product").sum(numeric_only=True).reset_index()
    profit_df["profit"] = profit_df["revenue"] - profit_df["cost"]
    profit_df = profit_df[profit_df["profit"] > 0]

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.plotly_chart(fig_trend, use_container_width=True)

    with r2c2:
        if profit_df.empty:
            st.info("No profit data available.")
        else:
            fig_profit = px.pie(
                profit_df,
                names="product",
                values="profit",
                hole=0.45,
                title="Profit Distribution",
                template="plotly"
            )
            st.plotly_chart(fig_profit, use_container_width=True)

    # ---------------- 🔥 HISTORY SAVE (FIXED ONLY THIS PART) ----------------
    if "user_email" in st.session_state and st.session_state.user_email:

        try:
            email = st.session_state.user_email

            result_data = {
                "type": "analysis",
                "data": df.to_json(),
                "kpi": {
                    "revenue": float(total_revenue),
                    "profit": float(profit),
                    "quantity": int(total_qty),
                    "best_product": best_product,
                    "top_city": top_city,
                    "best_day": best_day
                }
            }

            supabase.table("history").insert({
                "user_email": email,
                "type": "analysis",
                "result": json.dumps(result_data)
            }).execute()

        except Exception as e:
            st.error(f"History Save Error: {e}")
