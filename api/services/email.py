"""Sending emails"""

# system imports
from os import getenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# utilities
from .email_config import SMTPConfig
from api.utilities.helpers.errors import raises
from api.utilities.constants import EXCEPTIONS


class MailGun(SMTPConfig):
    """MailGun SMTP configurations"""

    sender = 'Support <mailgun@{}>'
    domain_name = getenv('MAILGUN_DOMAIN_NAME')
    api_key = getenv('MAILGUN_API_KEY')

    @classmethod
    def with_smtp(cls, receiver, email_template, subject):
        """Sends email through the SMTP

        Args:
            receiver (str): The receivers email
            email_template (str): the email template
            subject (str): The email subject

        Returns:
            None

        """

        msg = MIMEMultipart('alternative')
        sender = cls.sender.format(cls.domain_name)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        part1 = MIMEText(email_template, 'html')
        msg.attach(part1)

        cls.send(sender, receiver, msg)

    @classmethod
    def with_api(cls, receiver, email_template, subject):
        """Sends email through the mailGun API

        Args:
            receiver (str): The receivers email
            email_template (str): the email template
            subject (str): The email subject

        Returns:
            None

        """

        url = 'https://api.mailgun.net/v3/{}/messages'.format(cls.domain_name)
        auth = ('api', cls.api_key)
        data = {
            'from': cls.sender.format(cls.domain_name),
            'to': receiver,
            'subject': subject,
            "html": email_template,
        }

        response = cls.api_send(url, auth, data)

        if response.status_code != 200:
            raises(EXCEPTIONS['EMAIL_ERROR'], 500)
