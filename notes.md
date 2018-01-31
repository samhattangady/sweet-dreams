```
price schema 
{
    exchange: binance,
    ask: 0.01,
    bid: 0.009,
    time: 1517244685,
    symbol: ETHBTC
}
```

```
strategy schema : Binance
{
    exchange: binance,
    symbol: ETHBTC, // Symbol for trading
    commodity: ETH, // Currency we are trading
    base: BTC, // Base currency
    commodity_resolution: 3, // Number of decimal places for the commodity
    base_resolution: 6, // Number of decimal places for the base/capital
    trend: 'up', // the overall trend with BTC as base
    capital: 1, // fraction of total holdings in pair
    trend_flip_threshhold: 2, // % drop in midpoint prices before flipping
    profit_spread: .3, // target % gain from each trade before fees
    min_bnb: 1, // minimum BNB that must be held
    bnb_buy: 2, // BNB to buy when total goes below min_bnb
    time: 1517244685
}
```

```
trade schema
{
    exchange: binance,
    symbol: ETHBTC,
    side: buy,
    price: 0.01,
    quantity: 5,
    time: 1517244685,
    base: BTC,
    commodity: ETH,
    base_value: .05,
    commodity_value: 0.5,
    total_value: .08,
    order_id: 12345
}
```

```
order schema
{
    exchange: binance,
    symbol: ETHBTC,
    side: buy,
    price: 0.01,
    quantity: 5,
    time: 1517244685,
    base: BTC,
    commodity: ETH,
    bid: 0.009,
    ask: 0.011,
    status: new,
    order_id: 12345
}
```

