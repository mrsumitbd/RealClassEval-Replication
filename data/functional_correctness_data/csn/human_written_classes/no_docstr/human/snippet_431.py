from pebble.common import Result, ResultStatus
import itertools

class MapResults:

    def __init__(self, futures: list, timeout: float=None):
        self._results = itertools.chain.from_iterable((chunk_result(f, timeout) for f in futures))

    def __iter__(self):
        return self

    def next(self):
        result = next(self._results)
        if isinstance(result, Result):
            if result.status == ResultStatus.SUCCESS:
                return result.value
            result = result.value
        raise result
    __next__ = next