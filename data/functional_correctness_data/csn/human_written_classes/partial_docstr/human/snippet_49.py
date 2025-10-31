class ChannelState:
    """
    Stores the information needed to fetch updates from a channel.

    * channel_id: 64-bit number representing the channel identifier.
    * pts: 64-bit number holding the state needed to fetch updates.
    """
    __slots__ = ('channel_id', 'pts')

    def __init__(self, channel_id: int, pts: int):
        self.channel_id = channel_id
        self.pts = pts

    def __repr__(self):
        return repr({k: getattr(self, k) for k in self.__slots__})