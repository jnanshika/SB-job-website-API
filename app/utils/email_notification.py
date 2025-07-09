# app/utils/email_utils.py
import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_email(subject, body, recipients):
    # Basic SMTP setup (use Flask-Mail in production)
    smtp_server = current_app.config['SMTP_SERVER']
    smtp_port = current_app.config['SMTP_PORT']
    smtp_username = current_app.config['SMTP_USERNAME']
    smtp_password = current_app.config['SMTP_PASSWORD']
    sender = current_app.config['MAIL_SENDER']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipients, msg.as_string())
