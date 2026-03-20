from flask import Blueprint, jsonify, make_response

api_bp = Blueprint('api', __name__, url_prefix='/api')

from . import jobs_api
from . import auth_api


@api_bp.errorhandler(Exception)
def api_handle_exception(error):
    return make_response(jsonify({
        'error': 'Internal Server Error',
        'message': str(error) if str(error) else 'An unexpected error occurred'
    }), 500)
