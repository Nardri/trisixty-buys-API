"""Module to test the create link method"""

# utilities
from api.utilities.helpers.create_link import generate_link
from api.utilities.encryption import Encryption

# mocks
from tests.mocks.general_mocks import Request
from tests.mocks.user_mock_data import USER_DATA


class TestCreateLink:
    """Class to test the create link methods"""

    def test_generate_link_for_email_verification_succeeds(self):
        """Test the generate link method"""

        data = {'email': USER_DATA['email']}

        actual_behaviour = generate_link(
            Request, data, type='email_verification')
        decoded_token = Encryption.detokenize(actual_behaviour[1])

        assert isinstance(actual_behaviour, tuple)
        assert len(actual_behaviour) == 2
        assert decoded_token['sub'] == 'email_verification'

    def test_generate_link_for_password_reset_succeeds(self):
        """Test the generate link method"""

        data = {'email': USER_DATA['email']}

        actual_behaviour = generate_link(Request, data, type='password_reset')
        decoded_token = Encryption.detokenize(actual_behaviour[1])

        assert isinstance(actual_behaviour, tuple)
        assert len(actual_behaviour) == 2
        assert decoded_token['sub'] == 'password_reset'
