import time
from typing import Callable, List, TYPE_CHECKING

class Retry:

    def __init__(self):
        self.attempts: int = 6
        self.sleep_seconds: int = 10
        self.exceptions: List[Exception] = [botocore.exceptions.EndpointConnectionError]
        self.client_error_codes: List[str] = ['NoSuchUpload']

    def _do(self, fn: Callable):
        for attempt in range(self.attempts):
            try:
                return fn()
            except tuple(self.exceptions) as err:
                logger.critical('Caught non-fatal %s, retrying %d more times', err, self.attempts - attempt - 1)
                logger.exception(err)
                time.sleep(self.sleep_seconds)
            except botocore.exceptions.ClientError as err:
                error_code = err.response['Error'].get('Code')
                if error_code not in self.client_error_codes:
                    raise
                logger.critical('Caught non-fatal ClientError (%s), retrying %d more times', error_code, self.attempts - attempt - 1)
                logger.exception(err)
                time.sleep(self.sleep_seconds)
        else:
            logger.critical('encountered too many non-fatal errors, giving up')
            raise IOError('%s failed after %d attempts', fn.func, self.attempts)