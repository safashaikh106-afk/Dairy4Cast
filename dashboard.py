import streamlit as st
import pandas as pd
from supabase_client import supabase   # ✅ Supabase connection

def dashboard_page():

    st.markdown("## 📤 Upload Sales Data")
    st.caption("Upload a CSV file containing your dairy sales data")

    # 🎨 UI Styling (your original design)
    st.markdown("""
    <style>
    .upload-wrapper {
        border: 2px dashed #cfd8e3;
        border-radius: 14px;
        padding: 70px;
        text-align: center;
        background: #ffffff;
        margin-bottom: 25px;
    }
    .upload-icon {
        width:60px;
        height:60px;
        border-radius:50%;
        background:#e9f2ff;
        display:flex;
        align-items:center;
        justify-content:center;
        margin:auto;
        font-size:28px;
        color:#2f80ed;
        margin-bottom:12px;
    }
    .upload-title {
        font-size:18px;
        font-weight:600;
        margin-bottom:4px;
    }
    .upload-sub {
        color:#6b7280;
        margin-bottom:15px;
    }
    .card {
        background: #f9fafb;
        padding: 22px;
        border-radius: 14px;
        border:1px solid #e5e7eb;
        margin-top:20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-wrapper">
        <div class="upload-icon">⬆</div>
        <div class="upload-title">Drag and drop your CSV file</div>
        <div class="upload-sub">or browse files</div>
    </div>
    """, unsafe_allow_html=True)

    # 📤 File Upload
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        required_cols = ["product", "location", "date", "quantity", "cost", "revenue"]
        missing = [c for c in required_cols if c not in df.columns]

        if missing:
            st.error(f"❌ Missing columns: {', '.join(missing)}")
            return

        st.session_state.uploaded_data = df

        st.success(f"✅ Loaded {len(df)} records")
        st.dataframe(df, use_container_width=True)


    # 📄 Info Card
    st.markdown("""
    <div class="card">
        <h4>Expected CSV Format</h4>
        <code>product, location, date, quantity, cost, revenue</code>
        <ul>
            <li><b>product</b>: Product name</li>
            <li><b>location</b>: Sales location</li>
            <li><b>date</b>: YYYY-MM-DD</li>
            <li><b>quantity</b>: Units sold</li>
            <li><b>cost</b>: Cost per unit</li>
            <li><b>revenue</b>: Total revenue</li>
        </ul>    
    </div>
    """, unsafe_allow_html=True)
