import smtplib
import pandas as pd
import openai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sklearn.ensemble import IsolationForest
import google.generativeai as genai
from openai import OpenAI

# 🔐 Hardcoded OpenAI API Key (Replace with your actual key)
genai.configure(api_key="AIzaSyAseWxam3C3Y-XJePweJVvX_peREF2M8QM")

# 📂 Load Excel file
file_path = "reconciliation_data.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# 🔍 Select numerical columns for anomaly detection
features = ["quantity", "trade_date", "settlement_date"]
df_filtered = df[features].copy()

# 🕒 Convert dates to Unix timestamps
for col in ["trade_date", "settlement_date", "recon_date"]:
    if col in df.columns:
        df_filtered[col] = pd.to_datetime(df[col]).view('int64') // 10**9

# 🛠 Handle missing values
df_filtered.fillna(df_filtered.mean(), inplace=True)

# 🔥 Train Isolation Forest for anomaly detection
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = iso_forest.fit_predict(df_filtered)

# 🎯 Classify anomalies as Break (outliers) or Match (normal)
df["Status"] = df["anomaly"].map({-1: "Break", 1: "Match"})

# 💡 Generate explanations using GPT
def generate_explanation(trade_id, reason):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Explain why Trade ID {trade_id} is a break: {reason}")
    return response.text.strip()


df["Break Explanation"] = df.apply(lambda row: generate_explanation(row["trade_id"], "Anomaly detected in reconciliation") if row["Status"] == "Break" else "", axis=1)


# 📧 Email Configuration (Hardcoded Credentials)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "gmail-app-id"  # Prefer using an App Password
RECIPIENT_EMAIL = "recipient-email@gmail.com"

# ✉️ Function to send email notifications
def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()
        print(f"✅ Email Sent Successfully to {recipient}!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# 🚀 Send email notifications for detected breaks
for _, row in df[df["Status"] == "Break"].iterrows():
    email_subject = f"Anomaly Detected in Trade ID {row['trade_id']}"
    email_body = f"""Dear Team,

A break has been detected in Trade ID {row['trade_id']}.

Reason: {row['Break Explanation']}

Please review and take necessary action.

Best regards,
Reconciliation System"""
    send_email(email_subject, email_body, RECIPIENT_EMAIL)

# 📊 Save results
output_file = "final_reconciliation_report.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Process Completed - Anomaly Detection, Break Explanation & Email Notifications Sent! Results saved to {output_file}.")
