import torch.distributed as dist
import torch
from dataclasses import dataclass

@dataclass
class _LossRecord:
    iter_count: int = 0
    loss: float = 0

    def reset(self) -> None:
        self.iter_count = 0
        self.loss = 0

    def get_stat(self) -> tuple[float, float]:
        if self.iter_count > 0:
            loss = self.loss / self.iter_count
            dist.all_reduce(loss, op=dist.ReduceOp.AVG)
        else:
            loss = torch.ones(1)
        iter_count = self.iter_count
        self.reset()
        return (loss.tolist(), iter_count)