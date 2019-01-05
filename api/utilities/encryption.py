"""Module for all encryption"""

# standard imports
import hashlib
import binascii
from os import urandom, getenv
from uuid import uuid4

# third party imports
from authlib.specs.rfc7519 import jwt
from authlib.specs.rfc7515.errors import DecodeError

# local imports
from api.utilities.constants import CHARSETS
from api.utilities.constants import MESSAGES
from api.utilities.helpers.date_time import date_time
from api.utilities.helpers.errors import raises


class Encryption:
    """Class for all encryption"""

    @staticmethod
    def hash(password):
        """Hash password.

        Args:
            password (Str): Password to hash.

        Returns:
            String: Hashed password.

        """

        # generate random values to generate the salt for hashing
        random_bytes = urandom(120) + str(uuid4()).encode(CHARSETS[1])

        # generate salt for the password hashing
        salt = hashlib.sha256(random_bytes).hexdigest().encode(CHARSETS[1])

        # hash the password
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode(CHARSETS[0]),
                                       salt, 100000)
        # convert the hash to a hexadecimal
        pwd_hash = binascii.hexlify(pwd_hash)

        # returns the hash + salt
        return (salt + pwd_hash).decode(CHARSETS[1])

    @staticmethod
    def verify(stored_password, provided_password):
        """Verify a stored password against one provided by user.

        Args:
            stored_password (Str): The stored password.
            provided_password (Str): The password provided by the user.

        Returns:
            Boolean:

        """

        # get the first 64 characters from the stored
        # password, this is the salt
        salt = stored_password[:64]

        # get the remaining characters from the 64th index,
        # this is the stored password
        stored_password = stored_password[64:]

        # hash the provided password
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode(CHARSETS[0]),
                                      salt.encode(CHARSETS[1]), 100000)
        # convert the hash to a hexadecimal and decode to ascii
        pwdhash = binascii.hexlify(pwdhash).decode(CHARSETS[1])

        # compares the hashed password with the stored hash
        return pwdhash == stored_password

    @staticmethod
    def tokenize(payload, subject=None, **kwargs):
        """Generates a token for the given payload.

        Args:
            payload (dict): Payload
            subject (str): Subject of the encryption

        Returns:
            String: JWT token

        """
        header = {'alg': 'RS256'}

        data = {
            'data':
            payload,
            'iat':
            date_time.time(),
            'exp':
            date_time.time(manipulate=True, manipulation_type='ADD', **kwargs),
            'aud':
            'Yard-it.com.ng',
            'iss':
            'Yard-it-API',
            'sub':
            subject
        }
        private_key = getenv('JWT_PRIVATE_KEY')

        token = jwt.encode(
            header=header, payload=data, key=private_key).decode(CHARSETS[0])

        return token

    @staticmethod
    def detokenize(token):
        """Decodes the passed JWT token.

        Args:
            token (str): JWT token

        Returns:
            Dict: A dictionary of the decoded data.

        """

        public_key = getenv('JWT_PUBLIC_KEY')

        try:
            decoded_token = jwt.decode(token, public_key) if token else None

            dt = date_time.time().timestamp()

            now = int(round(dt))

            if not decoded_token:
                raises('No token was provided', 400)

            if decoded_token and decoded_token['exp'] < now:
                raises(MESSAGES['EXPIRED_TOKEN'], 403)

            return decoded_token

        except DecodeError:
            raises('There was a problem decoding the provided token', 400)
