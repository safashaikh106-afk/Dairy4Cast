import streamlit as st
import requests

# ---------------- CONFIG ----------------
CLIENT_ID = "204866650872-1jgkgim3fho887gh4qtkt4gsq6md83kt.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


def google_login():
    if st.session_state.get("logged_in"):
        return

    st.markdown("## 🔐 Login with Google")

    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    request_uri = requests.Request("GET", AUTH_URL, params=auth_params).prepare().url

    st.markdown(f"[👉 Login with Google]({request_uri})")

    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]

        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(TOKEN_URL, data=data).json()

        if "access_token" in token_response:
            access_token = token_response["access_token"]
            userinfo = requests.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            ).json()

            st.session_state.logged_in = True
            st.session_state.user_email = userinfo.get("email")
            st.success(f"✅ Logged in as {st.session_state.user_email}")
            st.rerun()
