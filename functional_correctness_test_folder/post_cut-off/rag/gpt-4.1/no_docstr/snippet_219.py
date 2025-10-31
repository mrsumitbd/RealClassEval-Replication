from typing import Dict, Any, List


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
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
        self._history: List[Dict[str, Any]] = []

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

        input_tokens = token_usage.get("input_tokens", 0)
        output_tokens = token_usage.get("output_tokens", 0)
        total_tokens = token_usage.get(
            "total_tokens", input_tokens + output_tokens)

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_tokens += total_tokens
        self.total_turns += turn_count
        self.total_execution_time += execution_time

        self._history.append({
            "success": success,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "turn_count": turn_count,
            "execution_time": execution_time,
        })

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        stats = {
            "total_runs": self.total_runs,
            "successful_runs": self.successful_runs,
            "failed_runs": self.failed_runs,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_turns": self.total_turns,
            "total_execution_time": self.total_execution_time,
            "average_input_tokens": self.total_input_tokens / self.total_runs if self.total_runs else 0,
            "average_output_tokens": self.total_output_tokens / self.total_runs if self.total_runs else 0,
            "average_total_tokens": self.total_tokens / self.total_runs if self.total_runs else 0,
            "average_turns": self.total_turns / self.total_runs if self.total_runs else 0,
            "average_execution_time": self.total_execution_time / self.total_runs if self.total_runs else 0,
            "success_rate": self.successful_runs / self.total_runs if self.total_runs else 0,
            "history": list(self._history),
        }
        return stats
