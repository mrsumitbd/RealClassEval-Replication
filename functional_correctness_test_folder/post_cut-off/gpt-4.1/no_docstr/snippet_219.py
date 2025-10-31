
from typing import Dict, Any


class TokenUsageTracker:

    def __init__(self):
        self.reset()

    def reset(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_token_usage = {}
        self.total_turn_count = 0
        self.total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        self.total_calls += 1
        if success:
            self.successful_calls += 1
        else:
            self.failed_calls += 1
        for k, v in token_usage.items():
            if k in self.total_token_usage:
                self.total_token_usage[k] += v
            else:
                self.total_token_usage[k] = v
        self.total_turn_count += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        avg_turn_count = self.total_turn_count / \
            self.total_calls if self.total_calls else 0
        avg_execution_time = self.total_execution_time / \
            self.total_calls if self.total_calls else 0
        avg_token_usage = {}
        for k, v in self.total_token_usage.items():
            avg_token_usage[k] = v / \
                self.total_calls if self.total_calls else 0
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "total_token_usage": dict(self.total_token_usage),
            "average_token_usage": avg_token_usage,
            "total_turn_count": self.total_turn_count,
            "average_turn_count": avg_turn_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": avg_execution_time
        }
