
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_executions: int = 0
        self.success_count: int = 0
        self.failure_count: int = 0
        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_tokens: int = 0
        self.total_turns: int = 0
        self.total_execution_time: float = 0.0

    def update(
        self,
        success: bool,
        token_usage: Dict[str, int],
        turn_count: int,
        execution_time: float,
    ):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        self.total_executions += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        self.total_input_tokens += token_usage.get("input_tokens", 0)
        self.total_output_tokens += token_usage.get("output_tokens", 0)
        self.total_tokens += token_usage.get("total_tokens", 0)

        self.total_turns += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        if self.total_executions == 0:
            avg_input = avg_output = avg_total = avg_turns = avg_time = 0.0
            success_rate = 0.0
        else:
            avg_input = self.total_input_tokens / self.total_executions
            avg_output = self.total_output_tokens / self.total_executions
            avg_total = self.total_tokens / self.total_executions
            avg_turns = self.total_turns / self.total_executions
            avg_time = self.total_execution_time / self.total_executions
            success_rate = self.success_count / self.total_executions

        return {
            "total_executions": self.total_executions,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_turns": self.total_turns,
            "total_execution_time": self.total_execution_time,
            "avg_input_tokens_per_execution": avg_input,
            "avg_output_tokens_per_execution": avg_output,
            "avg_total_tokens_per_execution": avg_total,
            "avg_turns_per_execution": avg_turns,
            "avg_execution_time_per_execution": avg_time,
            "success_rate": success_rate,
        }
