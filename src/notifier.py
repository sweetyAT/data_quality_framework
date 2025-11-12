# src/notifier.py
import os
import json
import smtplib
from email.message import EmailMessage
from slack_sdk.webhook import WebhookClient

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")  # set in env
EMAIL_FROM = os.getenv("ALERT_FROM")        # e.g., 'you@example.com'
EMAIL_TO = os.getenv("ALERT_TO")            # comma-separated

def slack_alert(text: str):
    if not SLACK_WEBHOOK:
        print("No SLACK_WEBHOOK set; skipping slack alert.")
        return
    wb = WebhookClient(SLACK_WEBHOOK)
    resp = wb.send(text=text)
    print("Slack status:", resp.status_code)

def email_alert(subject: str, body: str):
    if not EMAIL_FROM or not EMAIL_TO:
        print("Email env not set; skipping email alert.")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO.split(",")
    msg.set_content(body)
    # Simple local SMTP (for production, use secured server)
    try:
        s = smtplib.SMTP("localhost")
        s.send_message(msg)
        s.quit()
        print("Email sent")
    except Exception as e:
        print("Email failed:", e)

def alert_if_needed(summary: dict, null_thresh_pct=0.05, outlier_count_thresh=1):
    problems = []
    if summary["schema"].get("missing_columns"):
        problems.append(f"Missing columns: {summary['schema']['missing_columns']}")
    if summary["nulls"]["problem_columns"]:
        problems.append(f"High nulls: {summary['nulls']['problem_columns']}")
    # any column with outliers > threshold
    outliers = {k:v for k,v in summary["outliers"]["outliers_count"].items() if v > outlier_count_thresh}
    if outliers:
        problems.append(f"Outliers detected: {outliers}")
    if problems:
        message = " | ".join(problems)
        slack_alert(message)
        email_alert("Data Quality Alert", message)
    else:
        print("No alerts; data quality OK.")
