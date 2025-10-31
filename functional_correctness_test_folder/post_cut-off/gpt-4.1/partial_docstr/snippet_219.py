
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_runs = 0
        self.successful_runs = 0
        self.failed_runs = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turns = 0
        self.total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        self.total_runs += 1
        if success:
            self.successful_runs += 1
        else:
            self.failed_runs += 1

        self.total_input_tokens += token_usage.get('input_tokens', 0)
        self.total_output_tokens += token_usage.get('output_tokens', 0)
        self.total_tokens += token_usage.get('total_tokens', 0)
        self.total_turns += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        if self.total_runs == 0:
            avg_input_tokens = 0
            avg_output_tokens = 0
            avg_total_tokens = 0
            avg_turns = 0
            avg_execution_time = 0.0
            success_rate = 0.0
        else:
            avg_input_tokens = self.total_input_tokens / self.total_runs
            avg_output_tokens = self.total_output_tokens / self.total_runs
            avg_total_tokens = self.total_tokens / self.total_runs
            avg_turns = self.total_turns / self.total_runs
            avg_execution_time = self.total_execution_time / self.total_runs
            success_rate = self.successful_runs / self.total_runs

        return {
            'total_runs': self.total_runs,
            'successful_runs': self.successful_runs,
            'failed_runs': self.failed_runs,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'total_turns': self.total_turns,
            'total_execution_time': self.total_execution_time,
            'avg_input_tokens': avg_input_tokens,
            'avg_output_tokens': avg_output_tokens,
            'avg_total_tokens': avg_total_tokens,
            'avg_turns': avg_turns,
            'avg_execution_time': avg_execution_time,
            'success_rate': success_rate
        }
