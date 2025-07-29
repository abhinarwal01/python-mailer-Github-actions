import smtplib
import os
from email.mime.text import MIMEText   
from email.mime.multipart import MIMEMultipart

def send_email(workflow_name, repo_name, workflow_run_id):
    #Email details
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    #Email content
    subject = f"Workflow {workflow_name} in {repo_name} has failed"
    body = f"The workflow '{workflow_name}' in the repository '{repo_name}' has encountered an error.\nMore details can be found in the logs: \nRun_ID: {workflow_run_id}"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error: {e}")    

send_email(
    os.getenv('workflow_name'),
    os.getenv('github_repository'),
    os.getenv('github_run_id')
)

