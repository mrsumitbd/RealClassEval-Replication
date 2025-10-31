from itertools import chain as chain_iters
from typing import Callable, Dict, Optional, List
from protowhat.State import State

class ChainedCall:
    strict = False
    __slots__ = ('callable', 'args', 'kwargs')

    def __init__(self, callable_: Callable, args: Optional[tuple]=None, kwargs: Optional[dict]=None):
        """
        This contains the data for a function call that can be chained
        This means the chain state should only be provided when calling.
        """
        self.callable = link_to_state(callable_)
        self.args = args or ()
        self.kwargs = kwargs or {}
        if self.strict:
            self.validate()

    def validate(self) -> bool:
        """Can be used to check if the call data is valid without execution in the future."""
        raise NotImplementedError

    def __call__(self, state: State) -> State:
        return self.callable(state, *self.args, **self.kwargs)

    def __str__(self):
        return self.callable.__name__ + '(' + ', '.join(chain_iters((str(arg) for arg in self.args), ('{}={}'.format(kwarg, value) for kwarg, value in self.kwargs.items()))) + ')'