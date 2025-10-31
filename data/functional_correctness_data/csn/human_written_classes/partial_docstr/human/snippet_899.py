from typing import Any, Iterable, Optional

class Link:
    """
    DMRS-style dependency link.

    Links are a way of representing arguments without variables. A
    Link encodes a start and end node, the role name, and the scopal
    relationship between the start and end (e.g. label equality, qeq,
    etc).

    Args:
        start: node id of the start of the Link
        end: node id of the end of the Link
        role: role of the argument
        post: "post-slash label" indicating the scopal
            relationship between the start and end of the Link;
            possible values are `NEQ`, `EQ`, `HEQ`, and `H`
    Attributes:
        start: node id of the start of the Link
        end: node id of the end of the Link
        role: role of the argument
        post: "post-slash label" indicating the scopal
            relationship between the start and end of the Link
    """
    __slots__ = ('start', 'end', 'role', 'post')

    def __init__(self, start: int, end: int, role: str, post: str) -> None:
        self.start = int(start)
        self.end = int(end)
        self.role = role
        self.post = post

    def __repr__(self) -> str:
        return '<Link object ({} :{}/{} {}) at {}>'.format(self.start, self.role or '', self.post, self.end, id(self))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Link):
            return NotImplemented
        return self.start == other.start and self.end == other.end and (self.role == other.role) and (self.post == other.post)