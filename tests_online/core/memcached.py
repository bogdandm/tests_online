from functools import wraps
from typing import Any, Callable, Union

from django.core.cache import caches


def memcached_method(key: Union[str, Callable], timeout: int, cache=None):
    """
    Uses django cache to store value.

    Use ``class_or_instance.function.clear_cache(*args, **kwargs)`` to delete cached value

    :param key: str or lambda function that takes *args of actual call
    :param timeout: expire seconds
    :return: decorator
    :param cache:

    .. code-block:: python

        @memcached_method(
            key=lambda name: PREFIX + name,
            timeout=60
        )
        def get_by_name(self, name):
            return self.get(name=name)

        def clear_get_by_name(self, name):
            self.get_by_name.clear_cache(name)
    """
    cache = cache or caches['default']

    def decorator(fn):
        fn_name = fn.__name__

        def get_key(*args, **kwargs):
            return (key(*args, **kwargs) if callable(key) else key) + "(method)" + fn_name

        def clear_cache(*args, **kwargs):
            cache.delete(get_key(*args, **kwargs))

        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            cache_key = get_key(*args, **kwargs)
            cache_item = cache.get(cache_key)
            if cache_item is None:
                cache_item = fn(self, *args, **kwargs)
                cache.set(cache_key, cache_item, timeout)
            return cache_item

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator


def memcached_property(key: Union[str, Callable[[Any], str]], timeout: int, cache=None):
    """
    Uses django cache to store value.

    Use ``Class.property_name.fget.clear_cache(instance)`` to delete cached value

    :param key: str or lambda function that takes instance of property as agrument
    :param timeout: expire seconds
    :return: decorator
    :param cache:

    .. code-block:: python

        @memcached_property(
            key=lambda self: self.CACHE_PREFIX + str(self.id),
            timeout=30  # seconds
        )
        def is_subprocess(self):
            return self.child and self.child.subprocess

        def clear_is_subprocess(self):
            self.__class__.is_subprocess.fget.clear_cache(self)
    """
    cache = cache or caches['default']

    def decorator(fn):
        fn_name = fn.__name__

        def get_key(self):
            return (key(self) if callable(key) else key) + "(prop)" + fn_name

        def clear_cache(self):
            cache.delete(get_key(self))

        @wraps(fn)
        def wrapper(self):
            cache_key = get_key(self)
            cache_item = cache.get(cache_key)
            if cache_item is None:
                cache_item = fn(self)
                cache.set(cache_key, cache_item, timeout)
            return cache_item

        wrapper.clear_cache = clear_cache
        return property(wrapper)

    return decorator
