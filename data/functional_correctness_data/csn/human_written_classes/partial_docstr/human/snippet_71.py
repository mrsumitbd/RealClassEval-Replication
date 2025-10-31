import typing as t

class BaseAction:
    """Base class for representing actions to take by retry object.

    Concrete implementations must define:
    - __init__: to initialize all necessary fields
    - REPR_FIELDS: class variable specifying attributes to include in repr(self)
    - NAME: for identification in retry object methods and callbacks
    """
    REPR_FIELDS: t.Sequence[str] = ()
    NAME: t.Optional[str] = None

    def __repr__(self) -> str:
        state_str = ', '.join((f'{field}={getattr(self, field)!r}' for field in self.REPR_FIELDS))
        return f'{self.__class__.__name__}({state_str})'

    def __str__(self) -> str:
        return repr(self)