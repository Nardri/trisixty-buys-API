"""Module for Pytest Configuration"""

from os import getenv, environ
import pytest
from main import create_app


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


@pytest.fixture(scope='module')
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

