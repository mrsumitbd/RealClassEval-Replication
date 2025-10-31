import functools
import fastapi

class fastapi_min_version:

    def __init__(self, min_version):
        self.min_version = min_version

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not is_current_version_higher_or_equal(fastapi.__version__, self.min_version):
                raise FastAPIVersionError(self.min_version, reason=f'to use {func.__name__}() function')
            return func(*args, **kwargs)
        return wrapper