"""Configuration module"""

# default import
from os import getenv
from pathlib import Path  # python3 only

# Third party library
from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

defaultDB = 'postgresql://postgres:123456@localhost:5432/yardit'


class Config(object):
    """Base app configuration class"""

    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', default=defaultDB)


class Development(Config):
    """Configurations for development environment"""

    DEBUG = True


class Production(Config):
    """Configurations for production environment"""

    SQLALCHEMY_DATABASE_URI = getenv('PROD_DATABASE_URI')


class Testing(Config):
    """Configurations for testing environment"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URI')


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
