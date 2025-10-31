
from __future__ import annotations

from typing import Any, Dict


class TokenUsageTracker:
    """Track token usage across agent executions."""

    def __init__(self) -> None:
        """Initialize token usage tracker."""
        self.reset()

    def reset(self) -> None:
        """Reset all usage statistics."""
        self._total_success: int = 0
        self._total_fail: int = 0
        self._total_executions: int = 0
        self._total_turns: int = 0
        self._total_execution_time: float = 0.0
        self._sum_input_tokens: int = 0
        self._sum_output_tokens: int = 0
        self._sum_total_tokens: int = 0

    def update(
        self,
        success: bool,
        token_usage: Dict[str, int],
        turn_count: int,
        execution_time: float,
    ) -> None:
        """
        Update usage statistics.

        Args:
            success: Whether execution was successful
            token_usage: Token usage dict with input_tokens, output_tokens, total_tokens
            turn_count: Number of conversation turns
            execution_time: Execution time in seconds
        """
        if success:
            self._total_success += 1
        else:
            self._total_fail += 1

        self._total_executions = self._total_success + self._total_fail
        self._total_turns += turn_count
        self._total_execution_time += execution_time

        self._sum_input_tokens += token_usage.get("input_tokens", 0)
        self._sum_output_tokens += token_usage.get("output_tokens", 0)
        self._sum_total_tokens += token_usage.get("total_tokens", 0)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics with calculated averages.

        Returns:
            Dictionary containing usage statistics
        """
        avg_input_per_turn = (
            self._sum_input_tokens / self._total_turns
            if self._total_turns
            else 0.0
        )
        avg_output_per_turn = (
            self._sum_output_tokens / self._total_turns
            if self._total_turns
            else 0.0
        )
        avg_total_per_turn = (
            self._sum_total_tokens / self._total_turns
            if self._total_turns
            else 0.0
        )
        avg_execution_time_per_success = (
            self._total_execution_time / self._total_success
            if self._total_success
            else 0.0
        )
        avg_execution_time_per_execution = (
            self._total_execution_time / self._total_executions
            if self._total_executions
            else 0.0
        )

        return {
            "total_success": self._total_success,
            "total_fail": self._total_fail,
            "total_executions": self._total_executions,
            "total_turns": self._total_turns,
            "total_execution_time": self._total_execution_time,
            "avg_input_tokens_per_turn": avg_input_per_turn,
            "avg_output_tokens_per_turn": avg_output_per_turn,
            "avg_total_tokens_per_turn": avg_total_per_turn,
            "avg_execution_time_per_success": avg_execution_time_per_success,
            "avg_execution_time_per_execution": avg_execution_time_per_execution,
            "sum_input_tokens": self._sum_input_tokens,
            "sum_output_tokens": self._sum_output_tokens,
            "sum_total_tokens": self._sum_total_tokens,
        }
