from hidet.ir.expr import Constant, Equal, Expr, LogicalAnd, Mod, Var, as_expr
from typing import Any, Callable, Iterable, Literal, Optional, Sequence, Type, Union

class Attributes:
    """Attributes of the script program."""
    _blocks: Optional[Sequence[Expr | int] | Expr | int] = None
    _cluster_blocks: Optional[Sequence[Expr | int] | int] = (1, 1, 1)
    _warps: Optional[int] = None

    @property
    def blocks(self) -> Sequence[Expr | int] | Expr | int | None:
        """The number of blocks."""
        return self._blocks

    @blocks.setter
    def blocks(self, value: Sequence[Expr | int] | Expr | int) -> None:
        if not (isinstance(value, Sequence) and len(value) in [1, 2, 3]) and (not isinstance(value, (int, Expr))):
            raise ValueError('Expect 1d/2d/3d number of blocks, got {}'.format(value))
        self._blocks = value

    @property
    def cluster_blocks(self) -> Sequence[Expr | int] | int | None:
        """The number of blocks per cluster."""
        return self._cluster_blocks

    @cluster_blocks.setter
    def cluster_blocks(self, value: Sequence[Expr | int] | int) -> None:
        """The number of blocks per cluster."""
        if not isinstance(value, (int, Constant)) and (not (isinstance(value, Sequence) and all((isinstance(v, (int, Constant)) for v in value)))):
            raise ValueError('The number of blocks per cluster must be an integer or a sequence of integers')
        self._cluster_blocks = value

    @property
    def warps(self) -> Optional[int]:
        """The number of warps."""
        return self._warps

    @warps.setter
    def warps(self, value: int) -> None:
        if value is None:
            self._warps = None
        elif not isinstance(value, int):
            raise ValueError('The number of warps must be an integer')
        elif value <= 0:
            raise ValueError('The number of warps must be positive')
        elif value > 32:
            raise ValueError('The number of warps must be less than or equal to 32')
        else:
            self._warps = value