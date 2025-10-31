
from typing import Dict, Any


class TokenUsageTracker:
    """
    Tracks token usage statistics across multiple turns and executions.
    """

    def __init__(self):
        """
        Initializes all counters and accumulators.
        """
        self.reset()

    def reset(self):
        """
        Resets all statistics to their initial state.
        """
        self.total_successes: int = 0
        self.total_failures: int = 0
        self.total_turns: int = 0
        self.total_execution_time: float = 0.0
        self.token_counts: Dict[str, int] = {}
        self.total_tokens: int = 0

    def update(
        self,
        success: bool,
        token_usage: Dict[str, int],
        turn_count: int,
        execution_time: float,
    ):
        """
        Updates statistics with data from a single execution.

        Parameters
        ----------
        success : bool
            Whether the execution was successful.
        token_usage : Dict[str, int]
            Mapping from token type to the number of tokens used in this execution.
        turn_count : int
            Number of turns processed in this execution.
        execution_time : float
            Time taken for this execution (in seconds).
        """
        # Update success/failure counters
        if success:
            self.total_successes += 1
        else:
            self.total_failures += 1

        # Update turn and time counters
        self.total_turns += turn_count
        self.total_execution_time += execution_time

        # Update token usage counters
        for token_type, count in token_usage.items():
            self.token_counts[token_type] = self.token_counts.get(
                token_type, 0) + count
            self.total_tokens += count

    def get_stats(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing aggregated statistics.

        Returns
        -------
        Dict[str, Any]
            Dictionary with keys:
                - total_successes
                - total_failures
                - total_turns
                - total_execution_time
                - average_execution_time
                - success_rate
                - total_tokens
                - average_tokens_per_type (dict)
                - token_counts
        """
        if self.total_turns == 0:
            avg_exec_time = 0.0
            success_rate = 0.0
        else:
            avg_exec_time = self.total_execution_time / self.total_turns
            success_rate = self.total_successes / self.total_turns

        avg_tokens_per_type: Dict[str, float] = {}
        if self.total_turns > 0:
            for token_type, count in self.token_counts.items():
                avg_tokens_per_type[token_type] = count / self.total_turns

        return {
            "total_successes": self.total_successes,
            "total_failures": self.total_failures,
            "total_turns": self.total_turns,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": avg_exec_time,
            "success_rate": success_rate,
            "total_tokens": self.total_tokens,
            "average_tokens_per_type": avg_tokens_per_type,
            "token_counts": dict(self.token_counts),
        }
