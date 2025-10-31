from typing import Any, Dict, Optional


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self.total_runs: int = 0
        self.successful_runs: int = 0
        self.failed_runs: int = 0

        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_tokens: int = 0

        self.total_turns: int = 0
        self.total_execution_time: float = 0.0

        self.min_input_tokens: Optional[int] = None
        self.min_output_tokens: Optional[int] = None
        self.min_total_tokens: Optional[int] = None
        self.min_turns: Optional[int] = None
        self.min_execution_time: Optional[float] = None

        self.max_input_tokens: int = 0
        self.max_output_tokens: int = 0
        self.max_total_tokens: int = 0
        self.max_turns: int = 0
        self.max_execution_time: float = 0.0

        self.last: Optional[Dict[str, Any]] = None

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        '''
        Update usage statistics.
        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        '''
        input_tokens = int(token_usage.get('input_tokens', 0) or 0)
        output_tokens = int(token_usage.get('output_tokens', 0) or 0)
        total_tokens = int(token_usage.get(
            'total_tokens', input_tokens + output_tokens) or (input_tokens + output_tokens))

        turn_count = int(
            max(0, int(turn_count if turn_count is not None else 0)))
        execution_time = float(
            max(0.0, float(execution_time if execution_time is not None else 0.0)))

        self.total_runs += 1
        if success:
            self.successful_runs += 1
        else:
            self.failed_runs += 1

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_tokens += total_tokens

        self.total_turns += turn_count
        self.total_execution_time += execution_time

        def _min_update(curr, val):
            return val if curr is None or val < curr else curr

        self.min_input_tokens = _min_update(
            self.min_input_tokens, input_tokens)
        self.min_output_tokens = _min_update(
            self.min_output_tokens, output_tokens)
        self.min_total_tokens = _min_update(
            self.min_total_tokens, total_tokens)
        self.min_turns = _min_update(self.min_turns, turn_count)
        self.min_execution_time = _min_update(
            self.min_execution_time, execution_time)

        self.max_input_tokens = max(self.max_input_tokens, input_tokens)
        self.max_output_tokens = max(self.max_output_tokens, output_tokens)
        self.max_total_tokens = max(self.max_total_tokens, total_tokens)
        self.max_turns = max(self.max_turns, turn_count)
        self.max_execution_time = max(self.max_execution_time, execution_time)

        self.last = {
            'success': success,
            'token_usage': {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': total_tokens,
            },
            'turn_count': turn_count,
            'execution_time': execution_time,
        }

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        runs = self.total_runs

        def avg(numer, denom):
            return float(numer) / denom if denom else 0.0

        stats: Dict[str, Any] = {
            'runs': runs,
            'successes': self.successful_runs,
            'failures': self.failed_runs,
            'success_rate': avg(self.successful_runs, runs),
            'turns': {
                'total': self.total_turns,
                'avg_per_run': avg(self.total_turns, runs),
                'min': self.min_turns if self.min_turns is not None else 0,
                'max': self.max_turns,
            },
            'execution_time': {
                'total_seconds': self.total_execution_time,
                'avg_seconds_per_run': avg(self.total_execution_time, runs),
                'min_seconds': self.min_execution_time if self.min_execution_time is not None else 0.0,
                'max_seconds': self.max_execution_time,
                'throughput_tokens_per_second': (self.total_tokens / self.total_execution_time) if self.total_execution_time > 0 else 0.0,
            },
            'tokens': {
                'input': {
                    'total': self.total_input_tokens,
                    'avg_per_run': avg(self.total_input_tokens, runs),
                    'avg_per_turn': avg(self.total_input_tokens, self.total_turns),
                    'min': self.min_input_tokens if self.min_input_tokens is not None else 0,
                    'max': self.max_input_tokens,
                },
                'output': {
                    'total': self.total_output_tokens,
                    'avg_per_run': avg(self.total_output_tokens, runs),
                    'avg_per_turn': avg(self.total_output_tokens, self.total_turns),
                    'min': self.min_output_tokens if self.min_output_tokens is not None else 0,
                    'max': self.max_output_tokens,
                },
                'total': {
                    'total': self.total_tokens,
                    'avg_per_run': avg(self.total_tokens, runs),
                    'avg_per_turn': avg(self.total_tokens, self.total_turns),
                    'min': self.min_total_tokens if self.min_total_tokens is not None else 0,
                    'max': self.max_total_tokens,
                },
            },
            'last': self.last,
        }
        return stats
