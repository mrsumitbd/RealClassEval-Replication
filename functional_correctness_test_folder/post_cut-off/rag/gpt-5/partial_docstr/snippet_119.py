import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    kind: str
    raw: Dict[str, Any]

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Creates a Media Part from a JSON part."""
        if not isinstance(json_part, str):
            raise TypeError('json_part must be a string')

        try:
            obj = json.loads(json_part)
        except json.JSONDecodeError as exc:
            raise ValueError('invalid JSON for media part') from exc

        if not isinstance(obj, dict):
            raise ValueError('media part JSON must be an object')

        def normalize(value: str) -> str:
            v = value.strip().lower().replace('-', '_')
            if v in ('reset_command',):
                return 'reset'
            if v in ('microphone_off', 'micoff'):
                return 'mic_off'
            return v

        kind = None

        t = obj.get('type')
        if isinstance(t, str) and t.strip():
            kind = normalize(t)

        if kind is None:
            # Infer from known keys
            key_to_kind = {
                'image': 'image',
                'image_url': 'image',
                'image_base64': 'image',
                'audio': 'audio',
                'audio_url': 'audio',
                'audio_base64': 'audio',
                'reset': 'reset',
                'reset_command': 'reset',
                'config': 'config',
                'mic_off': 'mic_off',
                'microphone_off': 'mic_off',
                'mic-off': 'mic_off',
                'micOff': 'mic_off',
            }
            for k, mapped in key_to_kind.items():
                if k in obj:
                    kind = mapped
                    break

        if kind is None:
            # Infer from MIME / content type
            mime = None
            if isinstance(obj.get('mime'), str):
                mime = obj['mime']
            elif isinstance(obj.get('content_type'), str):
                mime = obj['content_type']
            elif isinstance(obj.get('headers'), dict):
                ct = obj['headers'].get(
                    'content-type') or obj['headers'].get('Content-Type')
                if isinstance(ct, str):
                    mime = ct
            if isinstance(mime, str):
                m = mime.lower()
                if m.startswith('image/'):
                    kind = 'image'
                elif m.startswith('audio/'):
                    kind = 'audio'

        if kind is None:
            kind = 'unknown'

        return cls(kind=kind, raw=obj)

    def _mime_startswith(self, prefix: str) -> bool:
        mime = None
        if isinstance(self.raw.get('mime'), str):
            mime = self.raw['mime']
        elif isinstance(self.raw.get('content_type'), str):
            mime = self.raw['content_type']
        elif isinstance(self.raw.get('headers'), dict):
            ct = self.raw['headers'].get(
                'content-type') or self.raw['headers'].get('Content-Type')
            if isinstance(ct, str):
                mime = ct
        return isinstance(mime, str) and mime.lower().startswith(prefix)

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        return self.kind == 'image' or self._mime_startswith('image/')

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        return self.kind == 'audio' or self._mime_startswith('audio/')

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        return self.kind == 'reset'

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        return self.kind == 'config'

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        return self.kind == 'mic_off'
