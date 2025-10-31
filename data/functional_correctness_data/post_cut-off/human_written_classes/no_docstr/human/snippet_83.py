from collections import defaultdict
from typing import Any, Callable, Sequence
from dataclasses import dataclass, field

@dataclass
class HivemindNode:
    model_name: str
    key: str
    is_coordinator: bool = False
    outputs: dict[Any, Any] = field(default_factory=dict)
    round_cache: dict[tuple[int, int], dict[str, tuple[float, dict]]] = field(default_factory=lambda: defaultdict(dict))
    rewards: Sequence[float | int] = field(default_factory=list)
    round_num: int = 0
    stage_num: int = 0
    out_expiration: int = 60 * 60 * 4

    @staticmethod
    def coordinator(*args, **kwargs):
        return HivemindNode(*args, **kwargs, is_coordinator=True)

    def get_stage_outputs(self, r, s) -> dict[str, tuple[float, dict]] | None:
        key = (r, s)
        if key in self.round_cache:
            return self.round_cache[key]

    def put_stage_outputs(self, r, s, question, value: tuple[float, dict]):
        self.round_cache[r, s][question] = value

    def clear_stage_cache(self):
        self.round_cache.clear()