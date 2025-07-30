import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(workflow_name, repo_name, workflow_run_id):  # Function to send an email notification
    smtp_server = os.getenv('SMTP_SERVER')  # Get SMTP server from environment variable
    smtp_port = os.getenv('SMTP_PORT')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    print(f"Connecting to {smtp_server}:{smtp_port} as {smtp_username}")    # Debugging output to check SMTP connection details

    subject = f"Workflow '{workflow_name}' in '{repo_name}' completed"  # Email subject
    body = f"The workflow '{workflow_name}' in repository '{repo_name}' has completed.\nRun_ID: {workflow_run_id}"  # Email body

    msg = MIMEMultipart()   # Create a multipart email message
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain')) # Attach the body to the email message

    try:        # Attempt to send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

send_email(         # Call the function with environment variables
    os.getenv('WORKFLOW_NAME'),
    os.getenv('GITHUB_REPOSITORY'),
    os.getenv('GITHUB_RUN_ID')
)
