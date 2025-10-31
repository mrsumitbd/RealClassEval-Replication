
class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self._total_executions = 0
        self._successful_executions = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_tokens = 0
        self._total_turns = 0
        self._total_execution_time = 0.0

    def reset(self):
        '''Reset all usage statistics.'''
        self._total_executions = 0
        self._successful_executions = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_tokens = 0
        self._total_turns = 0
        self._total_execution_time = 0.0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        self._total_executions += 1
        if success:
            self._successful_executions += 1
        self._total_input_tokens += token_usage.get('input_tokens', 0)
        self._total_output_tokens += token_usage.get('output_tokens', 0)
        self._total_tokens += token_usage.get('total_tokens', 0)
        self._total_turns += turn_count
        self._total_execution_time += execution_time

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        if self._total_executions == 0:
            return {
                'total_executions': 0,
                'successful_executions': 0,
                'success_rate': 0.0,
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_tokens': 0,
                'total_turns': 0,
                'total_execution_time': 0.0,
                'avg_input_tokens': 0.0,
                'avg_output_tokens': 0.0,
                'avg_total_tokens': 0.0,
                'avg_turns': 0.0,
                'avg_execution_time': 0.0
            }

        return {
            'total_executions': self._total_executions,
            'successful_executions': self._successful_executions,
            'success_rate': self._successful_executions / self._total_executions,
            'total_input_tokens': self._total_input_tokens,
            'total_output_tokens': self._total_output_tokens,
            'total_tokens': self._total_tokens,
            'total_turns': self._total_turns,
            'total_execution_time': self._total_execution_time,
            'avg_input_tokens': self._total_input_tokens / self._total_executions,
            'avg_output_tokens': self._total_output_tokens / self._total_executions,
            'avg_total_tokens': self._total_tokens / self._total_executions,
            'avg_turns': self._total_turns / self._total_executions,
            'avg_execution_time': self._total_execution_time / self._total_executions
        }
