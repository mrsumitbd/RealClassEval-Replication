class Retry:
    """
    Object to be used with `request_retry`.
    It configures some retry options and can be subclassed to customise related logic.
    """

    def __init__(self, max_retries, retry_on_status=(408, 500, 502, 503, 504)):
        self.max_retries = max_retries
        self.retry_on_status = retry_on_status
        self.retry_count = 0

    def should_retry(self, exception=None, response=None):
        """
        :return: True if the caller should retry the same request.
        :exception Exception: any raised exception
        :response HTTPResponse: any response returned, including successful ones.
        """
        if response is not None and response.status_code not in self.retry_on_status:
            return False
        return self.max_retries - self.retry_count > 0

    def before_retrying(self, request_kwargs):
        """
        Callback called before retrying.
        """
        self.retry_count += 1