from typing import Any, BinaryIO, Callable, ContextManager, Dict, Generator, Iterable, Iterator, List, Optional, TextIO, Tuple, Type, TypeVar, Union, cast

class HiddenText:

    def __init__(self, secret: str, redacted: str) -> None:
        self.secret = secret
        self.redacted = redacted

    def __repr__(self) -> str:
        return f'<HiddenText {str(self)!r}>'

    def __str__(self) -> str:
        return self.redacted

    def __eq__(self, other: Any) -> bool:
        if type(self) != type(other):
            return False
        return self.secret == other.secret