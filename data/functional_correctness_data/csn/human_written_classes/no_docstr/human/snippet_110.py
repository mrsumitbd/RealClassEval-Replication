class GitObject:
    rev: str
    name: str
    date: str

    def __eq__(self, other: object) -> bool:
        return hasattr(other, 'rev') and self.rev == other.rev

    def __hash__(self) -> int:
        return hash(self.rev)