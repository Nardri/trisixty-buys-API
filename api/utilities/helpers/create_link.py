"""Module for generating links"""

from api.utilities.encryption import Encryption
from os import getenv

FRONT_URL = getenv('REACT_URL')


def email_verification_link(url_root, token):
    """Generates email verification link.

    Args:
         url_root (str): root url
        token (str): Token to be attached to the url

    Returns:
        tuple: the verification link, token

    """

    link = url_root + f'api/v1/user/activate?token={token}'

    return link, token


def password_reset_link(url_root, token):
    """Generates password reset link.

    Args:
        url_root (str): root url
        token (str): Token to be attached to the url

    Returns:
        tuple: the verification link, token

    """

    link = FRONT_URL + f'/password/reset/{token}'

    return link, token


def generate_link(request, data, type='email_verification'):
    """Generate the link based on the type provided.

    Args:
        request (object): Request object
        data (dict): User data
        type (str): The type of token to be generated
            Examples:
                1. email_verification
                2. password_reset

    Returns:
        Tuple: A link and the token.

    """

    # gets the root url
    url_root = request.url_root

    token_payload = {
        'email': data['email'],
    }

    # generates a token
    token = Encryption.tokenize(token_payload, subject=type, minutes=10)

    # maps the methods with link type
    mapper = {
        'password_reset': password_reset_link(url_root, token),
        'email_verification': email_verification_link(url_root, token)
    }

    return mapper[type]
