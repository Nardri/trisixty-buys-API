"""Module for password reset"""

# third party imports
from flask_restplus import Resource
from flask import request

# local imports
from main import api

# models
from api.models.user import User

# schemas
from api.schemas.user_schema import UserSchema

# utilities
from api.utilities.constants import MESSAGES
from api.utilities.helpers.create_link import generate_link
from api.utilities.encryption import Encryption

# services
from api.services.email import MailGun
from api.services.email_templates import email_verification, style


@api.route('/user/password/reset')
class PasswordResetResource(Resource):
    """Resource for password reset"""

    def post(self):
        """Post request to reset password"""

        # instantiate the user schema
        schema = UserSchema(only=['id', 'email', 'verified'])

        # get the request data in json format
        request_json = request.get_json()

        # serialize and find the user data in the database
        user = schema.load_into_schema(request_json, partial=True)
        found_user = User.query_(email=user['email'], deleted=False).first()

        # throw an error if not found
        if not found_user:
            return {'status': 'error', 'message': MESSAGES['NOT_FOUND']}, 404

        # throw an error if user is found but not yet verified
        if found_user and not found_user.verified:
            return {
                'status': 'error',
                'message': MESSAGES['NOT_VERIFIED']
            }, 401

        else:
            # generate a reset token and link
            link, user['password_reset'] = generate_link(
                request, user, type='password_reset')

            # send the link to the email provided
            MailGun.with_api(
                found_user.email,
                email_verification.format(style, link, 'Reset your password'),
                'Password Reset')

            # update the user data
            found_user.update_(**user)

            # return success messages
            return {
                'status': 'success',
                'message': MESSAGES['RESET_LINK'],
            }, 200

    def patch(self):
        """patch request to reset the user's password"""

        # instantiate the user schema
        user_schema = UserSchema()

        # get the verification_token from the request params
        reset_token = request.args.get('token')

        # get the request data in json format
        request_json = request.get_json()

        # check if the token is valid
        # serialize the request data and
        # look for the token in the database
        Encryption.detokenize(reset_token)
        user_details = user_schema.load_into_schema(request_json, partial=True)
        found_token = User.query_(password_reset=reset_token).first()

        # throw an error if not found
        if not found_token:
            return {
                'status': 'error',
                'message': MESSAGES['RESET_LINK_RESEND']
            }, 404

        else:
            # set the password reset column to none
            user_details['password_reset'] = None

            # hash the new password and update the password
            user_details['password'] = Encryption.hash(
                user_details['password'])
            found_token.update_(**user_details)

            return {
                'status':
                'success',
                'message':
                MESSAGES['PROCEED_TO_LOGIN'].format(
                    'Your password has been changed')
            }, 200
