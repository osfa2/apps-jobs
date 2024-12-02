import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from singleton_base import SingletonBase
from dotenv import load_dotenv


class Email(SingletonBase):

    @staticmethod
    def send_email(subject, body, to_email, from_email):
        load_dotenv()

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(os.environ['SMTP_HOST'], os.environ['SMTP_PORT'])
            server.starttls()
            server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
            server.send_message(msg)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")            

Email().send_email('SUBJECT', 'BODY', 'djb83694@uga.edu', 'josh.bailey@uga.edu')