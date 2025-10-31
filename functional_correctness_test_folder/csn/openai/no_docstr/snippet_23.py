
class StripContentTypeMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # Remove any 'Content-Type' header (case-insensitive)
            filtered_headers = [(k, v)
                                for k, v in headers if k.lower() != 'content-type']
            return start_response(status, filtered_headers, exc_info)

        return self.app(environ, custom_start_response)
