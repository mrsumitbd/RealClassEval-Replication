from typing import Dict, Any, List


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self._executions: List[Dict[str, Any]] = []
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_tokens = 0
        self._total_turns = 0
        self._total_time = 0.0
        self._successes = 0
        self._failures = 0

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        self._executions.append({
            "success": success,
            "input_tokens": token_usage.get("input_tokens", 0),
            "output_tokens": token_usage.get("output_tokens", 0),
            "total_tokens": token_usage.get("total_tokens", 0),
            "turn_count": turn_count,
            "execution_time": execution_time,
        })
        self._total_input_tokens += token_usage.get("input_tokens", 0)
        self._total_output_tokens += token_usage.get("output_tokens", 0)
        self._total_tokens += token_usage.get("total_tokens", 0)
        self._total_turns += turn_count
        self._total_time += execution_time
        if success:
            self._successes += 1
        else:
            self._failures += 1

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        count = len(self._executions)
        stats = {
            "executions": count,
            "successes": self._successes,
            "failures": self._failures,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens": self._total_tokens,
            "total_turns": self._total_turns,
            "total_time": self._total_time,
            "avg_input_tokens": self._total_input_tokens / count if count else 0,
            "avg_output_tokens": self._total_output_tokens / count if count else 0,
            "avg_total_tokens": self._total_tokens / count if count else 0,
            "avg_turns": self._total_turns / count if count else 0,
            "avg_time": self._total_time / count if count else 0,
            "success_rate": self._successes / count if count else 0,
        }
        return stats
