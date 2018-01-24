strategy schema : Binance

```
{
    exchange: Binance,
    symbol: ETHBTC,
    base: ETH,  \\ Currency that we are trying to grow. Changes with every flip
    capital: 1, \\ Total weighted trading amount (Not implemented)
    flip_threshhold: 2, \\ % drop in midpoint prices before flipping
    profit_spread: .3, \\ target % gain from each trade before fees
    min_bnb: 1, \\ minimum BNB that must be held
    bnb_buy: 2 \\ BNB to buy when total goes below min_bnb
}
```
