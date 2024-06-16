import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
import boto3
from config import Config
import markdown

class EMailSender:
    def __init__(self):
        self.config = Config()
        email_config = self.config.get_email_config()
        self.sender_name = email_config['sender_name']
        self.sender_email = email_config['sender_email']

    def send_email(self, to_email: str, subject: str, body: str):
        ses = boto3.client('ses', 'eu-central-1')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((str(Header(self.sender_name, 'utf-8')), self.sender_email))
        msg['To'] = to_email

        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(markdown.markdown(body), 'html'))

        ses.send_raw_email(
            Source=formataddr((str(Header(self.sender_name, 'utf-8')), self.sender_email)),
            Destinations=[to_email],
            RawMessage={'Data': msg.as_string()}
        )