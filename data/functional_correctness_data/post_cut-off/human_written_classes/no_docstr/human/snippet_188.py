from dataclasses import dataclass, field
from pytorch_fob.engine.utils import log_warn, some
from torch.nn.parameter import Parameter
from typing import Any, Callable, Iterable, Optional

@dataclass
class ParameterGroup:
    named_parameters: dict[str, Parameter]
    lr_multiplier: Optional[float] = field(default=None)
    weight_decay_multiplier: Optional[float] = field(default=None)
    optimizer_kwargs: dict[str, Any] = field(default_factory=dict)

    def __and__(self, other) -> 'ParameterGroup':
        assert isinstance(other, ParameterGroup)
        n1 = set(self.named_parameters.keys())
        n2 = set(other.named_parameters.keys())
        all_params = self.named_parameters | other.named_parameters
        n12 = n1 & n2
        new_params = {n: all_params[n] for n in n12}
        return ParameterGroup(named_parameters=new_params, lr_multiplier=some(other.lr_multiplier, default=self.lr_multiplier), weight_decay_multiplier=some(other.weight_decay_multiplier, default=self.weight_decay_multiplier), optimizer_kwargs=self.optimizer_kwargs | other.optimizer_kwargs)

    def __len__(self) -> int:
        return len(self.named_parameters)

    def __bool__(self) -> bool:
        return not self.empty()

    def empty(self) -> bool:
        return len(self.named_parameters) == 0

    def to_optimizer_dict(self, lr: Optional[float]=None, weight_decay: Optional[float]=None) -> dict[str, list[Parameter] | Any]:
        names = sorted(self.named_parameters)
        d = {'params': [self.named_parameters[n] for n in names], 'names': names, **self.optimizer_kwargs}
        if lr is not None:
            d['lr'] = self.lr_multiplier * lr if self.lr_multiplier is not None else lr
        if weight_decay is not None:
            d['weight_decay'] = self.weight_decay_multiplier * weight_decay if self.weight_decay_multiplier is not None else weight_decay
        return d