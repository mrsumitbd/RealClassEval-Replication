from typing import Any, Dict


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self):
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self):
        '''Reset all usage statistics.'''
        self._runs: int = 0
        self._successes: int = 0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_tokens: int = 0
        self._total_turns: int = 0
        self._total_time: float = 0.0

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

        input_tokens = int(token_usage.get(
            'input_tokens', 0)) if token_usage else 0
        output_tokens = int(token_usage.get(
            'output_tokens', 0)) if token_usage else 0
        total_tokens = token_usage.get('total_tokens')
        if total_tokens is None:
            total_tokens = input_tokens + output_tokens
        total_tokens = int(total_tokens)

        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._total_tokens += total_tokens

        self._total_turns += int(turn_count)
        self._total_time += float(execution_time)

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        runs = self._runs
        successes = self._successes
        failures = runs - successes
        success_rate = (successes / runs) if runs > 0 else 0.0

        total_turns = self._total_turns
        total_time = self._total_time
        total_input = self._total_input_tokens
        total_output = self._total_output_tokens
        total_tokens = self._total_tokens

        avg_input_per_run = (total_input / runs) if runs > 0 else 0.0
        avg_output_per_run = (total_output / runs) if runs > 0 else 0.0
        avg_total_per_run = (total_tokens / runs) if runs > 0 else 0.0

        avg_turns_per_run = (total_turns / runs) if runs > 0 else 0.0

        avg_time_per_run = (total_time / runs) if runs > 0 else 0.0
        avg_time_per_turn = (
            total_time / total_turns) if total_turns > 0 else 0.0

        avg_input_per_turn = (
            total_input / total_turns) if total_turns > 0 else 0.0
        avg_output_per_turn = (
            total_output / total_turns) if total_turns > 0 else 0.0
        avg_total_per_turn = (
            total_tokens / total_turns) if total_turns > 0 else 0.0

        return {
            'runs': runs,
            'successes': successes,
            'failures': failures,
            'success_rate': success_rate,
            'tokens': {
                'total_input_tokens': total_input,
                'total_output_tokens': total_output,
                'total_tokens': total_tokens,
                'avg_input_tokens_per_run': avg_input_per_run,
                'avg_output_tokens_per_run': avg_output_per_run,
                'avg_total_tokens_per_run': avg_total_per_run,
                'avg_input_tokens_per_turn': avg_input_per_turn,
                'avg_output_tokens_per_turn': avg_output_per_turn,
                'avg_total_tokens_per_turn': avg_total_per_turn,
            },
            'turns': {
                'total_turns': total_turns,
                'avg_turns_per_run': avg_turns_per_run,
            },
            'time': {
                'total_seconds': total_time,
                'avg_seconds_per_run': avg_time_per_run,
                'avg_seconds_per_turn': avg_time_per_turn,
            },
        }
