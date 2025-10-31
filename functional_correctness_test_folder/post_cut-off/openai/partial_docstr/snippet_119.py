
import dataclasses
import json
from typing import Any, Dict, Optional


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """Represents a single part of a media message.

    The JSON representation is expected to contain at least a ``type`` field
    that indicates the kind of part.  Any additional data is stored in
    ``payload``.
    """
    type: str
    payload: Optional[Dict[str, Any]] = None

    @classmethod
    def from_json(cls, json_part: str) -> "MediaPart":
        """Create a :class:`MediaPart` instance from a JSON string.

        Parameters
        ----------
        json_part:
            A JSON string that must contain a ``type`` key.  Any other keys
            are stored in ``payload``.

        Returns
        -------
        MediaPart
            The parsed media part.
        """
        try:
            data = json.loads(json_part)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("JSON must represent an object")

        if "type" not in data:
            raise ValueError("JSON must contain a 'type' field")

        part_type = data.pop("type")
        return cls(type=part_type, payload=data or None)

    def is_image(self) -> bool:
        """Return ``True`` if the part represents an image."""
        return self.type.lower() == "image"

    def is_audio(self) -> bool:
        """Return ``True`` if the part represents an audio clip."""
        return self.type.lower() == "audio"

    def is_reset_command(self) -> bool:
        """Return ``True`` if the part is a reset command."""
        return self.type.lower() == "reset"

    def is_config(self) -> bool:
        """Return ``True`` if the part contains configuration data."""
        return self.type.lower() == "config"

    def is_mic_off(self) -> bool:
        """Return ``True`` if the part signals that the microphone was turned off."""
        return self.type.lower() == "mic_off"
