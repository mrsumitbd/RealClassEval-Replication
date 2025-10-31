
from typing import Dict, Any


class TokenUsageTracker:

    def __init__(self):
        self.total_tokens = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_turns = 0
        self.total_execution_time = 0.0

    def reset(self):
        self.total_tokens = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_turns = 0
        self.total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        self.total_tokens += sum(token_usage.values())
        self.total_turns += turn_count
        self.total_execution_time += execution_time
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_tokens': self.total_tokens,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'total_turns': self.total_turns,
            'total_execution_time': self.total_execution_time
        }
