"""Email services configurations"""

# system imports
import smtplib
import requests
from requests.exceptions import HTTPError, ConnectionError
from smtplib import SMTPException, SMTPDataError
from os import getenv

# utilities
from api.utilities.helpers.errors import raises
from api.utilities.constants import EXCEPTIONS

email_host = getenv('SMTP_HOSTNAME', 'smtp.mailgun.org')
email_port = getenv('SMTP_PORT', 587)
smtp_user = getenv('SMTP_USER')
smtp_password = getenv('SMTP_PASSWORD')


class SMTPConfig(object):
    """SMTP setup class"""

    @classmethod
    def send(cls, sender, receiver, msg):
        """Sends email

        Args:
            sender (str): Sender's email
            receiver (str): Receiver email
            msg (object): Body of the message

        Raises:
            Exceptions

        """

        try:
            smtp_obj = smtplib.SMTP(email_host, email_port)

            smtp_obj.login(smtp_user, smtp_password)

            smtp_obj.sendmail(sender, receiver, msg.as_string())

            smtp_obj.quit()

        except (SMTPException, SMTPDataError):
            raises(EXCEPTIONS['EMAIL_ERROR'], 500)

    @classmethod
    def api_send(cls, url, auth, data):
        """

        Args:
            url (str): Url for the post request
            auth (tuple): Authentication tuple
            data (dict): The data to be sent

        Returns:
            Response: Response object

        """

        try:
            return requests.post(url, auth=auth, data=data)

        except (HTTPError, ConnectionError) as err:
            exception_mapper = {
                HTTPError: raises(EXCEPTIONS['EMAIL_ERROR'], 500),
                ConnectionError: raises(EXCEPTIONS['CONNECTION_ERROR'], 500)
            }

            exception_mapper.get(type(err))
