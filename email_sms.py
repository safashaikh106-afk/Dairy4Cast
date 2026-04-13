import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage
import re
import urllib.parse


def send_report_ui():
    st.markdown("<h2>📨 Send Report</h2>", unsafe_allow_html=True)

    df = st.session_state.get("uploaded_data")

    if df is None:
        st.warning("⚠ Please upload CSV in Dashboard first.")
        return

    # --- Input ---
    col1, col2 = st.columns(2)
    with col1:
        owner_email = st.text_input("📧 Owner Email")
    with col2:
        owner_phone = st.text_input("📱 Owner WhatsApp Number (+91XXXXXXXXXX)")

    # --- Preview ---
    st.subheader("📄 Report Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # --- Download Button ---
    csv_data = df.to_csv(index=False)
    st.download_button(
        "⬇ Download Report CSV",
        csv_data,
        "dairy_report.csv",
        "text/csv"
    )

    # --- Action ---
    if st.button("🚀 Send Report"):

        # ---- Email Validation ----
        if not owner_email:
            st.warning("Please enter email address.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", owner_email):
            st.warning("Please enter valid email.")
            return

        try:
            # -------- EMAIL --------
            msg = EmailMessage()
            msg["Subject"] = "Daily Dairy Report"
            msg["From"] = "safashaikh106@gmail.com"
            msg["To"] = owner_email

            msg.set_content("Attached is today's dairy sales report.")

            msg.add_attachment(
                csv_data,
                maintype="text",
                subtype="csv",
                filename="dairy_report.csv"
            )

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("safashaikh106@gmail.com", "esnmtnzljwzcxgwf")
            server.send_message(msg)
            server.quit()

            st.success("📧 Report sent to Email!")

            # -------- WHATSAPP CLICK --------
            if owner_phone:
                owner_phone = owner_phone.replace(" ", "").strip()

                if not owner_phone.startswith("+"):
                    st.warning("WhatsApp number must start with +91")
                    return

                if not owner_phone[1:].isdigit():
                    st.warning("WhatsApp number must contain digits only")
                    return

                if len(owner_phone) < 12:
                    st.warning("WhatsApp number looks too short")
                    return

                clean_number = owner_phone.replace("+", "")

                message = f"""
📊 Dairy Sales Report

Rows: {len(df)}

✅ Report sent to Email
✅ CSV available in Dashboard

Please download your report from the app.

— Dairy Analytics
"""

                encoded_message = urllib.parse.quote(message)

                whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"

                st.markdown("### 📱 Share via WhatsApp")
                st.link_button("👉 Open WhatsApp Chat", whatsapp_url)

        except Exception as e:
            st.error(f"❌ Error sending report: {e}")
