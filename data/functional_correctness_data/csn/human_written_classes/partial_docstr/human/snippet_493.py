import time
import functools

class timer:

    def __call__(self, function):
        """Turn the object into a decorator"""

        @functools.wraps(function)
        def wrapper(*arg, **kwargs):
            t1 = time.clock()
            result = function(*arg, **kwargs)
            t2 = time.clock()
            TIMING_RESULTS[function.__name__].append(t2 - t1)
            return result
        return wrapper