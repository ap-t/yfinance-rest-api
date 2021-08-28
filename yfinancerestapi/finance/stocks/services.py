import csv
import threading
import logging
import pandas as pd
import yfinance as yf
import yfinancerestapi.common.helpers as helpers
import yfinancerestapi.finance.services as finance_services
from datetime import date
from pymongo import MongoClient
from pprint import pprint

STOCK_PROJECTION = { '_id': False , 'fastMoving': False }

def init():
    db = finance_services.get_db()
    db.stocks.create_index('symbol')

def rebuild_collection():
    def drop_collection(db):
        # Drop stocks collection
        db.stocks.drop()
    
    def create_documents(db):
        def format_security_name(name):
            if not isinstance(name, str): return name

            pieces = name.split('Corporation')
            if (len(pieces) > 1): return pieces[0]

            pieces = name.split(',')
            if (len(pieces) > 1): return pieces[0]

            pieces = name.split('Inc')
            if (len(pieces) > 1): return pieces[0]

            pieces = name.split('Common Stock')
            if (len(pieces) > 1): return pieces[0]

            pieces = name.split('Group Holding')
            return pieces[0]

        def insert_document(stock):
            #Step 3: Insert business object directly into MongoDB via isnert_one
            result=db.stocks.insert_one(stock)

            #Step 4: Print to the console the ObjectID of the new document
            print('Created as {0}'.format(result.inserted_id))

        def create_document(columns, values):
            stock = {}
            for i, column in enumerate(columns):
                stock[helpers.to_camel_case(column)] = values[i]
            
            security_name = stock.get('securityName')
            stock['name'] = format_security_name(security_name) if security_name else  ''
            return stock

        def parse_line(label, line):
            if not (isinstance(label, str) and isinstance(line, str)): 
                return
            
            columns = label.split('|')
            values = line.split('|')
            if (len(columns) == len(values)): insert_document(create_document(columns, values))

        def for_each_line(file_path, callback):
            df = pd.read_fwf(file_path)

            for label, content in df.iterrows():
                for label, line in content.items():
                    callback(label, line)
        
        for_each_line('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt', parse_line)

    
    db = finance_services.get_db()
    drop_collection(db)
    create_documents(db)
    #supplement_documents()  

def reset_analysis():
    db = finance_services.get_db()
    reset_stocks_analysis(db)

def run_analysis():
    db = finance_services.get_db()
    analyze_stocks_collection(db)
        
def get_stocks(query=None, limit=None):
    def sort_startwith(val):
        symbol = val.get('symbol', '').lower()
        q = query if query else ''
        return not(symbol.startswith(q.lower()))

    db = finance_services.get_db()
    filter = { 'symbol': { '$regex': '.*'+query+'.*', '$options': '-i'} } if query else {}
    cursors = db.stocks.find(filter, STOCK_PROJECTION)
    stocks = list(cursors)
    stocks.sort(key = sort_startwith)

    if limit: stocks = stocks[:limit]

    return stocks

def get_stock(symbol=None):
    db = finance_services.get_db()
    
    cursors = db.stocks.find_one({'symbol': symbol}, STOCK_PROJECTION)

    return cursors

def get_tickers():
    tickers_list = []

    db = finance_services.get_db()
    cursors = db.stocks.find({})

    for document in cursors:
        tickers_list.append(document.get('symbol'))

    return tickers_list

def get_fast_movers():
    fast_movers_list = []

    db = finance_services.get_db()
    cursors = db.stocks.find({ 'fastMoving': { '$exists': True } })

    for document in cursors:
        fast_movers_dict = document.get('fastMoving')

        if not(fast_movers_dict): continue

        fast_movers_dict['name'] = document.get('name')
        fast_movers_dict['symbol'] = document.get('symbol')

        fast_movers_list.append(fast_movers_dict)
    
    return fast_movers_list

def calculate_fast_moving(symbol, period):
    # Get history
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)

    low = float(10000)
    high = float(0)

    #print(ticker.info)
    print(symbol)
    for day in df.itertuples(index=True, name='Pandas'):
        if day.Low < low:
            low = day.Low
        if high < day.High:
            high = day.High
    
    if low == float(0): return None
    
    deltapercent = 100 * (high - low)/low
    Open = helpers.lookup_fn(df, 0, "Open")

    # Some error handling
    if len(df >= 5):
        Close = helpers.lookup_fn(df, 4, "Close")
    else:
        Close = Open
    
    if (Open == 0):
        deltaprice = 0
    else:
        deltaprice = 100 * (Close - Open) / Open

    return { 'deltaPercent': deltapercent, 'deltaPrice': deltaprice, 'lastUpdated': date.today().isoformat(), 'close': Close }

def analyze_stock_document(document):
    previous_fast_moving = document.get('fastMoving')
    fast_moving = previous_fast_moving if previous_fast_moving else calculate_fast_moving(document.get('symbol'), '5d')

    return { 'fastMoving': fast_moving }

def start_stock_documents_analysis(documents):
    db = finance_services.get_db()
    for document in documents:
        analysis = analyze_stock_document(document)
        result = db.stocks.update_one({ '_id': document.get('_id') }, { '$set': analysis })

def analyze_stocks_collection(db):
    cursors = db.stocks.find({})

    i = 0
    thread_count = 0
    documents = []
    while i < cursors.count():
        documents.append(cursors[i])
        if (i+1) % 600 == 0 or i == (cursors.count()-1):
            thread_count = thread_count + 1
            logging.info('Thread ' + str(thread_count) + ' Started')
            analysis_thread = threading.Thread(target=start_stock_documents_analysis, args=(documents,))
            analysis_thread.start()
            documents = []
        i += 1

def build_supplementary_info(symbol):
    ticker = yf.Ticker(symbol)
    print(symbol)
    
    # Get stock info
    all_info = ticker.info
    shortName = all_info.get('shortName') if all_info is not None else ''
    additional_info = { 'shortName': shortName }
    return additional_info

def get_supplementary_info(document):
    previous_additional_info = document.get('additionalInfo')
    additional_info = previous_additional_info if previous_additional_info else build_supplementary_info(document.get('symbol'))
    return { 'additionalInfo': additional_info }

def start_stock_documents_supplment(documents):
    db = finance_services.get_db()
    for document in documents:
        info = get_supplementary_info(document)

        # Get stock info
        db.stocks.update_one({ '_id': document.get('_id') }, { '$set': info })

def supplement_documents():
    db = finance_services.get_db()
    cursors = db.stocks.find({})

    i = 0
    thread_count = 0
    documents = []
    while i < cursors.count():
        documents.append(cursors[i])
        if (i+1) % 600 == 0 or i == (cursors.count()-1):
            thread_count = thread_count + 1
            logging.info('Thread ' + str(thread_count) + ' Started')
            supplement_thread = threading.Thread(target=start_stock_documents_supplment, args=(documents,))
            supplement_thread.start()
            documents = []
        i += 1

def reset_stocks_analysis(db):
    db.stocks.update_many({}, { '$unset': { 'fastMoving': '' } })

init()