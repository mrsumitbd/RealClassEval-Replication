
import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class MediaPart:
    type: str
    data: str

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        data = json.loads(json_part)
        return cls(**data)

    def is_image(self) -> bool:
        return self.type == 'image'

    def is_audio(self) -> bool:
        return self.type == 'audio'

    def is_reset_command(self) -> bool:
        return self.type == 'reset_command'

    def is_config(self) -> bool:
        return self.type == 'config'

    def is_mic_off(self) -> bool:
        return self.type == 'mic_off'
