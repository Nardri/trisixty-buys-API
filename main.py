"""Application main file"""

# Third party library
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restplus import Api

# local import
from config import app_config
from api import api_blueprint
from api.models.db_config import (db, migrate)
from api.utilities.validations.custom_validations import (
    ValidationError, error_handler_blueprint)

# initialize RestPlus with the API blueprint
api = Api(api_blueprint)


def register_blueprints(application):
    """Registers all blueprints

    Args:
        application (obj): Application instance

    Returns:
        None

    """

    application.register_blueprint(error_handler_blueprint)
    application.register_blueprint(api_blueprint)


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
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[env])

    # cross origin initialization
    CORS(app)

    # register the blueprint
    register_blueprints(app)

    # import all models
    import api.models

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
            data='Yard-it version 1.0',
        )

    return app


@api.errorhandler(ValidationError)
@error_handler_blueprint.errorhandler(ValidationError)
def handle_exceptions(err):
    """Error handler for when validation error"""

    return err.to_dict(), err.status_code
