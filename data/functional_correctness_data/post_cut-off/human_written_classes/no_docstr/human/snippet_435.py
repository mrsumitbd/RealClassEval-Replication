import click
from typing import Any, Callable, TypeVar, Union, overload

class CLIGroup(click.Group):

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command:
        ...

    @overload
    def command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], click.Command]:
        ...

    def command(self, *args: Any, **kwargs: Any) -> Union[click.Command, Callable[[Callable[..., Any]], click.Command]]:
        original_decorator = super().command(*args, **kwargs)

        def decorator(f: Callable[..., Any]) -> click.Command:
            result = original_decorator(f)
            assert isinstance(result, click.Command)
            return result
        if args and callable(args[0]):
            return decorator(args[0])
        else:
            return decorator