from typing import AsyncIterator, Dict, Optional, cast

class RunContext:

    def __init__(self, last_known_event_offset: int) -> None:
        self.data: Dict[str, Dict[str, bool]] = {}
        self.last_known_event_offset = last_known_event_offset

    def set_typing_emitted(self, event_id: str, emitted: bool) -> None:
        """Set the typing_emitted status for a given event_id."""
        if event_id not in self.data:
            self.data[event_id] = {}
        self.data[event_id]['typing_emitted'] = emitted

    def get_typing_emitted(self, event_id: str) -> bool:
        """Retrieve the typing_emitted status for a given event_id."""
        return self.data.get(event_id, {}).get('typing_emitted', False)

    def get_last_known_event_offset(self) -> int:
        """Get the last known event offset."""
        return self.last_known_event_offset

    def clear(self) -> None:
        """Clear the entire run context."""
        self.data.clear()
        self.last_known_event_offset = 0