import hashlib
import hmac
import time

import requests

from .credentials import binance

class Binance:
    def __init__(self):
        self.secret = binance['secret']
        self.api_key = binance['api_key']
        self.api_root = binance['api_root']

    def get_order_book(self, symbol, depth=10):
        r = requests.get(f'{self.api_root}/api/v1/depth', params={'symbol':symbol, 'limit': 5})
        if not r.ok:
            return {'error': r.json()}
        order_book = r.json()
        bids = [{'price': float(bid[0]), 'quantity': float(bid[1])} for bid in order_book['bids'][:depth]]
        asks = [{'price': float(ask[0]), 'quantity': float(ask[1])} for ask in order_book['asks'][:depth]]
        return {'bids': bids, 'asks': asks}

    def get_balance(self):
        message, signature = self._get_message_and_signature(request)
        r = requests.get(f'{self.api_root}/api/v3/account',
                params=f'{message}&signature={signature}',
                headers={'X-MBX-APIKEY': self.api_key})
        if not r.ok:
            return {'error': r.json()}
        return r.json()['balances']

    def get_account_value(self):
        balances = self.get_balances()
        if 'error' in balances:
            raise RuntimeError(f'Error in fetching balances: {balances["error"]}')
        value = 0
        for currency in balances:
            total = float(currency['free']) + float(currency['locked'])
            if currency['asset'] == 'BTC':
                value += total
            else:
                rates = self.get_order_book(currency['asset']+'BTC')
                if 'error' in rates:
                    raise RuntimeError(r'Error in getting rates: {rates["error"]}')
                ask = float(rates['asks'][0]['price'])
                bid = float(rates['bids'][0]['price'])
                mid = (ask + bid) / 2
                value = total * mid
        return value


    def execute_order_request(self, request, action='post'):
        message, signature = self._get_message_and_signature(request)
        if action == 'post':
            req = requests.post
        elif action == 'get':
            req = requests.get
        elif action == 'delete':
            req = requests.delete
        r = req(f'{self.api_root}/api/v3/order', 
                params=f'{message}&signature={signature}',
                headers={'X-MBX-APIKEY': self.api_key})
        if not r.ok:
            return {'error': r.json()}
        return r.json()

    def place_order(self, side, symbol, price, quantity):
        request = f'symbol={symbol}&side={side.upper()}&type=LIMIT&timeInForce=GTC&quantity={quantity}&price={price}'
        r = self.execute_order_request(request, action='post')
        return r

    def query_order(self, symbol, order_id):
        request = f'symbol={symbol}&orderId={order_id}'
        r = self.execute_order_request(request, action='get')
        return r

    def delete_order(self, symbol, order_id):
        request = f'symbol={symbol}&orderId={order_id}'
        r = self.execute_order_request(request, action='delete')
        return r

    def _get_message_and_signature(self, request):
        message = f'{request}&timestamp={str(int(time.time() * 1000))}'
        message_bytes = bytes(message, 'utf-8')
        secret = bytes(self.secret, 'utf-8')
        signature = hmac.new(secret, msg=message_bytes, digestmod=hashlib.sha256).hexdigest()
        return message, signature
