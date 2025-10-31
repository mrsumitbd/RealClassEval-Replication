
from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.total_turns = 0
        self.total_execution_time = 0.0
        self.execution_count = 0

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.total_turns = 0
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
        self.total_input_tokens += token_usage.get('input_tokens', 0)
        self.total_output_tokens += token_usage.get('output_tokens', 0)
        self.total_tokens += token_usage.get('total_tokens', 0)
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        self.total_turns += turn_count
        self.total_execution_time += execution_time
        self.execution_count += 1

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        avg_tokens_per_execution = self.total_tokens / \
            self.execution_count if self.execution_count > 0 else 0
        avg_turns_per_execution = self.total_turns / \
            self.execution_count if self.execution_count > 0 else 0
        avg_execution_time = self.total_execution_time / \
            self.execution_count if self.execution_count > 0 else 0

        return {
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'successful_executions': self.successful_executions,
            'failed_executions': self.failed_executions,
            'total_turns': self.total_turns,
            'total_execution_time': self.total_execution_time,
            'execution_count': self.execution_count,
            'avg_tokens_per_execution': avg_tokens_per_execution,
            'avg_turns_per_execution': avg_turns_per_execution,
            'avg_execution_time': avg_execution_time,
            'success_rate': self.successful_executions / self.execution_count if self.execution_count > 0 else 0
        }
