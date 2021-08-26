import yfinance as yf
import yfinancerestapi.common.helpers as helpers
import yfinancerestapi.finance.news.services as news_services
from flask import Blueprint, request, jsonify


news_api = Blueprint('news', __name__)

@news_api.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><p>The resource could not be found.</p>', 404

@news_api.route('/everything', methods=['GET'])
def everything():
    query_parameters = request.args
    query = query_parameters.get('q')
    
    return news_services.get_everything(query)