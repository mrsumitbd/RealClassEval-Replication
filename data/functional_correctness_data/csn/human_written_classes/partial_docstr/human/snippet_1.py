from typing import Any, Optional
import uuid

class InputDevice:
    """Describes the input device being used for the action."""

    def __init__(self, name: Optional[str]=None):
        self.name = name or uuid.uuid4()
        self.actions: list[Any] = []

    def add_action(self, action: Any) -> None:
        """"""
        self.actions.append(action)

    def clear_actions(self) -> None:
        self.actions = []

    def create_pause(self, duration: float=0) -> None:
        pass