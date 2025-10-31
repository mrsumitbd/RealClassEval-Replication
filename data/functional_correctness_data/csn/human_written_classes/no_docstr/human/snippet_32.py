class PtsInfo:
    __slots__ = ('pts', 'pts_count', 'entry')

    def __init__(self, pts: int, pts_count: int, entry: object):
        self.pts = pts
        self.pts_count = pts_count
        self.entry = entry

    @classmethod
    def from_update(cls, update):
        pts = getattr(update, 'pts', None)
        if pts:
            pts_count = getattr(update, 'pts_count', None) or 0
            try:
                entry = update.message.peer_id.channel_id
            except AttributeError:
                entry = getattr(update, 'channel_id', None) or ENTRY_ACCOUNT
            return cls(pts=pts, pts_count=pts_count, entry=entry)
        qts = getattr(update, 'qts', None)
        if qts:
            return cls(pts=qts, pts_count=1, entry=ENTRY_SECRET)
        return None

    def __repr__(self):
        return f'PtsInfo(pts={self.pts}, pts_count={self.pts_count}, entry={self.entry})'