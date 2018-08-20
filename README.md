# sweet dreams

_"If you don't find a way to make money while you sleep, you will work until you die."_ 

- Warren Buffet

Sweet dreams is a trading bot that allows you to make money even while you sleep. It is
the next stage of evolution of polaroid.

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
Theoretically, one of the losses that sweet dreams would have are on
multiple continous flips. Such a situation should be very rare, and it
should be possible to ensure that this doesn't happen using the correct
parameters for flipping. Because such fluctuations should be where the
most money is to be made.

The other situation where losses would be faced are when there is a sharp
movement without any corrections. Since the strategy is designed around
exploiting the small corrections in the general trend, if there are two
sharp movements consecutively, it could cause a lot of loss. But the
likelihood of that seems low.
