import time
from collections import OrderedDict

class BoundedSessionTracker:
    """Memory-safe session tracker with automatic expiration."""

    def __init__(self, max_sessions: int=1000, session_ttl: int=3600) -> None:
        self.max_sessions = max_sessions
        self.session_ttl = session_ttl
        self.sessions: OrderedDict[str, float] = OrderedDict()
        self.last_cleanup = time.time()

    def track_session(self, session_id: str) -> bool:
        """Track a session, returns True if it's new."""
        current_time = time.time()
        if current_time - self.last_cleanup > 300:
            self._cleanup_expired(current_time)
            self.last_cleanup = current_time
        if session_id in self.sessions:
            self.sessions.move_to_end(session_id)
            return False
        self.sessions[session_id] = current_time
        while len(self.sessions) > self.max_sessions:
            self.sessions.popitem(last=False)
        return True

    def _cleanup_expired(self, current_time: float) -> None:
        """Remove expired sessions."""
        expired = [sid for sid, timestamp in self.sessions.items() if current_time - timestamp > self.session_ttl]
        for sid in expired:
            del self.sessions[sid]

    def get_active_session_count(self) -> int:
        return len(self.sessions)