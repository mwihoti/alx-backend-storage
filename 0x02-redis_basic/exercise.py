#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    Class Cache
    """
    def __init__(self):
        """
        Cache class. In the __init__ method, store an instance of the Redis
        client as a private variable named _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes a data argument and returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """
        Method that takes a key string argument and an optional Callable
        argument named fn and returns the right data
        """
        # get data from redis
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Method that takes a key string argument and returns a string
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Method that takes a key string argument and returns an int
        """
        return self.get(key, lambda d: int(d))
