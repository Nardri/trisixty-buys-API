"""User module"""

# third party library
from flask_restplus import Resource
from flask import request

# local import
from main import api

# models
from api.models.user import User

# schemas
from api.schemas.user_schema import UserSchema

# Utilities
from api.utilities.encryption import Encryption
from api.utilities.constants import MESSAGES
from api.utilities.push_id import PushID
from api.utilities.helpers.format_data import format_user
from api.utilities.helpers.create_link import generate_link
from api.middlewares.url_params_validator import validate_email

# services
from api.services.email import MailGun
from api.services.email_templates import email_verification, style

# instantiating FireBase fancy id and mailGun
push_id = PushID()


@api.route('/user/register')
class UserRegisterResource(Resource):
    """Resource for UserRegister"""

    def post(self):
        """Post request for user registration"""

        # instantiate the user schema
        user_schema = UserSchema()

        # get the request data in json format
        request_json = request.get_json()

        # serialize and validate the request
        user_details = user_schema.load_into_schema(request_json, partial=True)
        user_details['first_name'] = user_details['first_name'].strip()
        user_details['last_name'] = user_details['last_name'].strip()

        # check if the user already exist
        found_user = User.query_(email=user_details['email']).first()
        if found_user:
            return {
                'status': 'error',
                'message': MESSAGES['DUPLICATES'].format(found_user.email)
            }, 409

        # hash password
        user_details['password'] = Encryption.hash(user_details['password'])

        # generate a random unique username
        user_details['username'] = push_id.next_id()[8:]

        link, user_details['token'] = generate_link(request, user_details)

        # save to database and serialize the returned user data
        saved_user = User(**user_details).save()

        # if the save was successful, send out the verification email and
        # return a success message.
        if saved_user:
            MailGun.with_api(
                saved_user.email,
                email_verification.format(style, link, 'Verification Link'),
                'Email verification')

            return {
                'status': 'success',
                'message': MESSAGES['REGISTER'],
            }, 201


@api.route('/user/activate')
class TokenVerifyResource(Resource):
    """Resource to verify email"""

    def get(self):
        """Get request to verify the user's emails"""

        # get the verification_token from the request params
        verification_token = request.args.get('token')

        # check if the token is valid and look for the token in the database
        Encryption.detokenize(verification_token)
        found_token = User.query_(token=verification_token).first()

        # throw an error if not found else update and return a success message
        if not found_token:
            return {'status': 'error', 'message': MESSAGES['VERIFIED']}, 409

        else:
            found_token.update_(token=None, verified=True)

            return {
                'status':
                'success',
                'message':
                MESSAGES['PROCEED_TO_LOGIN'].format(
                    'Your account has been successfully verified'),
            }, 200


@api.route('/user/activate/<string:email>/resend')
class TokenResendResource(Resource):
    """Resource to resend verify email"""

    @validate_email
    def get(self, email):
        """Get request to resend the user's verification link.

        Args:
            email (str): The email to send the verification link to

        Returns:
            JSON: The json response

        """

        # initialize the schema
        user_schema = UserSchema(only=['token', 'email', 'verified'])

        # find the email
        found_user = User.query_(email=email).first()

        # throw an error if not found
        if not found_user:
            return {'status': 'error', 'message': MESSAGES['NOT_FOUND']}, 404

        # throw an error if the user is not verified
        if found_user.verified:
            return {'status': 'error', 'message': MESSAGES['VERIFIED']}, 409

        # deserialize the user data and generate the verification link
        user_details = user_schema.dump(found_user).data
        link, user_details['token'] = generate_link(request, user_details)

        # updates the user in the database
        found_user.update_(**user_details)

        # sends out the email verification link
        MailGun.with_api(
            found_user.email,
            email_verification.format(style, link, 'Click to Verify'),
            'Email verification')

        # return a success message upon completion
        return {
            'status': 'success',
            'message': MESSAGES['RESEND_EMAIL'],
        }, 200


@api.route('/user/login')
class LoginResource(Resource):
    """Resource for user login"""

    def post(self):
        """Post request for user login"""

        # initialize the schema
        schema = UserSchema()

        # get the request details as json
        request_json = request.get_json()

        # serialize and find the user data in the database
        user_details = schema.load_into_schema(request_json, partial=True)
        found_user = User.query_(email=user_details['email'], deleted=False)\
            .first()

        # throw an error if not found
        if not found_user:
            return {'status': 'error', 'message': MESSAGES['NOT_FOUND']}, 404

        # deserialize the user data if found, and verify the password
        user = schema.dump(found_user).data
        is_match = Encryption.verify(user['password'],
                                     user_details['password'])

        # if password did not match throw an error
        if not is_match:
            return {
                'status': 'error',
                'message': MESSAGES['UNAUTHORIZED']
            }, 401

        else:

            # format the data and generate a JWT token.
            formatted_data = format_user(user)
            token = Encryption.tokenize(
                formatted_data, subject='User_Login', days=14)

            return {
                'status': 'success',
                'message': MESSAGES['LOGIN'],
                'data': {
                    'token': token,
                }
            }, 200
