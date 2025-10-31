from typing import Any, Callable, Dict, Optional, overload, Tuple, Type, TYPE_CHECKING

class BaseDefault:
    default = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if isinstance(self, StrDefault) and args:
            args = (args[0].__str__(),)
        self.args = args

    def __str__(self) -> str:
        return StrDefault(super().__str__())

    def deconstruct(self) -> Tuple[str, Tuple[Any, ...], Dict[str, Any]]:
        if self == self.default:
            return ('salesforce.fields.DefaultedOnCreate', (), {})
        else:
            return ('salesforce.fields.DefaultedOnCreate', self.args, {})