
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
        """Creates a Media Part from a JSON part."""
        try:
            payload: Dict[str, Any] = json.loads(json_part)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        if "type" not in payload:
            raise ValueError("Missing 'type' field in JSON payload")
        if "data" not in payload:
            raise ValueError("Missing 'data' field in JSON payload")

        return cls(type=payload["type"], data=payload["data"])

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
