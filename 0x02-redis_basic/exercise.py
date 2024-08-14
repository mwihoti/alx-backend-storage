#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to log the input arguments and output of the method.
        """
        # Creating keys for input and output
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Log the input arguments as a string
        self._redis.rpush(input_key, str(args))

        # Call the method and capture the output
        output = method(self, *args, **kwargs)

        # Log the output as a string
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    Args:
        method: The method to be decorated.
    Returns:
        A wrapper function that increments the call count each time the
        method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count each time the
        method is called.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


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

    @call_history
    @count_calls
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
