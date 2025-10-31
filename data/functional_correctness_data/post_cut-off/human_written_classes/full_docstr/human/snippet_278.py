from typing import Any, ClassVar, Dict, Type, List
from fletx.utils.exceptions import CommandError, CommandExecutionError, CommandNotFoundError

class CommandRegistry:
    """
    Registry for all commands in the FletX CLI.
    This class is responsible for storing and managing all available commands.
    It provides methods to register new commands and retrieve existing ones.
    """
    _commands: ClassVar[Dict[str, Type['BaseCommand']]] = {}

    @classmethod
    def register(cls, name: str, command_cls: Type['BaseCommand']) -> None:
        """Register a new command class."""
        cls._commands[name] = command_cls

    @classmethod
    def get(cls, name: str) -> Type['BaseCommand']:
        """Get a command class by its name."""
        if name not in cls._commands:
            raise CommandNotFoundError(f"Command '{name}' not found.")
        return cls._commands[name]

    @classmethod
    def all(cls) -> List[Type['BaseCommand']]:
        """Get all registered command classes."""
        return list(cls._commands.values())