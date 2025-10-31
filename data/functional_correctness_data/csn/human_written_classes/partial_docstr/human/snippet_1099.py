from django.conf import settings
from edx_django_utils.logging import encrypt_for_log
import random
import json

class CookieMonitoringMiddleware:
    """
    Middleware for monitoring the size and growth of all our cookies, to see if
    we're running into browser limits.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.deprecated_cookie_prefixes = getattr(settings, 'COOKIE_PREFIXES_TO_REMOVE', [])
        if not isinstance(self.deprecated_cookie_prefixes, list):
            log.warning(f'COOKIE_PREFIXES_TO_REMOVE must be a list of (name, domain) tuples, not {type(self.deprecated_cookie_prefixes)}. No cookies will be removed.')
            self.deprecated_cookie_prefixes = []

    def __call__(self, request):
        log_message = None
        try:
            log_message = self.get_log_message_and_monitor_cookies(request)
        except BaseException:
            log.exception('Unexpected error logging and monitoring cookies.')
        response = self.get_response(request)
        for deprecated_cookie_prefix, domain in self.deprecated_cookie_prefixes:
            for cookie_name in request.COOKIES.keys():
                if cookie_name.startswith(deprecated_cookie_prefix):
                    log.info(f'Deleting cookie {cookie_name} in domain {domain}')
                    response.delete_cookie(cookie_name, domain=domain)
        if log_message:
            log.info(log_message)
        return response

    def get_log_message_and_monitor_cookies(self, request):
        """
        Add logging and custom attributes for monitoring cookie sizes.

        For cookie size monitoring, we don't log raw contents of cookies because that might
        cause a security issue—we just want to see if any cookies are growing out of control.
        However, there is also an option for encrypted logging of cookie data where there
        appears to be some kind of data corruption occurring.

        Useful NRQL Queries:

            # Always available
            SELECT * FROM Transaction WHERE cookies.header.size > 6000

        Attributes that are added by this middleware:

            For all requests:

                cookies.header.size: The total size in bytes of the cookie header

            If COOKIE_HEADER_SIZE_LOGGING_THRESHOLD is reached:

                cookies.header.size.computed

        Related Settings (see annotations for details):

            - COOKIE_HEADER_SIZE_LOGGING_THRESHOLD
            - COOKIE_SAMPLING_REQUEST_COUNT
            - UNUSUAL_COOKIE_HEADER_PUBLIC_KEY
            - UNUSUAL_COOKIE_HEADER_LOG_CHUNK

        Returns: The message to be logged. This is returned, rather than directly
            logged, so that it can be processed at request time (before any cookies
            may be changed server-side), but logged at response time, once the user
            id is available for authenticated calls.

        """
        raw_header_cookie = request.headers.get('cookie', '')
        cookie_header_size = len(raw_header_cookie.encode('utf-8'))
        _set_custom_attribute('cookies.header.size', cookie_header_size)
        if cookie_header_size == 0:
            return None
        if (corrupt_cookie_count := raw_header_cookie.count('Cookie: ')):
            _set_custom_attribute('cookies.header.corrupt_count', corrupt_cookie_count)
            _set_custom_attribute('cookies.header.corrupt_key_count', sum((1 for key in request.COOKIES.keys() if 'Cookie: ' in key)))
            self.log_corrupt_cookie_headers(request, corrupt_cookie_count)
        logging_threshold = getattr(settings, 'COOKIE_HEADER_SIZE_LOGGING_THRESHOLD', None)
        if not logging_threshold:
            return None
        is_large_cookie_header_detected = cookie_header_size >= logging_threshold
        if not is_large_cookie_header_detected:
            sampling_request_count = getattr(settings, 'COOKIE_SAMPLING_REQUEST_COUNT', None)
            if not sampling_request_count or random.randint(1, sampling_request_count) > 1:
                return None
        cookies_header_size_computed = max(0, sum((len(name) + len(value) + 3 for name, value in request.COOKIES.items())) - 2)
        _set_custom_attribute('cookies.header.size.computed', cookies_header_size_computed)
        sorted_cookie_items = sorted(request.COOKIES.items(), key=lambda x: len(x[1]), reverse=True)
        sizes = ', '.join((f'{name}: {len(value)}' for name, value in sorted_cookie_items))
        if is_large_cookie_header_detected:
            log_prefix = f'Large (>= {logging_threshold}) cookie header detected.'
        else:
            log_prefix = f'Sampled small (< {logging_threshold}) cookie header.'
        log_message = f'{log_prefix} BEGIN-COOKIE-SIZES(total={cookie_header_size}) {sizes} END-COOKIE-SIZES'
        return log_message

    def log_corrupt_cookie_headers(self, request, corrupt_cookie_count):
        """
        Log all headers when corrupt cookies are detected (if settings permit).

        This log data is encrypted using the log-sensitive utility.

        - Logging requires that ``UNUSUAL_COOKIE_HEADER_PUBLIC_KEY`` is set.
        - Output is split across multiple lines using ``UNUSUAL_COOKIE_HEADER_LOG_CHUNK``.
        """
        if corrupt_cookie_count < 1:
            return
        corrupt_cookie_log_pub_key = getattr(settings, 'UNUSUAL_COOKIE_HEADER_PUBLIC_KEY', None)
        if not corrupt_cookie_log_pub_key:
            return
        chunk_size = getattr(settings, 'UNUSUAL_COOKIE_HEADER_LOG_CHUNK', 9000)
        header_data = json.dumps(dict(request.headers.items()))
        enc_output = encrypt_for_log(header_data, corrupt_cookie_log_pub_key)
        msg = f'All headers for request with corrupted cookies (count={corrupt_cookie_count}): {enc_output}'
        for piece in split_ascii_log_message(msg, chunk_size):
            log.info(piece)