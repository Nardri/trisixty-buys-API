"""User email activation test"""

# system imports
from os import getenv

# third party imports
from flask import json
from unittest.mock import patch

# utilities
from api.utilities.constants import CHARSETS, MESSAGES

BASE_URL = getenv('BASE_URL')
ACTIVATE_URL = BASE_URL + '/user/activate?token={}'
RESEND_EMAIL = BASE_URL + '/user/activate/{}/resend'


@patch('api.services.email.MailGun.with_api')
class TestUserEmailActivation:
    """Tests the the user email activation"""

    def test_email_activation_endpoint_with_already_verified_email_fails(
            self, mock_mailgun, client, generate_token, headers, new_user):
        """Test for when the email is already verified.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            generate_token (func): Generates a token
            headers (func): Header
            new_user: Creates a new user

        Returns:
            None

        """

        user = new_user.save()

        token = generate_token(
            dict(email=user.email), 'test_email_activation', minutes=5)

        response_object = client.get(
            ACTIVATE_URL.format(token), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 409
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['VERIFIED']

    def test_email_activation_endpoint_with_expired_token_fails(
            self, mock_mailgun, client, generate_token, headers, new_user):
        """Test for when the verification token has expired.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            generate_token (func): Generates a token
            headers (func): Header
            new_user: Creates a new user

        Returns:
            None

        """

        user = new_user.save()

        token = generate_token(
            dict(email=user.email), 'test_email_activation', minutes=-5)

        response_object = client.get(
            ACTIVATE_URL.format(token), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 403
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['EXPIRED_TOKEN']

    def test_email_activation_endpoint_succeeds(self, mock_mailgun, client,
                                                headers, new_user_two):
        """Test email verification.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user_two: Creates a new user

        Returns:
            None

        """

        user = new_user_two.save()

        token = user.token

        response_object = client.get(
            ACTIVATE_URL.format(token), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['PROCEED_TO_LOGIN'].format(
            'Your account has been successfully verified')

    def test_resend_email_verification_link_succeeds(
            self, mock_mailgun, client, headers, new_user_two):
        """Test email verification.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user_two: Creates a new user

        Returns:
            None

        """
        user = new_user_two.save()

        response_object = client.get(
            RESEND_EMAIL.format(user.email), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['RESEND_EMAIL']

    def test_resend_email_verification_link_with_invalid_email_fails(
            self, mock_mailgun, client, headers):
        """Test email verification.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header

        Returns:
            None

        """
        response_object = client.get(
            RESEND_EMAIL.format('test@exapmple'), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 400
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['INVALID_EMAIL']

    def test_resend_email_verification_link_with_unknown_email_fails(
            self, mock_mailgun, init_db, client, headers):
        """Test email verification.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header

        Returns:
            None

        """
        response_object = client.get(
            RESEND_EMAIL.format('test@exapmple.com'), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['NOT_FOUND']

    def test_resend_email_verification_link_with_verified_email_fails(
            self, mock_mailgun, new_user, client, headers):
        """Test email verification.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header

        Returns:
            None

        """

        user = new_user.save()

        response_object = client.get(
            RESEND_EMAIL.format(user.email), headers=headers)
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 409
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['VERIFIED']
