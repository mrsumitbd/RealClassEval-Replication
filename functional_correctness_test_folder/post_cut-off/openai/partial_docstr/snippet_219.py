
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_executions: int = 0
        self.successful_executions: int = 0
        self.failed_executions: int = 0
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
            self.successful_executions += 1
        else:
            self.failed_executions += 1

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
            success_rate = self.successful_executions / self.total_executions

        return {
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_turns": self.total_turns,
            "total_execution_time": self.total_execution_time,
            "average_input_tokens": avg_input,
            "average_output_tokens": avg_output,
            "average_total_tokens": avg_total,
            "average_turns_per_execution": avg_turns,
            "average_execution_time": avg_time,
            "success_rate": success_rate,
        }
