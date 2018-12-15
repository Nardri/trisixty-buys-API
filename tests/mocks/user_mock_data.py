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
