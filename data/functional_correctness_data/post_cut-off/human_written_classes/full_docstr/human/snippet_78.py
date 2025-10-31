from typing import Any, Callable, Type, TypeVar

class LoggedToolMixin:
    """A mixin class that adds logging functionality to any tool."""

    def _log_operation(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        """Helper method to log tool operations."""
        tool_name = self.__class__.__name__.replace('Logged', '')
        params = ', '.join([*(str(arg) for arg in args), *(f'{k}={v}' for k, v in kwargs.items())])
        logger.debug(f'Tool {tool_name}.{method_name} called with parameters: {params}')

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Override _run method to add logging."""
        self._log_operation('_run', *args, **kwargs)
        result = super()._run(*args, **kwargs)
        logger.debug(f"Tool {self.__class__.__name__.replace('Logged', '')} returned: {result}")
        return result