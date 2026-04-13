from database import conn, cursor
import streamlit as st
import urllib.parse
from supabase_client import supabase   # ✅ ADDED

# ---------------- GOOGLE CONFIG ----------------
CLIENT_ID = "204866650872-1jgkgim3fho887gh4qtkt4gsq6md83kt.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8501"
SCOPE = "openid email profile"

# ---------------- COMMON UI STYLE ----------------
def auth_ui():
    st.markdown("""
    <style>

    .block-container {
        padding-top: 1rem !important;
    }

    body {
        background-color: #f5f7fb;
        font-family: 'Poppins', sans-serif;
    }

    .banner {
        background: linear-gradient(135deg, #5f9cff, #6a5af9);
        color: white;
        padding: 12px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 900;
        margin-bottom: 12px;
        text-align: center;
    }

    .subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 16px;
        font-weight: 700;
        text-align: center;
    }

    .stTextInput > div > div > input {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        height: 38px !important;
        background-color: #fafafa !important;
    }

    .stTextInput > label {
        font-size: 14px !important;
        font-weight: 800 !important;
    }

    .stButton > button {
        height: 40px;
        font-size: 15px;
        font-weight: 800;
        border-radius: 8px;
        border: none;
        color: white;
        background: linear-gradient(135deg, #5f9cff, #6a5af9);
    }

    .google-btn {
        width: 100%;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: linear-gradient(135deg, #5f9cff, #6a5af9);
        color: white;
        font-size: 15px;
        font-weight: 800;
        text-decoration: none;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------- LOGIN ----------------
def login_page():

    auth_ui()

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:

        st.markdown('<div class="banner">🥛 Dairy4Cast</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Login to continue</div>', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            cursor.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password)
            )
            user = cursor.fetchone()

            if user:
                st.session_state.logged_in = True
            

                # ✅ ADDED: SAVE TO SUPABASE
                existing = supabase.table("users").select("*").eq("email", email).execute()

                if not existing.data:
                    supabase.table("users").insert({
                        "email": email
                    }).execute()

                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

        st.markdown("---")

        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent"
        }

        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

        st.markdown(
            f"""
            <a href="{google_auth_url}" target="_self" class="google-btn">
                 Continue with Google
            </a>
            """,
            unsafe_allow_html=True
        )


# ---------------- SIGNUP ----------------
def signup_page():

    auth_ui()

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:

        st.markdown('<div class="banner">🥛 Dairy4Cast</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Create account</div>', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup", use_container_width=True):

            if not email or not password:
                st.warning("Please fill all fields")
                return

            try:
                cursor.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?, ?)",
                    (email, password)
                )
                conn.commit()

                # ✅ ADDED: SAVE TO SUPABASE
                existing = supabase.table("users").select("*").eq("email", email).execute()

                if not existing.data:
                    supabase.table("users").insert({
                        "email": email
                    }).execute()

                st.success("Account created successfully 🎉")

            except:
                st.error("Email already exists ❌")

        st.markdown("---")

        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent"
        }

        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

        st.markdown(
            f"""
            <a href="{google_auth_url}" target="_self" class="google-btn">
                 Continue with Google
            </a>
            """,
            unsafe_allow_html=True
        )
