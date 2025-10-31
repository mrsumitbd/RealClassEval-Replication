
from typing import Dict, Any


class TokenUsageTracker:

    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.total_tokens = 0
        self.total_turns = 0
        self.total_execution_time = 0.0
        self.max_tokens = 0
        self.min_tokens = float('inf')

    def reset(self):
        self.success_count = 0
        self.failure_count = 0
        self.total_tokens = 0
        self.total_turns = 0
        self.total_execution_time = 0.0
        self.max_tokens = 0
        self.min_tokens = float('inf')

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        total_tokens = sum(token_usage.values())
        self.total_tokens += total_tokens
        self.total_turns += turn_count
        self.total_execution_time += execution_time

        if total_tokens > self.max_tokens:
            self.max_tokens = total_tokens
        if total_tokens < self.min_tokens:
            self.min_tokens = total_tokens

    def get_stats(self) -> Dict[str, Any]:
        total_calls = self.success_count + self.failure_count
        avg_tokens = self.total_tokens / total_calls if total_calls > 0 else 0
        avg_turns = self.total_turns / total_calls if total_calls > 0 else 0
        avg_execution_time = self.total_execution_time / \
            total_calls if total_calls > 0 else 0.0

        return {
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'total_tokens': self.total_tokens,
            'total_turns': self.total_turns,
            'total_execution_time': self.total_execution_time,
            'max_tokens': self.max_tokens,
            'min_tokens': self.min_tokens,
            'avg_tokens': avg_tokens,
            'avg_turns': avg_turns,
            'avg_execution_time': avg_execution_time
        }
