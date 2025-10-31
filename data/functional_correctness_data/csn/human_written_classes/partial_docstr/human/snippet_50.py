from typing import Optional, Tuple

class SessionState:
    """
    Stores the information needed to fetch updates and about the current user.

    * user_id: 64-bit number representing the user identifier.
    * dc_id: 32-bit number relating to the datacenter identifier where the user is.
    * bot: is the logged-in user a bot?
    * pts: 64-bit number holding the state needed to fetch updates.
    * qts: alternative 64-bit number holding the state needed to fetch updates.
    * date: 64-bit number holding the date needed to fetch updates.
    * seq: 64-bit-number holding the sequence number needed to fetch updates.
    * takeout_id: 64-bit-number holding the identifier of the current takeout session.

    Note that some of the numbers will only use 32 out of the 64 available bits.
    However, for future-proofing reasons, we recommend you pretend they are 64-bit long.
    """
    __slots__ = ('user_id', 'dc_id', 'bot', 'pts', 'qts', 'date', 'seq', 'takeout_id')

    def __init__(self, user_id: int, dc_id: int, bot: bool, pts: int, qts: int, date: int, seq: int, takeout_id: Optional[int]):
        self.user_id = user_id
        self.dc_id = dc_id
        self.bot = bot
        self.pts = pts
        self.qts = qts
        self.date = date
        self.seq = seq
        self.takeout_id = takeout_id

    def __repr__(self):
        return repr({k: getattr(self, k) for k in self.__slots__})