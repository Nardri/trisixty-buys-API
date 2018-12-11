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

# mocks
from .mocks.user_mock_data import NEW_USER


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


@pytest.fixture(scope='function')
def client(flask_app):
    """Setup client for making http requests, this will be run on every test.

    Args:
        flask_app (func): Flask application instance

    Returns:
        Object: flask application client instance

    """

    # initialize the flask test_client from the flask application instance
    client = flask_app.test_client()

    yield client


@pytest.fixture(scope='module')
def init_db(flask_app):
    """Fixture to initialize the database"""

    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def headers():
    """header data.

    Returns:
        dict: The header dictionary

    """

    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer iiu'
    }


@pytest.fixture(scope='module')
def create_new_user(init_db):
    """Creates a new user.

    Args:
        init_db (func): Initialize the database

    Returns:
        Instance: user instance.

    """

    user_instance = User(**NEW_USER)

    return user_instance
