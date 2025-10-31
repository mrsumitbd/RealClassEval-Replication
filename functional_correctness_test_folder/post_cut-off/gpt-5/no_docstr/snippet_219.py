from typing import Dict, Any, Optional
from copy import deepcopy


class TokenUsageTracker:
    def __init__(self):
        self.reset()

    def reset(self):
        self.total_calls: int = 0
        self.success_count: int = 0
        self.failure_count: int = 0

        self.total_turns: int = 0
        self.min_turns: Optional[int] = None
        self.max_turns: Optional[int] = None

        self.total_execution_time: float = 0.0
        self.min_execution_time: Optional[float] = None
        self.max_execution_time: Optional[float] = None

        self.total_token_usage: Dict[str, int] = {}
        self.total_tokens: int = 0

        self.success_turns: int = 0
        self.success_tokens: int = 0
        self.success_exec_time: float = 0.0

        self.last_call: Optional[Dict[str, Any]] = None

    def update(self, success: bool, token_usage: Dict[str, int], turn_count: int, execution_time: float):
        self.total_calls += 1
        if success:
            self.success_count += 1
            self.success_turns += turn_count
            self.success_tokens += sum(token_usage.values())
            self.success_exec_time += execution_time
        else:
            self.failure_count += 1

        self.total_turns += turn_count
        self.min_turns = turn_count if self.min_turns is None else min(
            self.min_turns, turn_count)
        self.max_turns = turn_count if self.max_turns is None else max(
            self.max_turns, turn_count)

        self.total_execution_time += execution_time
        self.min_execution_time = execution_time if self.min_execution_time is None else min(
            self.min_execution_time, execution_time)
        self.max_execution_time = execution_time if self.max_execution_time is None else max(
            self.max_execution_time, execution_time)

        for k, v in token_usage.items():
            self.total_token_usage[k] = self.total_token_usage.get(
                k, 0) + int(v)
        call_total_tokens = sum(token_usage.values())
        self.total_tokens += call_total_tokens

        self.last_call = {
            "success": success,
            "token_usage": deepcopy(token_usage),
            "turn_count": turn_count,
            "execution_time": execution_time,
            "total_tokens": call_total_tokens,
        }

    def get_stats(self) -> Dict[str, Any]:
        total = self.total_calls if self.total_calls else 1
        succ = self.success_count if self.success_count else 1

        return {
            "total_calls": self.total_calls,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": (self.success_count / self.total_calls) if self.total_calls else 0.0,
            "turns": {
                "total": self.total_turns,
                "min": self.min_turns,
                "max": self.max_turns,
                "avg_per_call": (self.total_turns / self.total_calls) if self.total_calls else 0.0,
                "avg_per_success": (self.success_turns / self.success_count) if self.success_count else 0.0,
            },
            "execution_time": {
                "total": self.total_execution_time,
                "min": self.min_execution_time,
                "max": self.max_execution_time,
                "avg_per_call": (self.total_execution_time / self.total_calls) if self.total_calls else 0.0,
                "avg_per_success": (self.success_exec_time / self.success_count) if self.success_count else 0.0,
            },
            "tokens": {
                "by_type_total": deepcopy(self.total_token_usage),
                "total": self.total_tokens,
                "avg_per_call": (self.total_tokens / self.total_calls) if self.total_calls else 0.0,
                "avg_per_success": (self.success_tokens / self.success_count) if self.success_count else 0.0,
            },
            "last_call": deepcopy(self.last_call),
        }
