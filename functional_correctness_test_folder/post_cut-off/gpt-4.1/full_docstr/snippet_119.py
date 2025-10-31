
import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class MediaPart:
    '''A part of media data.'''
    type: str
    data: Any = None

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        '''Creates a Media Part from a JSON part.'''
        obj = json.loads(json_part)
        type_ = obj.get("type", "")
        data = obj.get("data", None)
        return cls(type=type_, data=data)

    def is_image(self) -> bool:
        '''Returns whether the part is an image.'''
        return self.type.lower() == "image"

    def is_audio(self) -> bool:
        '''Returns whether the part is audio.'''
        return self.type.lower() == "audio"

    def is_reset_command(self) -> bool:
        '''Returns whether the part is a reset command.'''
        return self.type.lower() == "reset_command"

    def is_config(self) -> bool:
        '''Returns whether the part is a config.'''
        return self.type.lower() == "config"

    def is_mic_off(self) -> bool:
        '''Returns whether the part indicates the client has turned off the mic.'''
        return self.type.lower() == "mic_off"
