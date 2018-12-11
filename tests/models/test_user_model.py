"""Test the user model"""

# models
from api.models.user import User

# schemas
from api.schemas.user_schema import UserSchema

# mocks
from ..mocks.user_mock_data import NEW_USER


class TestUserModel:
    """Test for User model"""

    def test_save(self, init_db):

        """Test the model can save data to the database.

        Args:
            init_db (func): Database instance

        Returns:
            None

        """

        user = User(**NEW_USER).save()

        assert user.first_name == NEW_USER['first_name']
        assert user.last_name == NEW_USER['last_name']
        assert user.email == NEW_USER['email']

    def test_get(self, create_new_user):

        """Test that we can get data from the model.

        Args:
            create_new_user (func): Creates new user to the database.

        Returns:
            None

        """

        schema = UserSchema(many=True)
        user = schema.dump(User.query_()).data[0]

        assert user['firstName'] == NEW_USER['first_name']
        assert user['lastName'] == NEW_USER['last_name']
        assert user['email'] == NEW_USER['email']

    def test_get_with_repr(self, create_new_user):

        """Test the model class methods.

        Args:
            create_new_user (func): Creates new user to the database.

        Returns:
            None

        """

        user_instance = create_new_user

        user_details = user_instance.query.first()

        user_data_string = '<User {}>'.format(user_instance.email)

        assert str(user_details) == user_data_string








