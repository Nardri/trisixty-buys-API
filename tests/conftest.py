"""Module for Pytest Configuration"""

# system imports
from os import getenv, environ

# third party imports
import pytest

# local import
from main import create_app

# models
from api.models.user import User
from api.models.db_config import db

# utilities
from api.utilities.encryption import Encryption

# mocks
from .mocks.user_mock_data import FIXTURE_NEW_USER, FIXTURE_NEW_USER_TWO

testing_env = 'testing'
environ['FLASK_ENV'] = testing_env
env = getenv('FLASK_ENV')


@pytest.fixture(scope='session')
def flask_app():
    """Create a flask application instance for Pytest.

    Returns:
        Object: Flask application object

    """

    # create an application instance
    _app = create_app(env)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    # yield the application context for making requests
    yield _app

    ctx.pop()


@pytest.fixture
def client(flask_app):
    """Setup client for making http requests, this will be run on every
    test function.

    Args:
        flask_app (func): Flask application instance

    Returns:
        Object: flask application client instance

    """

    # initialize the flask test_client from the flask application instance
    client = flask_app.test_client()

    yield client


@pytest.fixture
def init_db():
    """Fixture to initialize the database"""

    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='session')
def headers():
    """header data.

    Returns:
        dict: The header dictionary

    """

    return {'Content-Type': 'application/json', 'Authorization': 'Bearer iiu'}


@pytest.fixture
def new_user(init_db):
    """Creates a new user.

    Args:
        init_db (func): Initialize the database

    Returns:
        Instance: user instance.

    """

    user_instance = User(**FIXTURE_NEW_USER)

    return user_instance


@pytest.fixture
def new_user_two(init_db):
    """Creates a new user.

    Args:
        init_db (func): Initialize the database

    Returns:
        Instance: user instance.

    """

    user_instance = User(**FIXTURE_NEW_USER_TWO)

    return user_instance


@pytest.fixture
def generate_token():
    """Generate JWT Token for tests."""

    def _encrypt(payload, subject, **kwargs):
        return Encryption.tokenize(payload, subject=subject, **kwargs)

    return _encrypt
