from typing import TYPE_CHECKING, Any, Dict, Final, Literal, Optional, Sequence, Type, TypedDict, TypeVar, Union, cast

class PlaylistInfo:
    """
    Attributes
    ----------
    name: :class:`str`
        The name of the playlist.
    selected_track: :class:`int`
        The index of the selected/highlighted track.
        This will be -1 if there is no selected track.
    """
    __slots__ = ('name', 'selected_track')

    def __init__(self, name: str, selected_track: int=-1):
        self.name: Final[str] = name
        self.selected_track: Final[int] = selected_track

    @classmethod
    def from_dict(cls, mapping: Dict[str, Any]):
        return cls(mapping['name'], mapping.get('selectedTrack', -1))

    @classmethod
    def none(cls):
        return cls('', -1)

    def __repr__(self):
        return f'<PlaylistInfo name={self.name} selected_track={self.selected_track}>'