import streamlit as st
from auth import login_page, signup_page
from dashboard import dashboard_page
from prediction import prediction_page
from analysis import analysis_page
from reports_page import send_report_ui

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Dairy Analytics", layout="wide")

# ---------------- GLOBAL THEME ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

/* ---------- FONT ---------- */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
}

/* ---------- BACKGROUND ---------- */
.stApp {
    background-color: #F8FAFC;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: white;
    font-size: 18px;
}

/* Sidebar title */
section[data-testid="stSidebar"] h1 {
    font-size: 26px;
}

/* ---------- BUTTONS ---------- */
.stButton>button {
    background-color: #6366F1;
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    border: none;
    font-weight: 600;
    font-size: 18px;
}

.stButton>button:hover {
    background-color: #4F46E5;
}

/* ---------- METRIC CARDS ---------- */
div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

/* ---------- DATAFRAME ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    font-size: 17px;
}
            h1, h2, h3 {
    font-weight: 700 !important;
}

p {
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ---------------- GOOGLE CALLBACK ----------------
params = st.query_params

if params.get("code") and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.user_email = "Google User"
    st.query_params.clear()
    st.rerun()

# ---------------- HEADER ----------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#6366F1,#4F46E5);
padding:25px;
border-radius:16px;
color:white;
margin-bottom:25px;
">

<h2 style="margin-bottom:5px;font-size:30px">
🥛 Dairy Sales Analytics
</h2>

<p style="opacity:0.9;font-size:16px">
Analyze sales trends and predict future demand with smart insights.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- APP FLOW ----------------
menu = ["Login", "Signup"]

# ---------------- NOT LOGGED IN ----------------
if not st.session_state.logged_in:

    st.sidebar.title("🥛 Dairy Analytics")
    st.sidebar.caption("Sales Dashboard")
    st.sidebar.divider()

    choice = st.sidebar.radio("Menu", menu)

    if choice == "Login":
        login_page()
    else:
        signup_page()

# ---------------- LOGGED IN ----------------
else:

    # -------- SIDEBAR --------
    st.sidebar.title("🥛 Dairy Analytics")
    st.sidebar.caption("Smart Sales Dashboard")
    st.sidebar.divider()

    st.sidebar.success(f"👤 {st.session_state.get('user_email','User')}")

    st.sidebar.markdown("### Navigation")

    menu = [
        "📂 Upload Data",
        "📊 Analysis",
        "📈 Future Sales",
        "📨 Reports"
    ]

    choice = st.sidebar.radio("", menu)

    # -------- PAGE ROUTING --------
    if choice == "📂 Upload Data":
        dashboard_page()

    elif choice == "📊 Analysis":
        analysis_page()

    elif choice == "📈 Future Sales":
        prediction_page()

    elif choice == "📨 Reports":
        send_report_ui()

    # -------- LOGOUT (BOTTOM FEEL) --------
    st.sidebar.markdown("---")
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.query_params.clear()
        st.rerun()
