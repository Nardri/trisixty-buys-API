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
from api.utilities.constants import MESSAGES, EXCLUDES
from api.utilities.push_id import PushID
from api.utilities.helpers.format_data import format_user

# instantiating FireBase fancy id
push_id = PushID()


@api.route('/user/register')
class UserRegisterResource(Resource):
    """Resource for UserRegister"""

    def post(self):
        """Post request for user registration"""

        # instantiate the user schema
        user_schema = UserSchema()

        # get the request in json format
        request_json = request.get_json()

        # serialize and validate the request
        user_details = user_schema.load_into_schema(request_json, partial=True)
        user_details['first_name'] = user_details['first_name'].strip()
        user_details['last_name'] = user_details['last_name'].strip()

        # check if the user already exist
        found_user = User.query_(email=user_details['email']).first()
        if found_user:
            user = user_schema.dump(found_user).data
            return {
                'status': 'error',
                'message': MESSAGES['DUPLICATES'].format(user['email'])
            }, 409

        # hash password
        user_details['password'] = Encryption.hash(user_details['password'])

        # generate a random unique username
        user_details['username'] = push_id.next_id()[8:]

        # save to database and serialize the returned user data
        saved_user = User(**user_details).save()
        user = user_schema.dump(saved_user).data

        # format and generate a JWT token.
        formatted_data = format_user(user)
        token = Encryption.tokenize(formatted_data)

        return {
            'status': 'success',
            'message': MESSAGES['CREATED'].format('User'),
            'data': {
                'token': token,
            }
        }, 201


@api.route('/user/login')
class LoginResource(Resource):
    """Resource for user login"""

    def post(self):
        """Post request for user login"""

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

        # if password did not match throw and error
        if not is_match:
            return {
                'status': 'error',
                'message': MESSAGES['UNAUTHORIZED']
            }, 401

        else:

            # format the data and generate a JWT token.
            formatted_data = format_user(user)
            token = Encryption.tokenize(formatted_data)

            return {
                'status': 'success',
                'message': MESSAGES['LOGIN'],
                'data': {
                    'token': token,
                }
            }, 200
