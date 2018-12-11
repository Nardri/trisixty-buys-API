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
        """Get request for users"""

        # instantiate the user schema
        user_schema = UserSchema()

        # get the request in json format
        request_json = request.get_json()

        # deserialize and validate the request
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

    def get(self):
        """get"""

        user_schema = UserSchema(many=True, exclude=EXCLUDES)

        users_object = User.query_()

        obj = user_schema.dump(users_object).data

        return {
            'data': obj
        }, 200
