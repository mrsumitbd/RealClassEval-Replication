
import dataclasses
import json
from typing import Dict, Any


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    data: Dict[str, Any]

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Creates a Media Part from a JSON part."""
        return cls(json.loads(json_part))

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        return self.data.get('type') == 'image'

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        return self.data.get('type') == 'audio'

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        return self.data.get('type') == 'reset'

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        return self.data.get('type') == 'config'

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        return self.data.get('mic') == 'off'
