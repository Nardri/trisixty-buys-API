"""Blue print module"""

from flask import Blueprint

# instantiating the blue print
api_blueprint = Blueprint('biabs_api', __name__, url_prefix='/api/v1')
