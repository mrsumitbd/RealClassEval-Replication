from typing import Optional, Callable, Union
from threedgrut.model.model import MixtureOfGaussians
import torch

class BaseStrategy:

    def __init__(self, config, model: MixtureOfGaussians) -> None:
        self.conf = config
        self.model = model

    def init_densification_buffer(self, checkpoint: Optional[dict]=None):
        """Callback function to initialize the densification buffers."""
        pass

    def pre_backward(self, step: int, scene_extent: float, train_dataset, batch=None, writer=None) -> bool:
        """Callback function to be executed before the `loss.backward()` call."""
        return False

    def post_backward(self, step: int, scene_extent: float, train_dataset, batch=None, writer=None) -> bool:
        """Callback function to be executed after the `loss.backward()` call."""
        return False

    def post_optimizer_step(self, step: int, scene_extent: float, train_dataset, batch=None, writer=None) -> bool:
        """Callback function to be executed after the optimizer step."""
        return False

    def update_gradient_buffer(self, sensor_position: torch.Tensor) -> None:
        """Callback function to update the gradient buffer."""
        pass

    def get_strategy_parameters(self) -> dict:
        """Callback function to get the strategy parameters."""
        return {}

    @torch.no_grad()
    def _update_param_with_optimizer(self, update_param_fn: Callable[[str, torch.Tensor], torch.Tensor] | None, update_optimizer_fn: Callable[[str, torch.Tensor], torch.Tensor] | None, names: Union[list[str], None]=None) -> None:
        """Update the parameters and the state in the optimizers using the provided lambda functions.

        Args:
            update_param_fn: A function that takes the name of the parameter and the parameter itself,
                and returns the new parameter.
            optimizer_fn: A function that takes the key of the optimizer state and the state value,
                and returns the new state value.
            names: A list of key names to update. If None, update all. Default: None.
        """
        for i, param_group in enumerate(self.model.optimizer.param_groups):
            name = param_group['name']
            if names is None or name in names:
                p = param_group['params'][0]
                p_state = self.model.optimizer.state[p]
                del self.model.optimizer.state[p]
                for key in p_state.keys():
                    if key != 'step':
                        v = p_state[key]
                        if update_optimizer_fn is not None:
                            p_state[key] = update_optimizer_fn(key, v)
                if update_param_fn is not None:
                    p_new = update_param_fn(name, p)
                    self.model.optimizer.param_groups[i]['params'] = [p_new]
                    self.model.optimizer.state[p_new] = p_state
                    setattr(self.model, name, p_new)