import yfinance as yf
import yfinancerestapi.common.helpers as helpers
import yfinancerestapi.finance.stocks.services as services
from flask import Blueprint, request, jsonify

stocks_api = Blueprint('stocks', __name__)

@stocks_api.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><p>The resource could not be found.</p>', 404

@stocks_api.route('/tickers', methods=['GET'])
def tickers():
    list_of_tickers = services.get_tickers()
    #_list_of_tickers = gt.get_tickers(NYSE=False, NASDAQ=False, AMEX=True)
    return helpers.parse_json(list_of_tickers)

@stocks_api.route('/search', methods=['GET'])
def search():
    
    query_parameters = request.args
    query = query_parameters.get('q')
    limit = query_parameters.get('limit')

    if limit: limit = int(limit) if limit.isnumeric() else None 

    list_of_stocks = services.get_stocks(query, limit)

    return helpers.parse_json(list_of_stocks)

@stocks_api.route('/most-popular', methods=['GET'])
def most_popular():
    list_of_stocks = []
    popular = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'FB', 'BABA', 'V', 'JNJ', 'WMT'] #FIXME

    for symbol in popular:
        stock = services.get_stock(symbol)

        if stock is not None:
            list_of_stocks.append(stock)

    return helpers.parse_json(list_of_stocks)

@stocks_api.route('fast-moving', methods=['GET'])
def fast_moving():
    def sort_delta_percentage(val):
        return val['deltaPercent']

    def sort_delta_price(val):
        return val['deltaPrice']

    def sort_close_price(val):
        return val['close']

    query_parameters = request.args
    sort = query_parameters.get('sort')
    limit = query_parameters.get('limit')

    if limit: limit = int(limit) if limit.isnumeric() else None 

    movementlist = services.get_fast_movers()

    if sort:
        occs = sort.split('.')
        if occs[0] == 'price' or occs[0] == 'percentage' or occs[0] == 'close':
            sort_by = occs[0]
            order_by = 'asc'
            if len(occs) == 2 and (occs[1] == 'desc' or occs[1] == 'asc'):
                order_by = occs[1]
            
            is_asc = order_by == 'asc'

            if sort_by == 'percentage': sort_fn = sort_delta_percentage
            elif sort_by == 'price': sort_fn = sort_delta_price
            elif sort_by == 'close': sort_fn = sort_close_price

        movementlist.sort(key = sort_fn, reverse = not(is_asc))
    
    if limit: movementlist = movementlist[:limit]
    
    return jsonify(movementlist)

@stocks_api.route('/info', methods=['GET'])
def info():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)
    
    # Get stock info
    info = ticker.info

    return jsonify(info)

@stocks_api.route('/historical', methods=['GET'])
def historical_market_data():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    period = query_parameters.get('period')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get historical market data
    df = ticker.history(period=period)

    # Make column headers to camel case
    df.columns = map(helpers.to_camel_case, df.columns)
    
    # Convert data frame to list
    history_list = helpers.dataframe_to_list_with_index(df)
    
    return jsonify(history_list)

@stocks_api.route('/dividends', methods=['GET'])
def dividends():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get dividends
    dividends = ticker.dividends

    # Convert series to list
    dividends_list = helpers.series_to_list_with_index(series=dividends)

    return jsonify(dividends_list)

@stocks_api.route('/splits', methods=['GET'])
def splits():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get splits
    splits = ticker.splits

    # Convert series to list
    splits_list = helpers.series_to_list_with_index(series=splits)
    
    return jsonify(splits_list)

@stocks_api.route('/financials', methods=['GET'])
def financials():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    term = query_parameters.get('term')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get financials
    df = ticker.quarterly_financials if term == 'quarter' else ticker.financials

    return df.to_json(orient='records')

#FIXME
@stocks_api.route('/major-holders', methods=['GET'])
def major_holders():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get major holders
    df = ticker.major_holders

    return df.to_json(orient='records')

@stocks_api.route('/institutional-holders', methods=['GET'])
def institutional_holders():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get institutional holders
    df = ticker.institutional_holders

    # Make column headers to camel case
    df.columns = map(helpers.to_camel_case, df.columns)

    return df.to_json(orient='records')

@stocks_api.route('/balance-sheet', methods=['GET'])
def balance_sheet():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    term = query_parameters.get('term')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get balance sheet
    df = ticker.quarterly_balance_sheet if term == 'quarter' else ticker.balance_sheet

    return df.to_json(orient='records')

@stocks_api.route('/cashflow', methods=['GET'])
def cashflow():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    term = query_parameters.get('term')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get cashflow
    df = ticker.quarterly_cashflow if term == 'quarter' else ticker.cashflow

    return df.to_json(orient='records')

@stocks_api.route('/earnings', methods=['GET'])
def earnings():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    term = query_parameters.get('term')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get earnings
    df = ticker.quarterly_earnings if term == 'quarter' else ticker.earnings

    return df.to_json(orient='records')

@stocks_api.route('/sustainability', methods=['GET'])
def sustainability():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get sustainability
    df = ticker.sustainability

    # Make column headers to camel case
    df.columns = map(helpers.to_camel_case, df.columns)

    return df.to_json(orient='index')

@stocks_api.route('/recommendations', methods=['GET'])
def recommendations():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get recommendations
    df = ticker.recommendations

    # Make column headers to camel case
    df.columns = map(helpers.to_camel_case, df.columns)

    return df.to_json(orient='records')

#FIXME
@stocks_api.route('/calendar', methods=['GET'])
def calendar():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    df = ticker.calendar

    return df.to_json(orient='records')

@stocks_api.route('/isin', methods=['GET'])
def isin():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get isin
    return jsonify({ 'isin': ticker.isin })

@stocks_api.route('/options-expirations', methods=['GET'])
def options():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')

    if not(symbol): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get options expirations
    t = ticker.options

    return jsonify(t)

@stocks_api.route('/calls', methods=['GET'])
def calls():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    date = query_parameters.get('date')

    if not(symbol) or not(date): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get option chain for specific expiration
    opt = ticker.option_chain(date=date)
    
    # Get option calls
    df = opt.calls

    return df.to_json(orient='records')

@stocks_api.route('/puts', methods=['GET'])
def puts():
    query_parameters = request.args
    symbol = query_parameters.get('ticker')
    date = query_parameters.get('date')

    if not(symbol) or not(date): return page_not_found(404)

    ticker = yf.Ticker(symbol)

    # Get option chain for specific expiration
    opt = ticker.option_chain(date=date)

    # Get option puts
    df = opt.puts

    return df.to_json(orient='records')