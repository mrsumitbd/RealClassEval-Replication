from lark.tree import Meta
from typing import Callable, Any

class SystemOfExpr:

    def __init__(self, expressions: list[tuple[Any, Meta]]):
        self.__expressions: list[Any] = [e[0] for e in expressions]
        self.__location_data: list[Meta] = [e[1] for e in expressions]

    def __len__(self):
        return len(self.__expressions)

    def extend(self, expressions: list[tuple[Any, Meta]]):
        return SystemOfExpr([*[(e, m) for e, m in zip(self.__expressions, self.__location_data)], *expressions])

    def change_expr(self, expression_index: int, change_func: Callable[[Any], Any]):
        self.__expressions[expression_index] = change_func(self.__expressions[expression_index])

    def get_expr(self, expression_index: int):
        return self.__expressions[expression_index]

    def get_all_expr(self):
        return tuple(self.__expressions)

    def get_location(self, expression_index: int) -> Meta:
        return self.__location_data[expression_index]

    def get_all_locations(self):
        return tuple(self.__location_data)