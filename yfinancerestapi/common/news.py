from newsapi import NewsApiClient

import os

API_KEY = os.environ.get('NEWS_API_KEY')
client = NewsApiClient(api_key = API_KEY)

def get_client():
    return client


