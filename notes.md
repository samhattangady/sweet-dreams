```
strategy schema : Binance
{
    exchange: Binance,
    symbol: ETHBTC, // Symbol for trading
    commodity: ETH, // Currency we are trading
    base: BTC, // Base currency
    commodity_resolution: 3, // Number of decimal places for the commodity
    base_resolution: 6, // Number of decimal places for the base/capital
    trend: 'up', // the overall trend with BTC as base
    capital: 1, // percent of total holdings in pair
    trend_flip_threshhold: 2, // % drop in midpoint prices before flipping
    profit_spread: .3, // target % gain from each trade before fees
    min_bnb: 1, // minimum BNB that must be held
    bnb_buy: 2 // BNB to buy when total goes below min_bnb
}
```

```
trade schema
{
    exchange: Binance,
    symbol: ETHBTC,
    price: 0.01,
    quantity: 5,
    time: 1517244685,
    base: BTC,
    commodity: ETH,
    total_base: .05,
    total_commodity: 0,

}
```
