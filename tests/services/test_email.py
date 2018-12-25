"""Test module to test the email."""
import pytest
from unittest.mock import patch
from api.services.email import MailGun
from api.utilities.validations.custom_validations_error import  \
    (ValidationError as CustomError)


@patch('api.services.email_config.SMTPConfig.send')
class TestSMTPEmail:
    """Test the email services methods"""

    def test_the_with_smtp_method(self, mock_smtp_config):
        """Test the Mailgun.with_smtp method"""

        MailGun.with_smtp('email', 'template', 'subject')
        assert True


class ApiResponse(object):
    """Mock for the mailgun api response"""
    status_code = 200

    def __init__(self, url, auth, data):
        pass


class TestEmailWithAPI:
    """Test the mailGun api"""

    @patch('api.services.email_config.SMTPConfig.api_send', ApiResponse)
    def test_the_with_api_method(self):
        """Test the Mailgun.with_smtp method"""

        MailGun.with_api('email', 'template', 'subject')
        assert True

    @patch('api.services.email_config.SMTPConfig.api_send')
    def test_the_with_api_method_fails(self, mock):
        """Test the Mailgun.with_smtp method"""

        with pytest.raises(CustomError):
            MailGun.with_api('email', 'template', 'subject')
