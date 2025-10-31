import os
from time import perf_counter

class RequestMetricsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.metrics_request_started = perf_counter()
        response = self.get_response(request)
        if hasattr(request, 'metrics_request_started'):
            view_name = getattr(getattr(request, 'resolver_match', None), 'view_name', None) or '<unnamed view>'
            duration = perf_counter() - request.metrics_request_started
            request_duration.labels(view=view_name, method=request.method, status=str(response.status_code), pid=str(os.getpid())).observe(duration)
        return response