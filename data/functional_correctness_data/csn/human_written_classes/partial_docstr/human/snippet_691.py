from typing import TYPE_CHECKING, Any, Dict, Final, Literal, Optional, Sequence, Type, TypedDict, TypeVar, Union, cast

class Plugin:
    """
    Represents a Lavalink server plugin.

    Parameters
    ----------
    data: Dict[str, Any]
        The data to initialise a Plugin from.

    Attributes
    ----------
    name: :class:`str`
        The name of the plugin.
    version: :class:`str`
        The version of the plugin.
    """
    __slots__ = ('name', 'version')

    def __init__(self, data: Dict[str, Any]):
        self.name: Final[str] = data['name']
        self.version: Final[str] = data['version']

    def __str__(self):
        return f'{self.name} v{self.version}'

    def __repr__(self):
        return f'<Plugin name={self.name} version={self.version}>'