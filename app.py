from flask import Flask
from flask_cors import CORS
from yfinancerestapi.home.routes import home
from yfinancerestapi.system.routes import system_api
from yfinancerestapi.finance.stocks.routes import stocks_api
from yfinancerestapi.finance.news.routes import news_api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(system_api, url_prefix='/api/v1/system')
    app.register_blueprint(stocks_api, url_prefix='/api/v1/finance/stocks')
    app.register_blueprint(news_api, url_prefix='/api/v1/finance/news')

    return app

app = create_app()
if __name__ == "__main__":
    app.run()