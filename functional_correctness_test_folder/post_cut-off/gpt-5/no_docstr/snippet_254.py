from datetime import datetime, timezone
from typing import Optional
import os


class TimeTracker:

    def __init__(self, history_dir: str):
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def _get_character_history_file(self, character_id: str) -> str:
        safe_id = "".join(
            c for c in character_id if c.isalnum() or c in ("-", "_"))
        if not safe_id:
            safe_id = "default"
        return os.path.join(self.history_dir, f"{safe_id}.history")

    def get_last_message_time(self, character_id: str) -> Optional[datetime]:
        path = self._get_character_history_file(character_id)
        if not os.path.exists(path):
            return None
        try:
            ts = os.path.getmtime(path)
        except OSError:
            return None
        return datetime.fromtimestamp(ts, tz=timezone.utc)

    def format_time_elapsed(self, last_time: Optional[datetime], current_time: datetime) -> str:
        if last_time is None:
            return ""
        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
        delta = current_time - last_time
        total_seconds = int(delta.total_seconds())
        if total_seconds <= 0:
            return ""
        if total_seconds < 60:
            return "moments later "
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        parts = []
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes and len(parts) < 2:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        phrase = ", ".join(parts) if parts else "moments"
        return f"{phrase} later "

    def get_time_elapsed_prefix(self, character_id: str) -> str:
        last_time = self.get_last_message_time(character_id)
        now = datetime.now(timezone.utc)
        return self.format_time_elapsed(last_time, now)
