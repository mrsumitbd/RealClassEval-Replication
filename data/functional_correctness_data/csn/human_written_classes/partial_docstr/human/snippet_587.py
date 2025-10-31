from typing import Any, cast, Callable, Iterable, Iterator, List, NoReturn, Optional, Tuple, Type, TypeVar, Union

class DeprecatedOperation:
    """Inform deprecated operation"""

    def __init__(self, name: str, alternative: str) -> None:
        self.name = name
        self.alt = alternative

    def __call__(self, *_args, **_kwargs) -> NoReturn:
        raise ValueError(f'{self.name} operation is deprecated. Use insteads {self.alt}.')