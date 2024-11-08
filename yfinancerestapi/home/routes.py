from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return render_template('index.html')