from apis import Binance
from stenographer import Stenographer


class SweetDreams:
    """
    Sweet dreams is a trading bot that allows you to make money even 
    while you sleep. It is the next stage of evolution of polaroid.

    Polaroid was the first version of the trading bot. It tried to make
    markets. It would check the mid-price, and place a buy slightly below
    and a sell slightly above. So every time a pair of trades are executed
    it earned a small amount. It only looked to grow the amount of BTC held.
    While buying, it was very aggressive. Rather than sitting and waiting
    with nothing, it would follow the price as it rose so that the time
    with unspent capital was minimum.
    While selling, the same cannot be done, as then it would have faced a
    loss. So instead, it just tracked the price, and if it fell below a 
    certain threshhold, then it would square off and sell according to the
    new mid-price.
    On upswings, it was very profitable, as it would buy in on the small dips
    and keep making. But since it was chasing price to the top, on down swings,
    it would keep squaring off, and each square-off was neutralizing 10-15
    successful trades.

    Sweet Dreams, to fix this issue, now tries to capitalise on the down-swings
    using the reverse of the original strategy. Rather than first buying low and 
    then selling high, it first sells high and then buys low. The thing it is
    betting on is small corrections in the direction opposite to the trend.

    Theoretically, the only loss that sweet dreams would have are on
    multiple continous flips. Such a situation should be very rare, and it
    should be possible to ensure that this doesn't happen using the correct
    parameters for flipping. Because such fluctuations should be where the 
    most money is to be made.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.stenographer = Stenographer()
        self._init_exchange()

    def _init_exchange(self):
        if self.exchange == 'binance':
            self.exchange = Binance()
        else:
            raise ValueError('Currently on Binance is supported')

    def perform_update(self, symbol):
        self.stenographer.record_price(symbol)
        self.stenographer.update_order(symbol)

    def perform_trade(self, symbol):
        self.symbol = task['symbol']
        self._set_class_variables()
        if self.previous_order['status'] in ['unfilled', 'partial']:
            # Depending on the change, see if you need to change price, or
            # change the trend
            self._check_prices()
        elif self.previous_order['status'] in ['filled']:
            # Place the next buy or sell order
            pass

    def _set_class_variables(self):
        self.previous_order = self.stenographer.repeat_order(self.symbol)
        self.strategy = self.stenographer.repeat_strategy(self.symbol)
        self.side = self.previous_order['side'].lower()
        self.trend = self.strategy['trend']

    def _place_order(self):
        rates = self.stenographer.repeat_price(self.symbol)
        mid = (rates['ask'] + rates['bid']) / 2
        price, quantity = self._get_order_price_and_quantity(mid)
        order = self.exchange.place_order(self.side, self.symbol, price, quantity)
        if 'error' in order:
            raise RuntimeError(order['error'])
        order['bid'], order['ask'] = rates['bid'], rates['ask']
        self.stenographer.record_order(order)

    def _get_order_price_and_quantity(self, mid):
        spread_percent = self.strategy['profit_spread']
        side = -1 if self.side == 'buy' else 1
        price = mid + (side * (spread_percent/100)/2 * mid)
        # Truncate the price according the resolution
        price = self._truncate(price, self.strategy['base_resolution'])
        balances = self.exchange.get_balances()
        if 'error' in balances:
            raise RuntimeError(balances['error'])
        if self.side == 'buy':
            for balance in balances:
                # TODO Add ability to operate when different bases are being used
                if balance['asset'] == self.strategy['base']:
                    bal = float(balance['free'])
                    break
            else:
                raise RuntimeError(f'Balance for {self.strategy["base"]} not found')
            quantity = self._truncate(bal / price, self.strategy['commodity_resolution'])
        elif self.side == 'sell':
            for balance in balances:
                # TODO Add ability to operate when different bases are being used
                if balance['asset'] == self.strategy['commodity']:
                    bal = float(balance['free'])
                    break
            else:
                raise RuntimeError(f'Balance for {self.strategy["base"]} not found')
            quantity = self._truncate(bal, self.strategy['commodity_resolution'])
        return price, quantity

    def _truncate(self, amount, digits):
        amount = int(amount * 10**digits)
        return amount/10**digits

    def _check_prices(self):
        current_price = self.stenographer.repeat_price(self.symbol)
        current_mid_price = (current_price['bid'] + current_price['ask']) / 2
        order_mid_price = (self.previous_order['bid'] + self.previous_order['ask']) / 2
        # There are 4 possibilities, first_leg and with_trend are boolean
        buying = self.side == 'buy'
        uptrending = self.trend == 'up'
        increasing = current_mid_price > order_mid_price
        # XNOR operations -> both true, or both false
        # first_leg = (buying and uptrending) or (not buying and not uptrending)
        first_leg = not (buying ^ uptrending)
        with_trend = not (uptrending ^ increasing)
        if first_leg and with_trend:
            # If on first leg and price is with trend, be aggressive
            # Cancel current order and place a new order according to new mid
            # on the same side
            pass
        elif not first_leg and not with_trend:
            # If on second leg, and price is against trend, then our prediction
            # is wrong. Check if price has changed enough to warrant a change of
            # trend. If it is, cancel order, and place a new order on same side
            # according to current mid.
            pass
        else:
            # If on first leg and price is against trend, the correction 
            # that we are betting on has started. Do nothing
            # if on the second leg and price is with trend, then trend prediction
            # is correct. Wait for order to go through. Do nothing
            pass

