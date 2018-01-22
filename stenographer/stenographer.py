import time

import pymongo
import requests

import apis


class Stenographer:
    """
    Peeker checks market prices.
    """
    def __init__(self, exchange='binance'):
        self.exchange = exchange
        self.engine = None
        self._initialise_engine()

    def _initialise_engine(self):
        if self.exchange == 'binance':
            self.engine = apis.Binance()

    def peek(self, symbol):
        return self.engine.get_order_book(symbol)

