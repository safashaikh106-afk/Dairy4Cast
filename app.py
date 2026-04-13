import streamlit as st
import requests
from auth import login_page, signup_page
from dashboard import dashboard_page
from prediction import prediction_page
from analysis import analysis_page
from reports_page import send_report_ui
from supabase_client import supabase
from history_page import history_page

# ---------------- GOOGLE CONFIG ----------------
CLIENT_ID = "204866650872-1jgkgim3fho887gh4qtkt4gsq6md83kt.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Dairy4Cast", layout="wide")

# ---------------- SIDEBAR COLOR ----------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #5f9cff, #6a5af9) !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GLOBAL THEME ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
}

.stApp {
    background-color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: transparent;
}

.stButton > button,
.stDownloadButton > button,
a.custom-btn {
    display: inline-block;
    text-align: center;
    text-decoration: none;
    background: linear-gradient(90deg, #6366F1, #4F46E5) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 18px !important;
    width: 100% !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
a.custom-btn:hover {
    background: linear-gradient(90deg, #4F46E5, #4338CA) !important;
    color: white !important;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

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

if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- GOOGLE CALLBACK (REAL LOGIN) ----------------
params = st.query_params

if params.get("code") and not st.session_state.logged_in:

    code = params.get("code")

    token_url = "https://oauth2.googleapis.com/token"

    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(token_url, data=token_data).json()
    access_token = token_response.get("access_token")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    st.session_state.logged_in = True
    st.session_state.user_email = user_info.get("email")
    st.session_state.username = user_info.get("name")

    # ✅ ADDED PART (FIXED POSITION)
    email = user_info.get("email")
    name = user_info.get("name")

    existing = supabase.table("users").select("*").eq("email", email).execute()

    if not existing.data:
        supabase.table("users").insert({
            "email": email,
        }).execute()

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
🥛 Dairy4Cast
</h2>

<p style="opacity:0.9;font-size:16px">
Analyze sales trends and predict future demand with smart insights.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- NOT LOGGED IN ----------------
if not st.session_state.logged_in:

    st.sidebar.title("🥛 Dairy4Cast")
    st.sidebar.caption("Where Dairy Meets Data")
    st.sidebar.divider()

    choice = st.sidebar.radio("Menu", ["Login", "Signup"])

    if choice == "Login":
        login_page()
    else:
        signup_page()

# ---------------- LOGGED IN ----------------
else:

    st.sidebar.title("🥛 Dairy4Cast")
    st.sidebar.caption("Where Dairy Meets Data")
    st.sidebar.divider()

    username = st.session_state.get("username")

    if not username and st.session_state.get("user_email"):
        username = st.session_state.user_email.split("@")[0]

    st.sidebar.markdown(f"""
    <div style="font-size:20px; font-weight:700;">
        👤 {username if username else "User"}
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### Navigation")

    choice = st.sidebar.radio("", [
        "📂 Upload Data",
        "📊 Analysis",
        "📈 Future Sales",
        "📜 History",
        "📨 Reports"
    ])

    if choice == "📂 Upload Data":
        dashboard_page()
    elif choice == "📊 Analysis":
        analysis_page()
    elif choice == "📈 Future Sales":
        prediction_page()
    elif choice == "📜 History":
        history_page()
    elif choice == "📨 Reports":
        send_report_ui()

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.username = None
        st.query_params.clear()
        st.rerun()
