from yangson.instance import ArrayEntry
from yangson.typealiases import RawObject

class ModuleData:
    name: str
    revision: str
    location: set[str]

    def __init__(self: 'ModuleData', rfc8525_entry: ArrayEntry):
        """Initialize the receiver."""
        val = rfc8525_entry.value
        self.name = val['name']
        self.revision = val.get('revision', '')
        self.location = set([loc.strip() for loc in val.get('location', [])])

    def key(self) -> tuple[str, str]:
        """Return the receiver's key (module name & revision)."""
        return (self.name, self.revision)

    def merge(self, other: 'ModuleData') -> None:
        """Merge the receiver with another instance."""
        self.location |= other.location

    def as_raw(self) -> RawObject:
        """Return the receiver represented as an RFC 7895 entry."""
        res = {'name': self.name, 'revision': self.revision}
        if self.location:
            res['schema'] = list(self.location)[0]
        return res