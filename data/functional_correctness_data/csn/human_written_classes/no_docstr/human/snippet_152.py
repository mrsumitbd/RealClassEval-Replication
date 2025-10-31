from typing import Callable, Iterable

class BoolBinOp:
    repr_symbol: str = ''
    eval_fn: Callable[[Iterable[bool]], bool] = lambda _: False

    def __init__(self, t):
        self.args = t[0][0::2]

    def __str__(self) -> str:
        sep = f' {self.repr_symbol} '
        return f'({sep.join(map(str, self.args))})'

    def __bool__(self) -> bool:
        return self.eval_fn((bool(a) for a in self.args))