"""Decorator for url param validator"""

# system imports
from functools import wraps

# utilities
from api.utilities.validations.validations import EMAIL_REGEX
from api.utilities.helpers.errors import raises
from api.utilities.constants import MESSAGES


def validate_email(func):
    """Decorator function to Validate the email passed in the url"""

    @wraps(func)
    def decorated_func(*args, **kwargs):
        """Function with decorated function mutations."""

        email = kwargs.get('email')
        if email and len(email) < 3 or not EMAIL_REGEX.match(email):
            raises(MESSAGES['INVALID_EMAIL'], 400)

        return func(*args, **kwargs)

    return decorated_func
