"""Test module for request assignee notification"""

# Standard library
from os import getenv
import json
from unittest.mock import patch

# utilities
from api.utilities.constants import MESSAGES, CHARSETS

BASE_URL = getenv('BASE_URL')
PASSWORD_RESET = BASE_URL + '/user/password/reset'
PASSWORD_RESET_CHANGE = BASE_URL + '/user/password/reset?token={}'


@patch('api.services.email.MailGun.with_api')
class TestPasswordReset:
    """Test the password reset """

    def test_password_reset_endpoint_with_a_not_verified_email_fails(
            self, mock_mailgun, client, headers, new_user_two):
        """Test for when the email is not yet verified.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user_two: Creates a new user

        Returns:
            None

        """

        user = new_user_two.save()

        data = {'email': user.email}

        response_object = client.post(
            PASSWORD_RESET, headers=headers, data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 401
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['NOT_VERIFIED']

    def test_password_reset_endpoint_with_invalid_email_fails(
            self, mock_mailgun, init_db, client, headers):
        """Test for when the email is invalid.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header

        Returns:
            None

        """

        data = {'email': 'test@xample'}

        response_object = client.post(
            PASSWORD_RESET, headers=headers, data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 400
        assert response['status'] == 'error'
        assert response['errors']['email'][0] == MESSAGES['EMAIL_FORMAT']
        assert response['message'] == MESSAGES['ERROR']

    def test_password_reset_endpoint_with_unknown_email_fails(
            self, mock_mailgun, init_db, client, headers):
        """Test for when the email is not found.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header

        Returns:
            None

        """

        data = {'email': 'test@xample.com'}

        response_object = client.post(
            PASSWORD_RESET, headers=headers, data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['NOT_FOUND']

    def test_password_reset_endpoint_succeeds(self, mock_mailgun, new_user,
                                              client, headers):
        """Test the password reset.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user (func): Creates new user

        Returns:
            None

        """

        user = new_user.save()

        data = {'email': user.email}

        response_object = client.post(
            PASSWORD_RESET, headers=headers, data=json.dumps(data))
        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['RESET_LINK']

    def test_password_change_endpoint_invalid_token(
            self, mock_mailgun, new_user, generate_token, client, headers):
        """Test the password reset.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user (func): Creates new user
            generate_token (func):

        Returns:
            None

        """

        user = new_user.save()

        token = generate_token(
            dict(email=user.email), 'test_password_reset', minutes=5)

        data = {'password': 'Password@123'}

        response_object = client.patch(
            PASSWORD_RESET_CHANGE.format(token),
            headers=headers,
            data=json.dumps(data))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['RESET_LINK_RESEND']

    def test_password_change_endpoint_expired_token(
            self, mock_mailgun, new_user, generate_token, client, headers):
        """Test the password reset.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user (func): Creates new user
            generate_token (func):

        Returns:
            None

        """

        user = new_user.save()

        token = generate_token(
            dict(email=user.email), 'test_password_reset', minutes=-5)

        data = {'password': 'Password@123'}

        response_object = client.patch(
            PASSWORD_RESET_CHANGE.format(token),
            headers=headers,
            data=json.dumps(data))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 403
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['EXPIRED_TOKEN']

    def test_password_change_endpoint_succeeds(self, mock_mailgun,
                                               new_user_two, client, headers):
        """Test the password reset.

        Args:
            mock_mailgun (object): mock instance for mailGun mailing client
            client (func): Flask client instance
            headers (func): Header
            new_user_two (func): Creates new user

        Returns:
            None

        """

        user = new_user_two.save()

        token = user.password_reset
        data = {'password': 'Password@123'}

        response_object = client.patch(
            PASSWORD_RESET_CHANGE.format(token),
            headers=headers,
            data=json.dumps(data))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['PROCEED_TO_LOGIN'].format(
            'Your password has been changed')
