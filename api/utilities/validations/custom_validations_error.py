"""Module for Validation error and error handler"""

from flask import Blueprint

error_handler_blueprint = Blueprint('validations', __name__)


class ValidationError(Exception):
    """Base Validation class for handling validation errors"""

    def __init__(self, error, status_code=None):
        Exception.__init__(self)
        self.status_code = 400
        self.error = error
        self.error['status'] = 'error'
        self.error['message'] = error['message']

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Returns the error dict

        Returns:
            Dict: Errors and message

        """

        return self.error
