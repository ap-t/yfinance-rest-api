# yfinance REST API

yfinance REST API is a REST API built in Python using the Flask framework. yfinance REST API is an extesion of the yfinance project hosted at https://github.com/ranaroussi/yfinance

## Getting Started

Install and run the app
```sh
cd /path/to/yfinance-rest-api
pip install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development
export MONGO_URL=<YOUR_MONGO_CONNECTION_URL>
export NEWS_API_KEY<YOUR_NEWS_API_KEY>
flask run
```

## Usage

| Name                  | HTTP Verb  | API Endpoint                                                     | Purpose                                 |
| --------------------- | ---------- | ---------------------------------------------------------------- | --------------------------------------- |
| Ping                  | GET        | /api/v1/system/ping                                              | Check if API is alive                   |
| Tickers               | GET        | /api/v1/finance/stocks/tickers                                   | Get list of tickers                     |
| Search                | GET        | /api/v1/finance/stocks/search?q=A&limit=25                       | Search for stocks by ticker             |
| Most Popular          | GET        | /api/v1/finance/stocks/most-popular                              |  Get a list of the most popular stocks  |
| Fast Moving           | GET        | /api/v1/finance/stocks/fast-moving?sort=percentage.asc&limit=100 | Get a list of the fastest moving stocks |
| Info                  | GET        | /api/v1/finance/stocks/info?ticker=F                             | Get stock info                          |
| Historical            | GET        | /api/v1/finance/stocks/historical?ticker=DIS&period=5d           | Get stock historical market data        |
| Dividends             | GET        | /api/v1/finance/stocks/dividends?ticker=MSFT                     | Get stock dividends                     |
| Splits                | GET        | /api/v1/finance/stocks/splits?ticker=FB                          | Get stock splits                        |
| Financials            | GET        | /api/v1/finance/stocks/financials?ticker=TSLA&term=1y            | Get stock financials                    |
| Major Holders         | GET        | /api/v1/finance/stocks/major-holders?ticker=JNJ                  | Get stock major holders                 |
| Institutional Holders | GET        | /api/v1/finance/stocks/institutional-holders?ticker=V            | Get stock institutional holders         |
| Balance Sheet         | GET        | /api/v1/finance/stocks/balance-sheet?ticker=AAPL&term=quarter    | Get stock balance sheet                 |
| Cashflow              | GET        | /api/v1/finance/stocks/cashflow?ticker=GOOG&term=quarter         | Get stock cashflow                      |
| Earnings              | GET        | /api/v1/finance/stocks/earnings?ticker=AMZN&term=quarter         | Get stock earnings                      |
| Sustainability        | GET        | /api/v1/finance/stocks/sustainability?ticker=WMT                 | Get stock sustainability                |
| Recommendations       | GET        | /api/v1/finance/stocks/recommendations?ticker=BAC                | Get stock recommendations               | 
| Calendar              | GET        | /api/v1/finance/stocks/calendar?ticker=MA                        | Get stock calendar                      |
| ISIN                  | GET        | /api/v1/finance/stocks/isin?ticker=HD                            | Get stock isin                          |
| Options Expirations   | GET        | /api/v1/finance/stocks/options-expirations?ticker=NKE            | Get stock options expirations           |
| Calls                 | GET        | /api/v1/finance/stocks/calls?ticker=CRM&date=2021-08-24          | Get stock calls                         | 
| Puts                  | GET        | /api/v1/finance/stocks/puts?ticker=NFLX&date=2021-08-25          | Get stock puts                          |
| News Everything       | GET        | /api/v1/finance/news?q=$MSFT                                     | Search millions of articles             |

## Built With

* [Flask](https://flask.palletsprojects.com)
* [PyMongo](https://pymongo.readthedocs.io)
* [yfinance](https://github.com/ranaroussi/yfinance)
* [News API](https://newsapi.org/)

## License

This project is licensed under the MIT license.