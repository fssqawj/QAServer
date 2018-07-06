import time
from functools import wraps


def timer(func):
    @wraps(func)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" % (str(func.__module__) + ':' + func.__name__, str(t1-t0)))
        return result
    return function_timer
