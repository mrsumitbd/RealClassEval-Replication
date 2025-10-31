from uuid import UUID
from binascii import hexlify

class AssetRef:

    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return '<%s (asset_path=%r, guid=%r, type=%r, file_path=%r)>' % (self.__class__.__name__, self.asset_path, self.guid, self.type, self.file_path)

    def load(self, buf):
        self.asset_path = buf.read_string()
        self.guid = UUID(hexlify(buf.read(16)).decode('utf-8'))
        self.type = buf.read_int()
        self.file_path = buf.read_string()
        self.asset = None

    def resolve(self):
        return self.source.get_asset(self.file_path)