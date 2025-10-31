
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.total_success_count = 0
        self.total_failure_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_success_count = 0
        self.total_failure_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turn_count = 0
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
        if success:
            self.total_success_count += 1
        else:
            self.total_failure_count += 1

        self.total_input_tokens += token_usage['input_tokens']
        self.total_output_tokens += token_usage['output_tokens']
        self.total_tokens += token_usage['total_tokens']
        self.total_turn_count += turn_count
        self.total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        total_count = self.total_success_count + self.total_failure_count
        stats = {
            'success_count': self.total_success_count,
            'failure_count': self.total_failure_count,
            'total_count': total_count,
            'success_rate': self.total_success_count / total_count if total_count > 0 else 0.0,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'avg_input_tokens': self.total_input_tokens / total_count if total_count > 0 else 0,
            'avg_output_tokens': self.total_output_tokens / total_count if total_count > 0 else 0,
            'avg_tokens': self.total_tokens / total_count if total_count > 0 else 0,
            'total_turn_count': self.total_turn_count,
            'avg_turn_count': self.total_turn_count / total_count if total_count > 0 else 0,
            'total_execution_time': self.total_execution_time,
            'avg_execution_time': self.total_execution_time / total_count if total_count > 0 else 0.0,
        }
        return stats
