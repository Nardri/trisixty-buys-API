"""Test the user model"""

# models
from api.models.user import User

# schemas
from api.schemas.user_schema import UserSchema

# mocks
from ..mocks.user_mock_data import FIXTURE_NEW_USER


class TestUserModel:
    """Test for User model"""

    def test_save(self, init_db):
        """Test the model can save data to the database.

        Args:
            init_db (func): Database instance

        Returns:
            None

        """

        user = User(**FIXTURE_NEW_USER).save()

        assert user.first_name == FIXTURE_NEW_USER['first_name']
        assert user.last_name == FIXTURE_NEW_USER['last_name']
        assert user.email == FIXTURE_NEW_USER['email']

    def test_get(self, new_user):
        """Test that we can get data from the model.

        Args:
            new_user (func): Creates new user to the database.

        Returns:
            None

        """

        new_user.save()

        schema = UserSchema(many=True)
        user = schema.dump(User.query_()).data[0]

        assert user['firstName'] == FIXTURE_NEW_USER['first_name']
        assert user['lastName'] == FIXTURE_NEW_USER['last_name']
        assert user['email'] == FIXTURE_NEW_USER['email']

    def test_get_with_repr(self, new_user):
        """Test the model class methods.

        Args:
            new_user (func): Creates new user to the database.

        Returns:
            None

        """

        user_instance = new_user.save()

        user_details = user_instance.query.first()

        user_data_string = '<User {}>'.format(user_instance.email)

        assert str(user_details) == user_data_string
