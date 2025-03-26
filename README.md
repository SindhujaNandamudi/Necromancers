# Reconciliation and Anomaly Detection System

This project performs reconciliation by detecting anomalies in financial data, generating explanations using AI, and notifying relevant parties via email.

## 📌 Prerequisites

Ensure you have the following installed:
- Python 3.8+
- Required Python libraries:
  - `pandas`
  - `openpyxl`
  - `smtplib` (built-in)
  - `sklearn`
  - `google-generativeai`
  - `openai`

## 🚀 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/reconciliation-anomaly-detection.git
   cd reconciliation-anomaly-detection
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## 🔑 Configuration

Before running the script, configure the following values:

1. **Set up OpenAI API Key**
   - Replace `your-api-key-here` in the script with your actual OpenAI API key.
   - If using Google Gemini AI, update `your-model-name-here` accordingly.

2. **Configure Email Credentials**
   - Replace `your-email-here`, `your-app-password-here`, and `recipient-email-here` with actual values.
   - If using Gmail, enable [App Passwords](https://support.google.com/accounts/answer/185833?hl=en).

3. **Prepare Your Data**
   - Ensure your Excel file (`your-excel-file.xlsx`) has the required columns:
     - `trade_id`
     - `quantity`
     - `trade_date`
     - `settlement_date`
     - `recon_date`
   
## 🏃 Running the Script

To execute the reconciliation process, run:
```sh
python reconciliation_script.py
```

This will:
- Load and process the reconciliation data.
- Apply anomaly detection.
- Generate AI-based explanations for anomalies.
- Send email notifications for detected breaks.
- Save the final report to `your-output-file.xlsx`.

## 📊 Output
- **Email notifications**: Sent to the recipient if anomalies are found.
- **Final report**: Saved as an Excel file containing reconciliation results.

## 🛠 Troubleshooting

- **Email not sending?**
  - Check SMTP configuration and credentials.
  - Ensure App Passwords are enabled for Gmail.

- **No anomalies detected?**
  - Try adjusting the `contamination` parameter in `IsolationForest`.

- **Missing dependencies?**
  - Run `pip install -r requirements.txt` to install required packages.

## 📝 License
This project is for educational and internal use. Modify as needed for production environments.

---

✨ Happy Reconciling! 🚀

