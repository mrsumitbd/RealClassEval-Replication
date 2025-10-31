from django_prometheus.conf import NAMESPACE, PROMETHEUS_LATENCY_BUCKETS
from prometheus_client import Counter, Histogram
from django_prometheus.utils import PowersOf, Time, TimeSince

class Metrics:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
        return metric_cls(name, documentation, labelnames=labelnames, **kwargs)

    def __init__(self, *args, **kwargs):
        self.register()

    def register(self):
        self.requests_total = self.register_metric(Counter, 'django_http_requests_before_middlewares_total', 'Total count of requests before middlewares run.', namespace=NAMESPACE)
        self.responses_total = self.register_metric(Counter, 'django_http_responses_before_middlewares_total', 'Total count of responses before middlewares run.', namespace=NAMESPACE)
        self.requests_latency_before = self.register_metric(Histogram, 'django_http_requests_latency_including_middlewares_seconds', 'Histogram of requests processing time (including middleware processing time).', buckets=PROMETHEUS_LATENCY_BUCKETS, namespace=NAMESPACE)
        self.requests_unknown_latency_before = self.register_metric(Counter, 'django_http_requests_unknown_latency_including_middlewares_total', 'Count of requests for which the latency was unknown (when computing django_http_requests_latency_including_middlewares_seconds).', namespace=NAMESPACE)
        self.requests_latency_by_view_method = self.register_metric(Histogram, 'django_http_requests_latency_seconds_by_view_method', 'Histogram of request processing time labelled by view.', ['view', 'method'], buckets=PROMETHEUS_LATENCY_BUCKETS, namespace=NAMESPACE)
        self.requests_unknown_latency = self.register_metric(Counter, 'django_http_requests_unknown_latency_total', 'Count of requests for which the latency was unknown.', namespace=NAMESPACE)
        self.requests_ajax = self.register_metric(Counter, 'django_http_ajax_requests_total', 'Count of AJAX requests.', namespace=NAMESPACE)
        self.requests_by_method = self.register_metric(Counter, 'django_http_requests_total_by_method', 'Count of requests by method.', ['method'], namespace=NAMESPACE)
        self.requests_by_transport = self.register_metric(Counter, 'django_http_requests_total_by_transport', 'Count of requests by transport.', ['transport'], namespace=NAMESPACE)
        self.requests_by_view_transport_method = self.register_metric(Counter, 'django_http_requests_total_by_view_transport_method', 'Count of requests by view, transport, method.', ['view', 'transport', 'method'], namespace=NAMESPACE)
        self.requests_body_bytes = self.register_metric(Histogram, 'django_http_requests_body_total_bytes', 'Histogram of requests by body size.', buckets=PowersOf(2, 30), namespace=NAMESPACE)
        self.responses_by_templatename = self.register_metric(Counter, 'django_http_responses_total_by_templatename', 'Count of responses by template name.', ['templatename'], namespace=NAMESPACE)
        self.responses_by_status = self.register_metric(Counter, 'django_http_responses_total_by_status', 'Count of responses by status.', ['status'], namespace=NAMESPACE)
        self.responses_by_status_view_method = self.register_metric(Counter, 'django_http_responses_total_by_status_view_method', 'Count of responses by status, view, method.', ['status', 'view', 'method'], namespace=NAMESPACE)
        self.responses_body_bytes = self.register_metric(Histogram, 'django_http_responses_body_total_bytes', 'Histogram of responses by body size.', buckets=PowersOf(2, 30), namespace=NAMESPACE)
        self.responses_by_charset = self.register_metric(Counter, 'django_http_responses_total_by_charset', 'Count of responses by charset.', ['charset'], namespace=NAMESPACE)
        self.responses_streaming = self.register_metric(Counter, 'django_http_responses_streaming_total', 'Count of streaming responses.', namespace=NAMESPACE)
        self.exceptions_by_type = self.register_metric(Counter, 'django_http_exceptions_total_by_type', 'Count of exceptions by object type.', ['type'], namespace=NAMESPACE)
        self.exceptions_by_view = self.register_metric(Counter, 'django_http_exceptions_total_by_view', 'Count of exceptions by view.', ['view'], namespace=NAMESPACE)