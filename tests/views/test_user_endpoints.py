"""Test for user endpoint"""

# system imports
from os import getenv

# third party imports
from flask import json

# utilities
from api.utilities.constants import CHARSETS, MESSAGES

# mocks
from ..mocks.user_mock_data import (USER, LOGIN_USER, WRONG_USER_DATA,
                                    INCOMPLETE_USER, INVALID_USER_LOGIN_DATA,
                                    WRONG_USER_EMAIL, INVALID_USER_EMAIL)

BASE_URL = getenv('BASE_URL')
REGISTER_URL = BASE_URL + '/user/register'
LOGIN_URL = BASE_URL + '/user/login'


class TestUserEndpoint:
    """Test User endpoints"""

    def test_user_registration_succeeds(self, init_db, headers, client):
        """Should successfully create a new user.

        Args:
            init_db (func): Database instance
            headers (func): Header
            client (func): Flask client instance

        Returns:
            None

        """

        response_object = client.post(
            REGISTER_URL, headers=headers, data=json.dumps(USER))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        data = response['data']

        assert response_object.status_code == 201
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['CREATED'].format('User')
        assert isinstance(data['token'], str)

    def test_user_registration_with_duplicate_data_fails(
            self, client, headers, new_user):
        """Should return a 409 status code when user tries to
        create a new user, that already exists.

        Args:
            headers (func): Header
            client (func): Flask client instance
            new_user (func): Creates new user to the database.

        Returns:
            None

        """

        user = new_user

        user_data = {
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'password': 'passowrd123'
        }

        response_object = client.post(
            REGISTER_URL, headers=headers, data=json.dumps(user_data))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 409
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['DUPLICATES']\
            .format(user_data['email'])

    def test_user_registration_with_incomplete_data_succeeds(
            self, init_db, headers, client):
        """Should throw an error when the required fields are empty.

        Args:
            init_db (func): Database instance
            headers (func): Header
            client (func): Flask client instance

        Returns:
            None

        """

        response_object = client.post(
            REGISTER_URL, headers=headers, data=json.dumps(INCOMPLETE_USER))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        errors = response['errors']

        assert response_object.status_code == 400
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['ERROR']
        assert errors['lastname'][0] == MESSAGES['REQUIRED_FIELDS']
        assert errors['firstname'][0] == MESSAGES['REQUIRED_FIELDS']

    def test_user_login_succeeds(self, headers, client, new_user_two):
        """Should successfully log in a registered user.

        Args:
            headers (func): Header
            client (func): Flask client instance
            new_user_two (func): Creates new user to the database.


        Returns:
            None

        """
        new_user_two.save()

        response_object = client.post(
            LOGIN_URL, headers=headers, data=json.dumps(LOGIN_USER))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        data = response['data']

        assert response_object.status_code == 200
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['LOGIN']
        assert isinstance(data['token'], str)

    def test_user_login_fails(self, headers, client, new_user_two):
        """Should not login a user when incorrect Credentials are provided.

        Args:
            headers (func): Header
            client (func): Flask client instance
            new_user_two (func): Creates new user to the database.


        Returns:
            None

        """

        new_user_two.save()

        response_object = client.post(
            LOGIN_URL, headers=headers, data=json.dumps(WRONG_USER_DATA))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 401
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['UNAUTHORIZED']

    def test_user_login_with_a_wrong_email_fails(self, headers, client,
                                                 new_user_two):
        """Should not login a user when wrong email is provided.

        Args:
            headers (func): Header
            client (func): Flask client instance
            new_user_two (func): Creates new user to the database.


        Returns:
            None

        """

        new_user_two.save()

        response_object = client.post(
            LOGIN_URL, headers=headers, data=json.dumps(WRONG_USER_EMAIL))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 404
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['NOT_FOUND']

    def test_user_login_with_incomplete_data_succeeds(self, init_db, headers,
                                                      client):
        """Should throw an error when the required fields are empty.

        Args:
            init_db (func): Database instance
            headers (func): Header
            client (func): Flask client instance

        Returns:
            None

        """

        response_object = client.post(
            LOGIN_URL,
            headers=headers,
            data=json.dumps(INVALID_USER_LOGIN_DATA))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        errors = response['errors']

        assert response_object.status_code == 400
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['ERROR']
        assert errors['email'][0] == MESSAGES['REQUIRED_FIELDS']
        assert errors['password'][0] == MESSAGES['REQUIRED_FIELDS']

    def test_user_login_with_a_wrong_email_format_fails(
            self, init_db, headers, client):
        """Should throw an error when the wrong email field is provided.

        Args:
            init_db (func): Database instance
            headers (func): Header
            client (func): Flask client instance

        Returns:
            None

        """

        response_object = client.post(
            LOGIN_URL, headers=headers, data=json.dumps(INVALID_USER_EMAIL))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        errors = response['errors']

        assert response_object.status_code == 400
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['ERROR']
        assert errors['email'][0] == MESSAGES['EMAIL_FORMAT']
        assert errors['password'][0] == MESSAGES['REQUIRED_FIELDS']
