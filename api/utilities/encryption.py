"""Module for all encryption"""

# standard imports
import hashlib
import binascii
from os import urandom
from uuid import uuid4
from datetime import datetime, timedelta

# third party imports
from authlib.specs.rfc7519 import jwt

# local imports
from api.utilities.constants import CHARSETS


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

        # get the first 64 characters from the stored password, this is the salt
        salt = stored_password[:64]

        # get the remaining characters from the 64th index,
        # this is the stored password
        stored_password = stored_password[64:]

        # hash the provided password
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode(CHARSETS[0]),
                                      salt.encode(CHARSETS[1]),
                                      100000)
        # convert the hash to a hexadecimal and decode to ascii
        pwdhash = binascii.hexlify(pwdhash).decode(CHARSETS[1])

        # compares the hashed password with the stored hash
        return pwdhash == stored_password

    @staticmethod
    def tokenize(payload):
        """Generates a token for the given payload.

        Args:
            payload (dict): Payload

        Returns:
            String: JWT token

        """

        header = {
            'alg': 'RS256'
        }

        data = {
            "data": payload,
            "iat": datetime.now(),
            "exp": datetime.now() + timedelta(days=14),
            "aud": "Yard-it.com.ng",
            "iss": "Yard-it-API"
        }
        private_key = open('Jwt_key').read()

        token = jwt.encode(header=header, payload=data,
                           key=private_key).decode(CHARSETS[0])

        return token

    @staticmethod
    def detokenize(token):
        """Decodes the passed JWT token.

        Args:
            token (str): JWT token

        Returns:
            Dict: A dictionary of the decoded data.

        """

        public_key = open('Jwt_key.pub').read()

        decoded_token = jwt.decode(token, public_key)

        return decoded_token



