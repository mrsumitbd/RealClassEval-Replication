from typing import Any, Dict


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.runs = 0
        self.successes = 0
        self.failures = 0

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
        self.runs += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1

        in_tokens = int(token_usage.get("input_tokens", 0) or 0)
        out_tokens = int(token_usage.get("output_tokens", 0) or 0)
        total_tokens = token_usage.get("total_tokens")
        if total_tokens is None:
            total_tokens = in_tokens + out_tokens
        total_tokens = int(total_tokens or 0)

        self.total_input_tokens += max(0, in_tokens)
        self.total_output_tokens += max(0, out_tokens)
        self.total_tokens += max(0, total_tokens)

        self.total_turns += int(max(0, turn_count))
        try:
            exec_time = float(execution_time)
        except (TypeError, ValueError):
            exec_time = 0.0
        self.total_execution_time += max(0.0, exec_time)

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        runs = self.runs if self.runs > 0 else 1  # avoid division by zero for averages
        success_count = self.successes if self.successes > 0 else 1  # for per-success averages

        stats = {
            "runs": self.runs,
            "successes": self.successes,
            "failures": self.failures,
            "success_rate": (self.successes / self.runs) if self.runs > 0 else 0.0,

            "totals": {
                "input_tokens": self.total_input_tokens,
                "output_tokens": self.total_output_tokens,
                "total_tokens": self.total_tokens,
                "turns": self.total_turns,
                "execution_time": self.total_execution_time,
            },

            "averages_per_run": {
                "input_tokens": self.total_input_tokens / runs,
                "output_tokens": self.total_output_tokens / runs,
                "total_tokens": self.total_tokens / runs,
                "turns": self.total_turns / runs,
                "execution_time": self.total_execution_time / runs,
            },

            "averages_per_success": {
                "input_tokens": (self.total_input_tokens / success_count) if self.successes > 0 else 0.0,
                "output_tokens": (self.total_output_tokens / success_count) if self.successes > 0 else 0.0,
                "total_tokens": (self.total_tokens / success_count) if self.successes > 0 else 0.0,
                "turns": (self.total_turns / success_count) if self.successes > 0 else 0.0,
                "execution_time": (self.total_execution_time / success_count) if self.successes > 0 else 0.0,
            },
        }
        return stats
