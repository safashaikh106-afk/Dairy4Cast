import streamlit as st
import re
import urllib.parse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import smtplib
from email.message import EmailMessage


# ---------------- PDF GENERATOR ----------------
def generate_pdf(df):
    file_path = "prediction_report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Dairy Sales Prediction Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    story.append(table)
    doc.build(story)
    return file_path


# ---------------- EMAIL SENDER ----------------
def send_email(to_email, file_path):
    sender = "safashaikh106@gmail.com"
    password = "esnmtnzljwzcxgwf"

    msg = EmailMessage()
    msg["Subject"] = "Dairy Prediction Report"
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content("Attached is your Dairy Sales Prediction Report.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="prediction_report.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


# ---------------- UI ----------------
def send_report_ui():
    st.markdown("## 📨 Send / Share Report")

    # REPORT CARD
    st.markdown("""
    <div style="
        border:1px solid #d0d7de;
        border-radius:12px;
        padding:18px;
        background:#ffffff;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
        margin-bottom:20px;
    ">
    <h4>📄 Report Contents</h4>
    <ul>
        <li>Sales summary and totals</li>
        <li>Best-selling products, locations, and days</li>
        <li>Revenue and cost analysis</li>
        <li>Profit margins and trends</li>
        <li>Next-day sales predictions</li>
        <li>Confidence levels for predictions</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if "predicted_df" not in st.session_state:
        st.warning("⚠ Run prediction first.")
        return

    df = st.session_state.predicted_df

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("📧 Email")
    with col2:
        phone = st.text_input("📱 WhatsApp Number", placeholder="9876543210")

    if st.button("🚀 Generate & Share Report"):

        if not email and not phone:
            st.error("Please enter Email or WhatsApp number")
            return

        pdf_path = generate_pdf(df)

        # -------- EMAIL --------
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Invalid email format")
                return

            send_email(email, pdf_path)
            st.success("📧 Report sent via Email")

        # -------- DOWNLOAD --------
        st.subheader("⬇ Download Report")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Prediction Report",
                data=f,
                file_name="prediction_report.pdf",
                mime="application/pdf"
            )

        # -------- WHATSAPP SHARE --------
        if phone:
            phone = phone.replace(" ", "").strip()

            if phone.startswith("+"):
                phone = phone[1:]

            if phone.startswith("91") and len(phone) == 12:
                phone = phone[2:]

            if not phone.isdigit() or len(phone) != 10:
                st.error("WhatsApp number must be 10 digits (example: 9876543210)")
                return

            message = (
                "📊 Dairy Sales Prediction Report\n\n"
                "The report has been sent to your email successfully.\n\n"
                "— Dairy Analytics"
            )

            encoded_msg = urllib.parse.quote(message)
            whatsapp_link = f"https://wa.me/91{phone}?text={encoded_msg}"

            st.subheader("📱 Share via WhatsApp")

            st.markdown(f"""
<a href="{whatsapp_link}" target="_blank" style="text-decoration:none;">
    <button style="
        display:inline-block;
        background: linear-gradient(90deg, #6366F1, #4F46E5);
        color:white;
        padding:12px 24px;
        border:none;
        border-radius:12px;
        font-size:18px;
        font-weight:600;
        cursor:pointer;
    ">
        📲 Click here to open WhatsApp
    </button>
</a>
""", unsafe_allow_html=True)
