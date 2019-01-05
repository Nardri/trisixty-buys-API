"""Tests for the encryption class"""

# third party imports
import pytest

# utilities
from api.utilities.encryption import Encryption
from api.utilities.validations.custom_validations_error import \
    (ValidationError as CustomError)

# mocks
from ..mocks.user_mock_data import USER_DATA, DECODED_TOKEN


class TestEncryptionClass:
    """Tests encryption class"""

    def test_password_hash_succeeds(self):
        """Test that passwords are hashed"""

    hashed_password = Encryption.hash('password123')

    assert type(hashed_password) == str
    assert len(hashed_password) == 192

    def test_password_verify_succeeds(self):
        """Test that the password verify works"""

        hashed_password = Encryption.hash('password123')

        is_verify = Encryption.verify(hashed_password, 'password123')

        assert type(hashed_password) == str
        assert is_verify

    def test_password_verify_fails(self):
        """Test that the password verify fails when a wrong
        password is provided"""

        hashed_password = Encryption.hash('password123')

        is_verify = Encryption.verify(hashed_password, 'password1234')

        assert type(hashed_password) == str
        assert not is_verify

    def test_tokenize_succeeds(self):
        """Test token generation"""

        token = Encryption.tokenize(USER_DATA, subject='Testing', minutes=10)

        assert type(token) == str

    def test_detokenize_succeeds(self):
        """Test token decoding"""

        token = Encryption.tokenize(USER_DATA, subject='Testing', minutes=10)

        decoded_token = Encryption.detokenize(token)

        assert decoded_token['data'] == DECODED_TOKEN['data']
        assert decoded_token['aud'] == DECODED_TOKEN['aud']
        assert decoded_token['iss'] == DECODED_TOKEN['iss']
        assert decoded_token['sub'] == DECODED_TOKEN['sub']

    def test_detokenize_with_no_token_fails(self):
        """Test token decoding with no token"""

        with pytest.raises(CustomError) as e_info:
            Encryption.detokenize(None)

    def test_detokenize_with_expired_token_fails(self):
        """Test token decoding with no token"""

        with pytest.raises(CustomError) as e_info:
            token = Encryption.tokenize(
                USER_DATA, subject='Testing', minutes=-10)
            Encryption.detokenize(token)
