class BaseMiddleware:
    """Django-plotly-dash middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.dpd_content_handler = ContentCollector()
        response = self.get_response(request)
        response = request.dpd_content_handler.adjust_response(response)
        return response