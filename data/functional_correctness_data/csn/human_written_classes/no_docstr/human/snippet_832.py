import shlex
from typing import Any, Callable, Iterable, Literal, Mapping, Optional, Sequence, Union

class UnixLex:

    @classmethod
    def quote_args(cls, args: Sequence[str]) -> Sequence[str]:
        return [cls.quote_string(a) for a in args]

    @classmethod
    def quote_string(cls, s: str) -> str:
        quoted = shlex.quote(s)
        if quoted.startswith("'") and '"' not in quoted:
            quoted = f'"{quoted[1:-1]}"'
        return quoted