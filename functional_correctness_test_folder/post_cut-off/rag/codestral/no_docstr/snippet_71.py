
@dataclass
class HookEvent:
    '''Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    '''
    agent: Any

    @property
    def should_reverse_callbacks(self) -> bool:
        '''Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        '''
        return False

    def _can_write(self, name: str) -> bool:
        '''Check if the given property can be written to.
        Args:
            name: The name of the property to check.
        Returns:
            True if the property can be written to, False otherwise.
        '''
        return name in self.__annotations__

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        for name in self.__dict__:
            if not self._can_write(name):
                raise AttributeError(
                    f"Cannot set attribute '{name}' on {self.__class__.__name__}")

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        if not hasattr(self, name) or not self._can_write(name):
            raise AttributeError(
                f"Cannot set attribute '{name}' on {self.__class__.__name__}")
        super().__setattr__(name, value)
