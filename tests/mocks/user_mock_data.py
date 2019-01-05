"""Mock data"""

# utilities
from api.utilities.encryption import Encryption
from api.utilities.push_id import PushID

USER_DATA = {
    'firstname': 'Test',
    'lastname': 'User',
    'email': 'test.user@example.com',
    'password': 'Password@1234',
}

FIXTURE_NEW_USER = {
    'first_name': 'Test',
    'last_name': 'User',
    'username': PushID().next_id()[8:],
    'email': 'test.user@example.com',
    'password': Encryption.hash('Password@1234'),
    'verified': True,
    'token': None,
    'password_reset': None
}

FIXTURE_NEW_USER_TWO = {
    'first_name':
    'Test',
    'last_name':
    'User',
    'username':
    PushID().next_id()[8:],
    'email':
    'test.user@example.com',
    'password':
    Encryption.hash('Password@1234'),
    'verified':
    False,
    'token':
    Encryption.tokenize(
        dict(email='test.user@example.com'),
        subject='Email_verification',
        minutes=5),
    'password_reset':
    Encryption.tokenize(
        dict(email='test.user@example.com'),
        subject='password_reset',
        minutes=5)
}

INCOMPLETE_USER = {
    'firstname': 'i',
    'lastname': 'i',
    'email': 'test.user@example.com',
    'password': 'Password@1234'
}

DECODED_TOKEN = {
    'data': {
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'test.user@example.com',
        'password': 'Password@1234'
    },
    'iat': 1545321234,
    'exp': 1546530834,
    'aud': 'Yard-it.com.ng',
    'iss': 'Yard-it-API',
    'sub': 'Testing'
}

WRONG_USER_EMAIL = {'email': 'wrong@example.com', 'password': 'Password@1234'}

INVALID_USER_LOGIN_DATA = {'email': '', 'password': ''}

INVALID_USER_EMAIL = {'email': 'test.user2@examplecom', 'password': ''}
