
import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    type: str
    payload: Dict[str, Any]

    @classmethod
    def from_json(cls, json_part: str) -> "MediaPart":
        """Creates a MediaPart from a JSON part."""
        try:
            part = json.loads(json_part)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        if not isinstance(part, dict):
            raise ValueError("JSON part must be an object")

        # The type field is mandatory; fall back to empty string if missing
        part_type = part.get("type", "")
        if not isinstance(part_type, str):
            raise ValueError("The 'type' field must be a string")

        return cls(type=part_type, payload=part)

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        return self.type.lower() == "image"

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        return self.type.lower() == "audio"

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        return self.type.lower() in {"reset", "reset_command"}

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        return self.type.lower() == "config"

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        return self.type.lower() == "mic_off"
