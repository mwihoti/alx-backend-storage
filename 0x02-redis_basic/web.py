#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function (prototype: def get_page
(url: str) -> str:). The core of the function is very simple. It uses the
requests module to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code written
in exercise.py.

Inside get_page track how many times a particular URL was accessed in the key
"count:{url}" and cache the result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow
response and test your caching.
Bonus: implement this use case with decorators.
"""


import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
"""
Redis instance
"""


def cache(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result_cache = redis_store.get(f'result:{url}')
        if result_cache:
            return result_cache.decode('utf-8')
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    
    return invoker


@cache
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
