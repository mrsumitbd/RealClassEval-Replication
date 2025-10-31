
import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""

    type: str
    data: Any

    @classmethod
    def from_json(cls, json_part: str) -> "MediaPart":
        """Creates a MediaPart from a JSON part."""
        try:
            parsed: Dict[str, Any] = json.loads(json_part)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        # The JSON is expected to contain a 'type' key and optionally a 'data' key.
        part_type = parsed.get("type")
        if part_type is None:
            raise ValueError("JSON part must contain a 'type' field")

        part_data = parsed.get("data")
        return cls(type=part_type, data=part_data)

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        return self.type.lower() == "image"

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        return self.type.lower() == "audio"

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        return self.type.lower() == "reset"

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        return self.type.lower() == "config"

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        return self.type.lower() == "mic_off"
