from genai_bench.protocol import UserChatResponse, UserResponse
from genai_bench.metrics.metrics import RequestLevelMetrics

class RequestMetricsCollector:
    """
    A class to collect and calculate metrics for individual requests.

    Attributes:
        metrics (RequestLevelMetrics): An instance to store metrics related
            to a single request.
    """

    def __init__(self):
        self.metrics = RequestLevelMetrics()

    def calculate_metrics(self, response: UserResponse):
        """
        Calculates various metrics from the response of a request.

        Args:
            response (UserResponse): The customized UserResponse object
                containing the response data needed to calculate metrics.
        """
        assert response.num_prefill_tokens is not None, 'response.num_prefill_tokens is None'
        assert response.time_at_first_token is not None, 'response.time_at_first_token is None'
        assert response.start_time is not None, 'response.start_time is None'
        assert response.end_time is not None, 'response.end_time is None'
        self.metrics.num_input_tokens = response.num_prefill_tokens
        self.metrics.ttft = response.time_at_first_token - response.start_time
        self.metrics.e2e_latency = response.end_time - response.start_time
        self.metrics.total_tokens = self.metrics.num_input_tokens
        self.metrics.input_throughput = self.metrics.num_input_tokens / self.metrics.ttft if self.metrics.ttft else 0
        if isinstance(response, UserChatResponse):
            self._calculate_output_metrics(response)
        else:
            self._reset_output_metrics()

    def _calculate_output_metrics(self, response: UserChatResponse):
        """
        Helper function to calculate output metrics from a UserChatResponse.
        """
        assert response.tokens_received is not None, 'response.tokens_received is None'
        self.metrics.num_output_tokens = response.tokens_received
        self.metrics.total_tokens += self.metrics.num_output_tokens
        self.metrics.output_latency = self.metrics.e2e_latency - self.metrics.ttft
        if self.metrics.num_output_tokens > 1:
            self.metrics.tpot = self.metrics.output_latency / (self.metrics.num_output_tokens - 1)
            self.metrics.output_inference_speed = 1 / self.metrics.tpot
            self.metrics.output_throughput = (self.metrics.num_output_tokens - 1) / self.metrics.output_latency if self.metrics.output_latency else 0
        else:
            logger.warning(f'‼️ num_output_tokens:{self.metrics.num_output_tokens} is <= 1. Please check your server and request!')

    def _reset_output_metrics(self):
        """Helper function to reset all output-related metrics to 0."""
        for field in RequestLevelMetrics.OUTPUT_METRICS_FIELDS:
            setattr(self.metrics, field, 0)