import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(workflow_name, repo_name, workflow_run_id):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))   # safe default
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    subject = f"Workflow {workflow_name} in {repo_name} has finished"
    body = f"The workflow '{workflow_name}' in the repository '{repo_name}' has completed.\nRun_ID: {workflow_run_id}"

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print(f"Connecting to {smtp_server}:{smtp_port} as {smtp_username}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, receiver_email, text)
        server.quit()
        print(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

send_email(
    os.getenv('WORKFLOW_NAME'),
    os.getenv('GITHUB_REPOSITORY'),
    os.getenv('GITHUB_RUN_ID')
)
