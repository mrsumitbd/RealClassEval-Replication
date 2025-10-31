
import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """Represents a part of media data.

    The JSON representation is expected to contain at least a ``type`` field
    that indicates the kind of part.  Optional additional data can be stored
    in the ``payload`` dictionary.
    """
    type: str
    payload: Dict[str, Any] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Create a :class:`MediaPart` instance from a JSON string.

        Parameters
        ----------
        json_part:
            A JSON string that must contain a ``type`` key.  Any other keys
            are stored in the ``payload`` dictionary.

        Returns
        -------
        MediaPart
            The parsed media part.

        Raises
        ------
        ValueError
            If the JSON cannot be parsed or the ``type`` key is missing.
        """
        try:
            data = json.loads(json_part)
        except Exception as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("JSON must represent an object")

        if 'type' not in data:
            raise ValueError("Missing required 'type' field in JSON")

        part_type = data.pop('type')
        return cls(type=part_type, payload=data)

    def is_image(self) -> bool:
        """Return ``True`` if this part represents an image."""
        return self.type.lower() == 'image'

    def is_audio(self) -> bool:
        """Return ``True`` if this part represents an audio clip."""
        return self.type.lower() == 'audio'

    def is_reset_command(self) -> bool:
        """Return ``True`` if this part is a reset command."""
        return self.type.lower() == 'reset'

    def is_config(self) -> bool:
        """Return ``True`` if this part contains configuration data."""
        return self.type.lower() == 'config'

    def is_mic_off(self) -> bool:
        """Return ``True`` if this part signals that the microphone should be turned off."""
        return self.type.lower() == 'mic_off'
