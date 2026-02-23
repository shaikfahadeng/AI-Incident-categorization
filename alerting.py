import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv("ALERT_EMAIL") or ""
PASSWORD = os.getenv("ALERT_PASSWORD") or ""
RECEIVER = os.getenv("ALERT_RECEIVER") or ""


def send_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = RECEIVER

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("🚨 ALERT EMAIL SENT")
    except Exception as e:
        print("Email failed:", e)