from apis import Binance
from stenographer import Stenographer

class SweetDreams:
    """
    Sweet dreams is a trading bot that allows you to make money even 
    while you sleep. It is the next stage of evolution of polaroid.
    """

    def __init__(self, pair):
        self.exchange = Binance()
        self.pair = pair

    
