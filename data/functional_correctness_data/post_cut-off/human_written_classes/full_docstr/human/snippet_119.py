import dataclasses
import json

@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    base64data: str
    mime_type: str

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Creates a Media Part from a JSON part."""
        json_dict = json.loads(json_part)
        return MediaPart(base64data=json_dict['data'], mime_type=json_dict['mime_type'])

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        return self.mime_type.startswith('image/')

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        return self.mime_type.startswith('audio/')

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        return self.mime_type == _COMMAND_MIMETYPE and self.base64data == 'RESET'

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        return self.mime_type == _CONFIG_MIMETYPE

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        return self.mime_type == _STATE_MIMETYPE and self.base64data == 'MIC_OFF'