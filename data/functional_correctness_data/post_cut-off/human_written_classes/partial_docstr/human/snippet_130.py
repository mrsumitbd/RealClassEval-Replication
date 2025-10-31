from urllib.parse import urljoin
import time
from minitap.mobile_use.utils.requests_utils import get_session_with_curl_logging
import requests

class ScreenApiClient:

    def __init__(self, base_url: str, retry_count: int=5, retry_wait_seconds: int=1):
        self.base_url = base_url
        self.session = get_session_with_curl_logging()
        self.retry_count = retry_count
        self.retry_wait_seconds = retry_wait_seconds

    def get_with_retry(self, path: str, **kwargs):
        """
        Make a GET request to the Screen API with retry logic based on the client configuration.
        """
        for attempt in range(self.retry_count):
            try:
                response = self.session.get(urljoin(self.base_url, path), **kwargs)
                if 200 <= response.status_code and response.status_code < 300:
                    return response
                logger.warning(f'Received {response.status_code}, attempt {attempt + 1} of {self.retry_count}. Retrying in {self.retry_wait_seconds} seconds...')
                time.sleep(self.retry_wait_seconds)
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_count - 1:
                    raise e
                time.sleep(self.retry_wait_seconds)
        raise requests.exceptions.RequestException(f'Failed to get a valid response after {self.retry_count} attempts.')

    def post(self, path: str, **kwargs):
        return self.session.post(urljoin(self.base_url, path), **kwargs)