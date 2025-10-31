from typing import Dict, Any


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_runs: int = 0
        self.success_count: int = 0
        self.failure_count: int = 0

        # Totals across all runs
        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_tokens: int = 0
        self.total_turns: int = 0
        self.total_execution_time: float = 0.0

        # Totals for successful runs
        self.success_input_tokens: int = 0
        self.success_output_tokens: int = 0
        self.success_total_tokens: int = 0
        self.success_turns: int = 0
        self.success_execution_time: float = 0.0

        # Totals for failed runs
        self.failure_input_tokens: int = 0
        self.failure_output_tokens: int = 0
        self.failure_total_tokens: int = 0
        self.failure_turns: int = 0
        self.failure_execution_time: float = 0.0

        # Last run snapshot
        self.last_run: Dict[str, Any] = {}

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        # Extract and validate token usage
        input_tokens = int(token_usage.get("input_tokens", 0))
        output_tokens = int(token_usage.get("output_tokens", 0))
        total_tokens = int(token_usage.get(
            "total_tokens", input_tokens + output_tokens))

        if input_tokens < 0 or output_tokens < 0 or total_tokens < 0:
            raise ValueError("Token counts must be non-negative.")
        if turn_count < 0:
            raise ValueError("turn_count must be non-negative.")
        if execution_time < 0:
            raise ValueError("execution_time must be non-negative.")

        self.total_runs += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        # Update totals
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_tokens += total_tokens
        self.total_turns += int(turn_count)
        self.total_execution_time += float(execution_time)

        # Update per-outcome totals
        if success:
            self.success_input_tokens += input_tokens
            self.success_output_tokens += output_tokens
            self.success_total_tokens += total_tokens
            self.success_turns += int(turn_count)
            self.success_execution_time += float(execution_time)
        else:
            self.failure_input_tokens += input_tokens
            self.failure_output_tokens += output_tokens
            self.failure_total_tokens += total_tokens
            self.failure_turns += int(turn_count)
            self.failure_execution_time += float(execution_time)

        # Record last run snapshot
        self.last_run = {
            "success": success,
            "token_usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
            },
            "turn_count": int(turn_count),
            "execution_time": float(execution_time),
        }

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        runs = self.total_runs
        successes = self.success_count
        failures = self.failure_count

        def safe_div(n: float, d: int) -> float:
            return n / d if d else 0.0

        stats: Dict[str, Any] = {
            "runs": runs,
            "successes": successes,
            "failures": failures,
            "success_rate": safe_div(successes, runs),

            "totals": {
                "input_tokens": self.total_input_tokens,
                "output_tokens": self.total_output_tokens,
                "total_tokens": self.total_tokens,
                "turns": self.total_turns,
                "execution_time": self.total_execution_time,
            },

            "averages_per_run": {
                "input_tokens": safe_div(self.total_input_tokens, runs),
                "output_tokens": safe_div(self.total_output_tokens, runs),
                "total_tokens": safe_div(self.total_tokens, runs),
                "turns": safe_div(self.total_turns, runs),
                "execution_time": safe_div(self.total_execution_time, runs),
            },

            "totals_success": {
                "input_tokens": self.success_input_tokens,
                "output_tokens": self.success_output_tokens,
                "total_tokens": self.success_total_tokens,
                "turns": self.success_turns,
                "execution_time": self.success_execution_time,
            },
            "averages_per_success": {
                "input_tokens": safe_div(self.success_input_tokens, successes),
                "output_tokens": safe_div(self.success_output_tokens, successes),
                "total_tokens": safe_div(self.success_total_tokens, successes),
                "turns": safe_div(self.success_turns, successes),
                "execution_time": safe_div(self.success_execution_time, successes),
            },

            "totals_failure": {
                "input_tokens": self.failure_input_tokens,
                "output_tokens": self.failure_output_tokens,
                "total_tokens": self.failure_total_tokens,
                "turns": self.failure_turns,
                "execution_time": self.failure_execution_time,
            },
            "averages_per_failure": {
                "input_tokens": safe_div(self.failure_input_tokens, failures),
                "output_tokens": safe_div(self.failure_output_tokens, failures),
                "total_tokens": safe_div(self.failure_total_tokens, failures),
                "turns": safe_div(self.failure_turns, failures),
                "execution_time": safe_div(self.failure_execution_time, failures),
            },

            "last_run": self.last_run,
        }

        return stats
