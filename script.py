import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(workflow_name, repo_name, workflow_run_id):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    subject = f"Workflow {workflow_name} in {repo_name} has failed"
    body = (
        f"The workflow '{workflow_name}' in the repository '{repo_name}' has encountered an error.\n"
        f"More details can be found in the logs:\nRun_ID: {workflow_run_id}"
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    send_email(
        os.getenv('WORKFLOW_NAME'),
        os.getenv('GITHUB_REPOSITORY'),
        os.getenv('GITHUB_RUN_ID')
    )
