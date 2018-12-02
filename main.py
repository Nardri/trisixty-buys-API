"""Application main file"""

# Third party library
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restplus import Api

# local import
from config import app_config
from api import api_blueprint
from api.models import db, migrate


# initialize RestPlus with the API blueprint
api = Api(api_blueprint)


def create_app(env):
    """Create the flask application instance
    The Application factory

    Args:
        env (string): The environment

    Returns:
        Object: Flask instance

    """

    # initialization the application
    app = Flask(__name__)
    app.config.from_object(app_config[env])

    # cross origin initialization
    CORS(app)

    # register the api blueprint
    app.register_blueprint(api_blueprint)

    # import all models
    from api.models import User

    # import views
    import api.views

    # binding the database to the app
    db.init_app(app)

    # binding the migrate and db to the app instance
    migrate.init_app(app, db)

    # home route
    @app.route('/', methods=['GET'])
    def index():
        """Index route for the API"""
        return jsonify(
                status='success',
                data='Biabs version 1.0',
        )

    return app
