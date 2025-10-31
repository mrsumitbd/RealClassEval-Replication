
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        self.total_success = 0
        self.total_failures = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0
        self.execution_count = 0

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_success = 0
        self.total_failures = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.total_turn_count = 0
        self.total_execution_time = 0.0
        self.execution_count = 0

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
            self.total_success += 1
        else:
            self.total_failures += 1

        self.total_input_tokens += token_usage['input_tokens']
        self.total_output_tokens += token_usage['output_tokens']
        self.total_tokens += token_usage['total_tokens']
        self.total_turn_count += turn_count
        self.total_execution_time += execution_time
        self.execution_count += 1

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        stats = {
            'total_success': self.total_success,
            'total_failures': self.total_failures,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'total_turn_count': self.total_turn_count,
            'total_execution_time': self.total_execution_time,
            'execution_count': self.execution_count,
        }

        if self.execution_count > 0:
            stats['average_input_tokens'] = self.total_input_tokens / \
                self.execution_count
            stats['average_output_tokens'] = self.total_output_tokens / \
                self.execution_count
            stats['average_tokens'] = self.total_tokens / self.execution_count
            stats['average_turn_count'] = self.total_turn_count / \
                self.execution_count
            stats['average_execution_time'] = self.total_execution_time / \
                self.execution_count
            stats['success_rate'] = self.total_success / self.execution_count

        return stats
