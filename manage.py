"""API entry module"""

from os import getenv
from main import create_app


# get the environment name
env = getenv('FLASK_ENV', default='production')
app = create_app(env)


if __name__ == '__main__':
    app.run()
