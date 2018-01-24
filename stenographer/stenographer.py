import time

import pymongo
import requests

import apis


class Stenographer:
    """
    Peeker keeps track of sweet_dreams
    """
    def __init__(self, exchange='binance'):
        self.exchange = exchange
        self.engine = None
        self.database = pymongo.MongoClient().sweet_dreams
        self._initialise_engine()

    def _initialise_engine(self):
        if self.exchange == 'binance':
            self.engine = apis.Binance()

    def update_prices(self, symbol):
        rates = self.engine.get_order_book(symbol)
        ask = rates['asks'][0]
        bid = rates['bids'][0]
        t = time.time()
        entry = {
            'ask': ask,
            'bid': bid,
            'time': t,
            'symbol': symbol
        }
        self.database.prices.insert_one(entry)

    def repeat_prices(self, symbol):
        cursor =  self.database.prices.find({'symbol': symbol}).sort([('time', -1)]).limit(1)
        # TODO. Deal with IndexError here
        return cursor[0]

