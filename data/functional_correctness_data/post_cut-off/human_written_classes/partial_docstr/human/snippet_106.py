from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union

@dataclass
class Sample:
    """The sample generated"""
    index: Optional[int] = None
    prompt: Union[str, list[dict[str, str]]] = ''
    tokens: list[int] = field(default_factory=list)
    response: str = ''
    response_length: int = 0
    label: Optional[str] = None
    reward: Optional[Union[float, dict[str, Any]]] = None
    loss_mask: Optional[list[int]] = None
    rollout_log_probs: Optional[list[float]] = None

    class Status(Enum):
        PENDING = 'pending'
        COMPLETED = 'completed'
        TRUNCATED = 'truncated'
        ABORTED = 'aborted'
    status: Status = Status.PENDING
    metadata: dict = field(default_factory=dict)
    train_metadata: Optional[dict] = None

    def to_dict(self):
        value = self.__dict__.copy()
        value['status'] = self.status.value
        return value

    @staticmethod
    def from_dict(data: dict):
        data['status'] = Sample.Status(data['status'])
        return Sample(**data)

    def get_reward_value(self, args) -> float:
        return self.reward if not args.reward_key else self.reward[args.reward_key]