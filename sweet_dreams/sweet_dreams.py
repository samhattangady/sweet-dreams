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
    On upswings, it was very profitable, as it would buy in the small dips
    and keep making. But since it was chasing price to the top, on down swings,
    it would keep squaring off, and each square-off was neutralizing 10-15
    successful trades.

    Sweet Dreams on the other hand, now tries to capitalise on the down-swings
    by growing the opposite currency by _flipping_. So once it flips, it 
    makes more of the opposite with the same logic that polaroid was using on
    upward swings.
    Prior to field tests, the only loss that sweet dreams would have are on
    multiple continous flips. Such a situation should be very rare, and it
    should be possible to ensure that this doesn't happen using the correct
    parameters for flipping. Because such fluctuations should be where the 
    most money is to be made.

    Internally, we use the `self.flipped` parameter is used to track whether 
    to be aggressive on the buy or the sell.
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.stenographer = Stengrapher()
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
            # Depending on the side, see if you need to change price, or
            # initiate flip
            self._check_prices()
        elif self.previous_order['status'] in ['filled']:
            # Depending on the side, place the next buy or sell order
            pass


    def _set_class_variables(self):
        self.previous_order = self.stenographer.repeat_order(self.symbol)
        self.strategy = self.stenographer.repeat_strategy(self.symbol)
        self.flipped = False
        if self.strategy['symbol'].index(strategy['base']) == 0:
            # ETHBTC with strategy base as ETH
            self.flipped = True
        self.side = self.previous_order['side'].lower()

    def _start_buy_order(self):
        price = self.stenographer.repeat_price(self.symbol)
        mid = (price['ask'] + price['bid']) / 2


