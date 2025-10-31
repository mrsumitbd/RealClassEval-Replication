from argh.exceptions import CommandError, DispatchingError
import argparse
from typing import IO, Any, Callable, Dict, Iterator, List, Optional, Tuple
from argh.assembling import NameMappingPolicy, add_commands, set_default_command

class EntryPoint:
    """
    An object to which functions can be attached and then dispatched.

    When called with an argument, the argument (a function) is registered
    at this entry point as a command.

    When called without an argument, dispatching is triggered with all
    previously registered commands.

    Usage::

        from argh import EntryPoint

        app = EntryPoint("main", {"description": "This is a cool app"})

        @app
        def ls() -> Iterator[int]:
            for i in range(10):
                yield i

        @app
        def greet() -> str:
            return "hello"

        if __name__ == "__main__":
            app()

    """

    def __init__(self, name: Optional[str]=None, parser_kwargs: Optional[Dict[str, Any]]=None) -> None:
        self.name = name or 'unnamed'
        self.commands: List[Callable] = []
        self.parser_kwargs = parser_kwargs or {}

    def __call__(self, function: Optional[Callable]=None):
        if function:
            self._register_command(function)
            return function
        return self._dispatch()

    def _register_command(self, function: Callable) -> None:
        self.commands.append(function)

    def _dispatch(self) -> None:
        if not self.commands:
            raise DispatchingError(f'no commands for entry point "{self.name}"')
        parser = argparse.ArgumentParser(**self.parser_kwargs)
        add_commands(parser, self.commands)
        dispatch(parser)