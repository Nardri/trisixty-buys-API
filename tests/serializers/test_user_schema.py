"""Test for the user schema"""

# third party imports
import pytest

# Utilities
from api.utilities.validations.custom_validations_error import ValidationError
from api.utilities.constants import EXCLUDES

# schema
from api.schemas.user_schema import UserSchema

# mocks
from ..mocks.user_mock_data import USER_DATA, FIXTURE_NEW_USER


class TestUserSchema:
    """Test user schema"""

    def test_user_schema_deserialization_succeeds(self):
        """Test the user data deserialization."""

        schema = UserSchema()

        user = schema.load_into_schema(USER_DATA, partial=True)

        user_deserialized = {
            'last_name': USER_DATA['lastname'],
            'password': USER_DATA['password'],
            'email': USER_DATA['email'],
            'first_name': USER_DATA['firstname']
        }

        assert user == user_deserialized

    def test_user_schema_raises_exception(self):
        """Test the user schema validation exception."""

        schema = UserSchema()
        with pytest.raises(ValidationError):
            schema.load_into_schema(USER_DATA)

    def test_user_schema_serialization_succeeds(self, new_user):
        """Test the user data deserialization.

        Args:
            new_user (func): Creates new user to the database.

        Returns:
            None

        """

        schema = UserSchema(exclude=EXCLUDES)

        user = new_user.save()

        user_data_object = schema.dump(user).data

        assert FIXTURE_NEW_USER['first_name'] == user_data_object['firstName']
        assert FIXTURE_NEW_USER['last_name'] == user_data_object['lastName']
        assert FIXTURE_NEW_USER['email'] == user_data_object['email']
