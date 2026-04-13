import streamlit as st
from auth import login_page, signup_page
from dashboard import dashboard_page
from prediction import prediction_page
from analysis import analysis_page
from reports_page import send_report_ui

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Dairy Analytics", layout="wide")

# ---------------- PROFESSIONAL THEME ----------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F6F9FC;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Buttons */
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #1E40AF;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
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


# ---------------- HANDLE GOOGLE CALLBACK ----------------
params = st.query_params

if params.get("code") and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.user_email = "Google User"
    st.query_params.clear()
    st.rerun()


# ---------------- TOP NAV BAR ----------------
st.markdown("""
<div style="
position:fixed;
top:0;
left:0;
right:0;
height:60px;
background:white;
display:flex;
align-items:center;
padding:0 30px;
box-shadow:0 2px 8px rgba(0,0,0,.1);
z-index:1000">
<h3>🥛 Dairy Analytics Dashboard</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding-top:80px'></div>", unsafe_allow_html=True)


# ---------------- HEADER BANNER ----------------
st.markdown("""
<div style="
background:linear-gradient(90deg,#2563EB,#1E3A8A);
padding:20px;
border-radius:12px;
color:white;
text-align:center;
margin-bottom:20px;
">
<h2>Dairy Sales Analytics & Prediction System</h2>
<p>Analyze sales trends, generate insights and predict future dairy product sales</p>
</div>
""", unsafe_allow_html=True)


# ---------------- APP FLOW ----------------
menu = ["Login", "Signup"]

if not st.session_state.logged_in:

    st.sidebar.title("🥛 Dairy Analytics")
    st.sidebar.caption("Sales Prediction Dashboard")
    st.sidebar.divider()

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_page()
    else:
        signup_page()

else:

    st.sidebar.title("🥛 Dairy Analytics")
    st.sidebar.caption("Smart Sales Dashboard")
    st.sidebar.divider()

    st.sidebar.success(f"Logged in as {st.session_state.get('user_email','User')}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.query_params.clear()
        st.rerun()

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["⬆ Upload Data", "📊 Data Analysis", "📈 Sales Prediction", "📨 Reports"]
    )

    with tab1:
        dashboard_page()

    with tab2:
        analysis_page()

    with tab3:
        prediction_page()

    with tab4:
        send_report_ui()
