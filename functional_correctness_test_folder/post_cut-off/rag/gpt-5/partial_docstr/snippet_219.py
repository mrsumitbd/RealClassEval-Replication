from typing import Any, Dict


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self._runs = 0
        self._successes = 0
        self._failures = 0

        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_tokens = 0

        self._total_turns = 0
        self._total_time = 0.0

        self._last = {
            'success': None,
            'token_usage': None,
            'turn_count': None,
            'execution_time': None,
        }

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        self._runs += 1
        if success:
            self._successes += 1
        else:
            self._failures += 1

        input_tokens = int(token_usage.get('input_tokens', 0))
        output_tokens = int(token_usage.get('output_tokens', 0))
        total_tokens = int(token_usage.get(
            'total_tokens', input_tokens + output_tokens))

        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._total_tokens += total_tokens

        self._total_turns += int(turn_count)
        self._total_time += float(execution_time)

        self._last = {
            'success': success,
            'token_usage': {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': total_tokens,
            },
            'turn_count': int(turn_count),
            'execution_time': float(execution_time),
        }

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        runs = self._runs
        successes = self._successes
        failures = self._failures
        total_turns = self._total_turns
        total_time = self._total_time

        def avg(val: float, denom: int) -> float:
            return float(val) / denom if denom > 0 else 0.0

        stats: Dict[str, Any] = {
            'runs': runs,
            'successes': successes,
            'failures': failures,
            'success_rate': avg(successes, runs),

            'tokens': {
                'total_input_tokens': self._total_input_tokens,
                'total_output_tokens': self._total_output_tokens,
                'total_tokens': self._total_tokens,
                'avg_input_tokens_per_run': avg(self._total_input_tokens, runs),
                'avg_output_tokens_per_run': avg(self._total_output_tokens, runs),
                'avg_total_tokens_per_run': avg(self._total_tokens, runs),
                'avg_tokens_per_turn': avg(self._total_tokens, total_turns),
            },

            'turns': {
                'total_turns': total_turns,
                'avg_turns_per_run': avg(total_turns, runs),
            },

            'time': {
                'total_time_sec': total_time,
                'avg_time_per_run_sec': avg(total_time, runs),
            },

            'last_execution': self._last,
        }
        return stats
