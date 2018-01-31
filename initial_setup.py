import json
import time

import greenstalk
import pymongo

def check_db():
    # We expect a local instance of mongodb to be running
    client = pymongo.MongoClient('localhost:27017', serverSelectionTimeoutMS=5)
    try:
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        raise RuntimeError('Expecting MongoDB to be running at localhost:27017')
    return client

def setup_db(client):
    database = client.sweet_dreams
    collections = database.collection_names()
    # Create 1GB capped collections for prices if it doesnt exist
    if not 'prices' in collections:
        database.create_collection('prices', capped=True, size=2**30)
    # Create collections for orders, trades and strategies
    if not 'orders' in collections:
        database.create_collection('orders')
    if not 'trades' in collections:
        database.create_collection('trades')
    if not 'strategies' in collections:
        database.create_collection('strategies')
    order = database.orders.find_one()
    if order is None:
        # Add 'cancelled' order to db so that the trading can start
        # We don't add order_id so that steno doesn't try to update
        database.orders.insert_one({
                'exchange': 'binance',
                'symbol': 'ETHBTC',
                'side': 'buy',
                'time': time.time(),
                'base': 'BTC',
                'commodity': 'ETH',
                'status': 'cancelled'
            })
    strategy = database.strategies.find_one()
    if strategy is None:
        # Add a starting strategy
        database.strategies.insert_one({
                'exchange': 'binance',
                'symbol': 'ETHBTC',
                'commodity': 'ETH',
                'base': 'BTC',
                'commodity_resolution': 3,
                'base_resolution': 6,
                'trend': 'up',
                'capital': 1,
                'trend_flip_threshhold': 2,
                'profit_spread': .3,
                'min_bnb': 1,
                'bnb_buy': 3,
                'time': time.time()
            })

def check_beanstalk():
    # Check that beanstalkd is running in the correct place
    try:
        queue = greenstalk.Client()
    except ConnectionRefusedError:
        raise RuntimeError('Could not connect to beanstalkd at 127.0.0.1:11300')
    return queue
    
def setup_beanstalk(queue):
    # We just want to know if there is a job in the queue
    # Checking whether it is a valid job is out of scope
    try:
        job = queue.peek_ready()
    except greenstalk.NotFoundError:
        update_task = json.dumps({'symbol': 'ETHBTC', 'task': 'update'})
        trade_task = json.dumps({'symbol': 'ETHBTC', 'task': 'trade'})
        queue.put(update_task, priority=500)
        queue.put(trade_task, priority=1000)

def setup():
    client = check_db()
    queue = check_beanstalk()
    setup_db(client)
    setup_beanstalk(queue)
    return client, queue

