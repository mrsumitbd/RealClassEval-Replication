
from typing import Dict, Any


class TokenUsageTracker:
    """Track token usage across agent executions."""

    def __init__(self):
        """Initialize token usage tracker."""
        self.reset()

    def reset(self):
        """Reset all usage statistics."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0
        self.success_count = 0
        self.failure_count = 0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        """
        Update usage statistics.

        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        """
        self.total_input_tokens += token_usage['input_tokens']
        self.total_output_tokens += token_usage['output_tokens']
        self.total_tokens += token_usage['total_tokens']
        self.total_turn_count += turn_count
        self.total_execution_time += execution_time
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics with calculated averages.

        Returns:
            Dictionary containing usage statistics
        """
        total_executions = self.success_count + self.failure_count
        return {
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'total_turn_count': self.total_turn_count,
            'total_execution_time': self.total_execution_time,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'average_input_tokens': self.total_input_tokens / total_executions if total_executions > 0 else 0,
            'average_output_tokens': self.total_output_tokens / total_executions if total_executions > 0 else 0,
            'average_tokens': self.total_tokens / total_executions if total_executions > 0 else 0,
            'average_turn_count': self.total_turn_count / total_executions if total_executions > 0 else 0,
            'average_execution_time': self.total_execution_time / total_executions if total_executions > 0 else 0.0,
            'success_rate': self.success_count / total_executions if total_executions > 0 else 0.0,
        }
