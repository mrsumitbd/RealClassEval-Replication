
from __future__ import annotations

from typing import Any, Dict


class TokenUsageTracker:
    '''Track token usage across agent executions.'''

    def __init__(self) -> None:
        '''Initialize token usage tracker.'''
        self.reset()

    def reset(self) -> None:
        '''Reset all usage statistics.'''
        self._total_executions: int = 0
        self._successes: int = 0
        self._failures: int = 0
        self._total_turns: int = 0
        self._total_time: float = 0.0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_tokens: int = 0

    def update(
        self,
        success: bool,
        token_usage: Dict[str, int],
        turn_count: int,
        execution_time: float,
    ) -> None:
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
            self._successes += 1
        else:
            self._failures += 1

        self._total_turns += turn_count
        self._total_time += execution_time

        self._total_input_tokens += token_usage.get("input_tokens", 0)
        self._total_output_tokens += token_usage.get("output_tokens", 0)
        self._total_tokens += token_usage.get("total_tokens", 0)

    def get_stats(self) -> Dict[str, Any]:
        '''
        Get usage statistics with calculated averages.
        Returns:
            Dictionary containing usage statistics
        '''
        if self._total_executions == 0:
            avg_turns = 0.0
            avg_time = 0.0
            avg_input = 0.0
            avg_output = 0.0
            avg_total = 0.0
            success_rate = 0.0
        else:
            avg_turns = self._total_turns / self._total_executions
            avg_time = self._total_time / self._total_executions
            avg_input = self._total_input_tokens / self._total_executions
            avg_output = self._total_output_tokens / self._total_executions
            avg_total = self._total_tokens / self._total_executions
            success_rate = self._successes / self._total_executions

        return {
            "total_executions": self._total_executions,
            "successes": self._successes,
            "failures": self._failures,
            "success_rate": success_rate,
            "total_turns": self._total_turns,
            "avg_turns_per_execution": avg_turns,
            "total_time_seconds": self._total_time,
            "avg_time_seconds": avg_time,
            "total_input_tokens": self._total_input_tokens,
            "avg_input_tokens": avg_input,
            "total_output_tokens": self._total_output_tokens,
            "avg_output_tokens": avg_output,
            "total_tokens": self._total_tokens,
            "avg_total_tokens": avg_total,
        }
