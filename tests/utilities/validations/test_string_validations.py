"""Test for the string validation"""

# third party imports
import pytest
from marshmallow.exceptions import ValidationError

# utilities
from api.utilities.validations.string_validations import validate_string
from api.utilities.constants import MESSAGES


class TestStringValidations:
    """Test for string validation"""

    def test_string_validation_succeeds(self):
        """Should return the data"""

        clean = validate_string('victor')
        assert clean == 'victor'

    def test_string_validation_fails(self):
        """Should raise a validation error when invalid data is provided"""

        with pytest.raises(ValidationError) as excinfo:
            validate_string('')

        assert str(excinfo.value) == MESSAGES['REQUIRED_FIELDS']

    def test_string_validation_with_two_characters_fails(self):
        """Should raise a validation error when data less than three
         is provided"""

        with pytest.raises(ValidationError) as excinfo:
            validate_string('vi')

        assert str(excinfo.value) == MESSAGES['REQUIRED_FIELDS']
