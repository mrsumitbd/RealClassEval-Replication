from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Rollout:
    payload: Any
    completion: str
    is_end: bool
    reward: float
    advantage: float
    prompt_idx: int
    n_ignore_prefix_tokens: int = 0

    def __init__(self, payload: Any, completion: str, is_end: bool, reward: float, advantage: float, prompt_idx: int, n_ignore_prefix_tokens: int=0):
        self.payload = payload
        self.completion = completion
        self.is_end = is_end
        self.reward = reward
        self.advantage = advantage
        self.prompt_idx = prompt_idx
        self.n_ignore_prefix_tokens = n_ignore_prefix_tokens

    @classmethod
    def from_dict(cls, dict_v: Dict[str, Any]) -> 'Rollout':
        return cls(**dict_v)