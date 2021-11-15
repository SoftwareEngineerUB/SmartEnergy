
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

from flask import render_template

from server.general.general import General


class Mailer:
    def __init__(self):
        self.server = None
        self.general_settings = General.getGeneralSettings()
        self.initializeConnection()
        super().__init__()

    def __del__(self):
        if self.server is not None:
            self.server.quit()
            self.server = None
        pass

    def initializeConnection(self):
        smtp_server = self.general_settings['mail']['host']
        port = self.general_settings['mail']['port']
        sender_email = self.general_settings['mail']['username']
        password = self.general_settings['mail']['password']

        try:
            self.server = smtplib.SMTP_SSL(smtp_server, port)
            self.server.ehlo()
            self.server.login(sender_email, password)
        except Exception as e:
            print(e)

    def sendMail(self, receiver, subject, content, html_content=None, attachments=None, sender=None):

        if attachments is None:
            attachments = []

        message = MIMEMultipart()
        message["Subject"] = subject
        message["Date"] = formatdate(localtime=True)
        if sender is None:
            sender = self.general_settings['mail']['username']
        message["From"] = sender
        message["To"] = receiver

        part1 = MIMEText(content, "plain")

        message.attach(part1)

        for attachment in attachments:
            part = MIMEBase('application', "octet-stream")
            with open(attachment, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(attachment).name))
            message.attach(part)

        try:
            self.server.sendmail(self.general_settings['mail']['username'], receiver, message.as_string())
        except Exception as e:
            print(e)

        return True

    def sendTemplateMail(self, receiver, template_name, values: dict, attachments=None, sender=None):
        if attachments is None:
            attachments = []
        subject = self.general_settings['emails'][template_name]['subject']
        message = self.general_settings['emails'][template_name]['message']
        for key in values.keys():
            message = message.replace(f"[{key}]", values[key])
            subject = subject.replace(f"[{key}]", values[key])

        html_message = message
        # html_message = render_template("email-template.html", subject=subject, content=message)

        return self.sendMail(receiver, subject, message, html_content=html_message, attachments=attachments, sender=sender)
