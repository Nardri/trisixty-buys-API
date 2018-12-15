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

