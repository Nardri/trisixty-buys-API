"""Helper module for formatting data"""


def format_user(user):
    """A helper method to format the user data for token generation.

    Args:
        user (dict): User dictionary

    Returns:
        Object: Formatted user dictionary

    """

    return {
        'id': user['id'],
        'firstname': user['firstName'],
        'lastName': user['lastName'],
        'username': user['username'],
        'email': user['email']
    }
