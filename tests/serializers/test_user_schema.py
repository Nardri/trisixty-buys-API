"""Test for the user schema"""

# third party imports
import pytest

# Utilities
from api.utilities.validations.custom_validations import ValidationError
from api.utilities.constants import EXCLUDES

# schema
from api.schemas.user_schema import UserSchema

# mocks
from ..mocks.user_mock_data import USER, NEW_USER


class TestUserSchema:
    """Test user schema"""

    def test_user_schema_deserialization_succeeds(self):
        """Test the user data deserialization."""

        schema = UserSchema()

        user = schema.load_into_schema(USER, partial=True)

        user_deserialized = {
            'last_name': USER['lastname'],
            'password': USER['password'],
            'email': USER['email'],
            'first_name': USER['firstname']
        }

        assert user == user_deserialized

    def test_user_schema_raises_exception(self):
        """Test the user schema validation exception."""

        schema = UserSchema()
        with pytest.raises(ValidationError):
            schema.load_into_schema(USER)

    def test_user_schema_serialization_succeeds(self, create_new_user):
        """Test the user data deserialization.

        Args:
            create_new_user:

        Returns:
            None

        """

        schema = UserSchema(exclude=EXCLUDES)

        user = create_new_user.save()

        user_data_object = schema.dump(user).data

        assert NEW_USER['first_name'] == user_data_object['firstName']
        assert NEW_USER['last_name'] == user_data_object['lastName']
        assert NEW_USER['email'] == user_data_object['email']
