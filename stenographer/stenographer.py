import time

import pymongo
import requests

import apis


class Stenographer:
    """
    Stenographer keeps track of sweet_dreams
    """
    def __init__(self, exchange='binance'):
        self.exchange = exchange
        self.engine = None
        self.database = pymongo.MongoClient().sweet_dreams
        self._initialise_engine()

    def _initialise_engine(self):
        if self.exchange == 'binance':
            self.engine = apis.Binance()

    def record_price(self, symbol):
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

    def repeat_price(self, symbol):
        cursor =  self.database.prices.find({'symbol': symbol}).sort([('time', -1)]).limit(1)
        # TODO. Deal with IndexError here
        return cursor[0]

    def record_order(self, order):
        # TODO Add the order to db
        pass

    def repeat_order(self, symbol):
        # TODO Return the most recent order
        pass

    def update_order(self, symbol):
        # TODO Update the order based on the state of order in exchange
        pass

