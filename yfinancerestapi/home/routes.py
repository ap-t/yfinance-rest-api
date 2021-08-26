from flask import Blueprint

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return '<h1>yFinance REST API</h1>'