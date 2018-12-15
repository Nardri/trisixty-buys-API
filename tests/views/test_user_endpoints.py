"""Test for user endpoint"""

from flask import json
from os import getenv
from api.utilities.constants import CHARSETS, MESSAGES
from ..mocks.user_mock_data import USER

BASE_URL = getenv('BASE_URL')
REGISTER_URL = BASE_URL + '/user/register'


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

        response_object = client.post(REGISTER_URL,
                                      headers=headers,
                                      data=json.dumps(USER))

        response = json.loads(response_object.data.decode(CHARSETS[0]))
        data = response['data']

        assert response_object.status_code == 201
        assert response['status'] == 'success'
        assert response['message'] == MESSAGES['CREATED'].format('User')
        assert isinstance(data['token'], str)

    def test_user_registration_with_duplicate_data_fails(self, client,
                                                         headers,
                                                         create_new_user):
        """Should return a 409 status code when user tries to
        create a new user, that already exists.

        Args:
            headers (func): Header
            client (func): Flask client instance
            create_new_user (func): Creates new user to the database.

        Returns:
            None

        """

        user = create_new_user

        user_data = {
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'password': 'passowrd123'
        }

        response_object = client.post(REGISTER_URL,
                                      headers=headers,
                                      data=json.dumps(user_data))

        response = json.loads(response_object.data.decode(CHARSETS[0]))

        assert response_object.status_code == 409
        assert response['status'] == 'error'
        assert response['message'] == MESSAGES['DUPLICATES']\
            .format(user_data['email'])


