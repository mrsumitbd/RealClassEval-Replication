import typing as t
from dataclasses import dataclass

@dataclass
class Arg:
    value: str
    orig: str
    arg_type: t.Literal['long-opt', 'short-opt', 'pos']

    def is_pos(self):
        return self.arg_type == 'pos'

    def is_long_opt(self):
        return self.arg_type == 'long-opt'

    def is_short_opt(self):
        return self.arg_type == 'short-opt'

    def is_opt(self):
        return self.is_long_opt() or self.is_short_opt()