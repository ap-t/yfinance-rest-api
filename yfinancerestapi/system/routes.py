from flask import Blueprint

system_api = Blueprint('system', __name__)

@system_api.route('/ping', methods=['GET'])
def index():
    return { 'status': 'ok' }