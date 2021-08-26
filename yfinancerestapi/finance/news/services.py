import yfinancerestapi.common.news as news_helpers
import yfinancerestapi.finance.services as finance_services
import datetime

def init():
    db = finance_services.get_db()
    db.news.create_index('createdAt', expireAfterSeconds=60*60*24)
    db.news.create_index('query')

def get_everything(query, language='en', sort_by='relevancy', page_size=5):
    client = news_helpers.get_client()
    db = finance_services.get_db()

    cursors = db.news.find_one({'query': query})
    if cursors is None:
        all_articles = client.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
        db.news.insert_one({ 'query': query, 'everything': all_articles, 'createdAt': datetime.datetime.now()})
        return all_articles
    else:
        return cursors.get('everything')

init()