class StripContentTypeMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        cl = environ.get('CONTENT_LENGTH')
        has_length = False
        if cl is not None and cl != '':
            try:
                has_length = int(cl) > 0
            except (ValueError, TypeError):
                has_length = False

        if not has_length:
            environ.pop('CONTENT_TYPE', None)
            environ.pop('HTTP_CONTENT_TYPE', None)

        return self.app(environ, start_response)
