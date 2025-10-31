
from typing import Dict, Any


class TokenUsageTracker:

    def __init__(self):
        self.total_token_usage = {"prompt_tokens": 0,
                                  "completion_tokens": 0, "total_tokens": 0}
        self.success_count = 0
        self.failure_count = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0

    def reset(self):
        self.total_token_usage = {"prompt_tokens": 0,
                                  "completion_tokens": 0, "total_tokens": 0}
        self.success_count = 0
        self.failure_count = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        self.total_token_usage["prompt_tokens"] += token_usage.get(
            "prompt_tokens", 0)
        self.total_token_usage["completion_tokens"] += token_usage.get(
            "completion_tokens", 0)
        self.total_token_usage["total_tokens"] += token_usage.get(
            "total_tokens", 0)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        self.total_turn_count += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        stats = {
            "total_token_usage": self.total_token_usage,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_turn_count": self.total_turn_count,
            "total_execution_time": self.total_execution_time,
            "average_turn_count": self.total_turn_count / (self.success_count + self.failure_count) if (self.success_count + self.failure_count) > 0 else 0,
            "average_execution_time": self.total_execution_time / (self.success_count + self.failure_count) if (self.success_count + self.failure_count) > 0 else 0.0,
            "success_rate": self.success_count / (self.success_count + self.failure_count) if (self.success_count + self.failure_count) > 0 else 0.0
        }
        return stats
