
import dataclasses
import json


@dataclasses.dataclass(frozen=True)
class MediaPart:
    '''A part of media data.'''
    data: bytes
    content_type: str

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        '''Creates a Media Part from a JSON part.'''
        part_dict = json.loads(json_part)
        return cls(data=part_dict['data'].encode(), content_type=part_dict['content_type'])

    def is_image(self) -> bool:
        '''Returns whether the part is an image.'''
        return self.content_type.startswith('image/')

    def is_audio(self) -> bool:
        '''Returns whether the part is audio.'''
        return self.content_type.startswith('audio/')

    def is_reset_command(self) -> bool:
        '''Returns whether the part is a reset command.'''
        return self.content_type == 'application/reset'

    def is_config(self) -> bool:
        '''Returns whether the part is a config.'''
        return self.content_type == 'application/config'

    def is_mic_off(self) -> bool:
        '''Returns whether the part indicates the client has turned off the mic.'''
        return self.content_type == 'application/mic-off'
