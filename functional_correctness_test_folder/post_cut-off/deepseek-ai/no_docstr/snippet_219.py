
from typing import Dict, Any


class TokenUsageTracker:

    def __init__(self):
        self.total_successful_turns = 0
        self.total_failed_turns = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_turns = 0
        self.total_execution_time = 0.0

    def reset(self):
        self.total_successful_turns = 0
        self.total_failed_turns = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_turns = 0
        self.total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        if success:
            self.total_successful_turns += 1
        else:
            self.total_failed_turns += 1

        self.total_prompt_tokens += token_usage.get('prompt_tokens', 0)
        self.total_completion_tokens += token_usage.get('completion_tokens', 0)
        self.total_turns += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_successful_turns': self.total_successful_turns,
            'total_failed_turns': self.total_failed_turns,
            'total_prompt_tokens': self.total_prompt_tokens,
            'total_completion_tokens': self.total_completion_tokens,
            'total_tokens': self.total_prompt_tokens + self.total_completion_tokens,
            'total_turns': self.total_turns,
            'total_execution_time': self.total_execution_time,
            'avg_execution_time_per_turn': self.total_execution_time / self.total_turns if self.total_turns > 0 else 0.0
        }
