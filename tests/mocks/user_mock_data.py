"""Mock data"""

# utilities
from api.utilities.encryption import Encryption
from api.utilities.push_id import PushID

USER = {
    'firstname': 'Test',
    'lastname': 'User',
    'email': 'test.user@example.com',
    'password': 'password1234',
}

NEW_USER = {
    'first_name': 'Test',
    'last_name': 'User',
    'username': PushID().next_id()[8:],
    'email': 'test.user@example.com',
    'password': Encryption.hash('password123')
}

NEW_USER_2 = {
    'first_name': 'Test1',
    'last_name': 'User2',
    'username': PushID().next_id()[8:],
    'email': 'test1.user2@example.com',
    'password': Encryption.hash('password123')
}

INCOMPLETE_USER = {
    'firstname': 'i',
    'lastname': 'i',
    'email': 'test.user@example.com',
    'password': 'password1234'
}

DECODED_TOKEN = {
    'data': {
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'test.user@example.com',
        'password': 'password1234'
    },
    'iat': 1545321234,
    'exp': 1546530834,
    'aud': 'Yard-it.com.ng',
    'iss': 'Yard-it-API'
}

LOGIN_USER = {'email': 'test1.user2@example.com', 'password': 'password123'}

WRONG_USER_DATA = {'email': 'test1.user2@example.com', 'password': 'password1'}

WRONG_USER_EMAIL = {'email': 'test.user2@example.com', 'password': 'password1'}

INVALID_USER_LOGIN_DATA = {'email': '', 'password': ''}

INVALID_USER_EMAIL = {'email': 'test.user2@examplecom', 'password': ''}
