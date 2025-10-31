
import dataclasses
import json
from typing import Dict, Any


@dataclasses.dataclass(frozen=True)
class MediaPart:
    type: str
    data: Dict[str, Any] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        part_dict = json.loads(json_part)
        return cls(**part_dict)

    def is_image(self) -> bool:
        '''Returns whether the part is an image.'''
        return self.type == 'image'

    def is_audio(self) -> bool:
        return self.type == 'audio'

    def is_reset_command(self) -> bool:
        return self.type == 'reset'

    def is_config(self) -> bool:
        return self.type == 'config'

    def is_mic_off(self) -> bool:
        return self.type == 'mic_off'
