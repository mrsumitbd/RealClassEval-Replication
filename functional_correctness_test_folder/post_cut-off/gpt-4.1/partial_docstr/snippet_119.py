
import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class MediaPart:
    type: str
    data: dict

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        obj = json.loads(json_part)
        type_ = obj.get("type", "")
        data = obj.get("data", {})
        return cls(type=type_, data=data)

    def is_image(self) -> bool:
        '''Returns whether the part is an image.'''
        return self.type.lower() == "image"

    def is_audio(self) -> bool:
        return self.type.lower() == "audio"

    def is_reset_command(self) -> bool:
        return self.type.lower() == "reset_command"

    def is_config(self) -> bool:
        return self.type.lower() == "config"

    def is_mic_off(self) -> bool:
        return self.type.lower() == "mic_off"
