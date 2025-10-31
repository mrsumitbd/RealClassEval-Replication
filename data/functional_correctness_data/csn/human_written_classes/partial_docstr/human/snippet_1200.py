from typing import Iterable, FrozenSet, TypeVar, NamedTuple

class PluginRequirements:
    """Requirements of a :py:class:`~.SectionPlugin`"""
    __slots__ = ('required', 'before', 'after')

    def __init__(self, required: bool=False, before: FrozenSet[str]=frozenset(), after: FrozenSet[str]=frozenset()):
        self.required = required
        self.before = before
        self.after = after

    def __repr__(self):
        return f'{self.__class__.__name__}(required={self.required}, before={self.before}, after={self.after})'