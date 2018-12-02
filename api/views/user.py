"""User module"""

# third party library
from flask_restplus import Resource

# local import
from main import api
from api.models.User import UserModel


@api.route('/user')
class UserResource(Resource):
    """Resource for user route"""

    def get(self):
        """Get request for users"""
        user = UserModel(username='Veeqtor', email='nwokeochavictor@gmail.com')

        user.save()

        print(user)
        return {
            'data': "Lower"
        }
