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
        ask = float(rates['asks'][0]['price'])
        bid = float(rates['bids'][0]['price'])
        t = time.time()
        entry = {
            'exchange': self.exchange,
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

    def record_order(self, symbol, order):
        to_insert = {
            'exchange': self.exchange,
            'symbol': order['symbol'],
            'side': order['side'].lower(),
            'price': float(order['price']),
            'quantity': float(order['origQty']),
            'time': time.time(),
            'base': order['base'],
            'commodity': order['commodity'],
            'bid': order['bid'],
            'ask': order['ask'],
            'status': order['status'].lower(),
            'order_id': order['orderId']
            'status': order
        }
        self.database.orders.insert_one(to_insert)

    def repeat_order(self, symbol):
        cursor = self.database.orders.find({'symbol': symbol}).sort([('time', -1)]).limit(1)
        # TODO. Deal with IndexError here
        return cursor[0]

    def update_order(self, symbol):
        current_order = self.repeat_order(symbol)
        # For first ever order, don't try to update
        if 'order_id' not in current_order:
            return
        order = self.engine.query_order(self, symbol, current_order['order_id'])
        statusses = {'NEW': 'new', 'PARTIALLY_FILLED': 'partial', 'FILLED': 'filled',
                'CANCELED': 'cancelled'}
        status = statusses.get(order['status'], order['status'])
        self.database.orders.update_one({'order_id': current_order['order_id']}, 
                {'$set': {'status': status}})

    def record_strategy(self, symbol, strategy):
        strategy['time'] = time.time()
        self.database.strategies.insert_one(strategy)

    def repeat_strategy(self, symbol):
        cursor = self.database.strategies.find({'symbol': symbol}).sort([('time', -1)]).limit(1)
        # TODO. Deal with IndexError here
        return cursor[0]

    def record_trade(self, symbol, trade):
        del trade['ask']
        del trade['bid']
        del trade['status']
        trade['time'] = time.time()
        trade['base_value'] = trade['price'] * trade['quantity']
        trade['commodity_value'] = trade['quantity']
        self.database.trades.insert_one(trade)
        # total_value calculation may cause RuntimeErrors. Don't want that 
        # to prevent the recording of the trade in db
        total_value = self.exchange.get_account_value()
        self.database.update_one({'order_id': trade['order_id']}, {'$set': {'total_value': total_value}})

    def repeat_trade(self, symbol):
        cursor = self.database.trades.find({'symbol': symbol}).sort([('time', -1)]).limit(1)
        # TODO. Deal with IndexError here
        return cursor[0]

