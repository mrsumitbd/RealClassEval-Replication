import dataclasses
import json
from typing import Any, Mapping


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    raw: dict

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Creates a Media Part from a JSON part."""
        if isinstance(json_part, str):
            try:
                obj = json.loads(json_part)
            except Exception as exc:
                raise ValueError('invalid JSON for MediaPart') from exc
        elif isinstance(json_part, Mapping):
            obj = dict(json_part)
        else:
            raise TypeError('json_part must be a JSON string or a mapping')
        if not isinstance(obj, dict):
            raise ValueError('MediaPart JSON must decode to an object')
        return cls(raw=obj)

    def _type_str(self) -> str:
        t = self.raw.get('type') or self.raw.get(
            'kind') or self.raw.get('event') or self.raw.get('action')
        return str(t).lower() if isinstance(t, str) else ''

    def _mime_str(self) -> str:
        m = self.raw.get('mime') or self.raw.get(
            'content_type') or self.raw.get('mimetype')
        return str(m).lower() if isinstance(m, str) else ''

    def _str_field(self, *keys: str) -> str:
        for k in keys:
            v = self.raw.get(k)
            if isinstance(v, str):
                return v
        return ''

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        t = self._type_str()
        if t in {'image', 'image_part', 'photo', 'frame', 'thumbnail'}:
            return True
        mime = self._mime_str()
        if mime.startswith('image/'):
            return True
        data_uri = self._str_field('data_uri', 'data')
        if data_uri.startswith('data:image/'):
            return True
        url = self._str_field('url', 'path', 'src', 'href')
        image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.webp',
                      '.tif', '.tiff', '.bmp', '.svg', '.heic', '.avif')
        if any(url.lower().endswith(ext) for ext in image_exts if url):
            return True
        return False

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        t = self._type_str()
        if t in {'audio', 'sound', 'voice', 'audio_part'}:
            return True
        mime = self._mime_str()
        if mime.startswith('audio/'):
            return True
        data_uri = self._str_field('data_uri', 'data')
        if data_uri.startswith('data:audio/'):
            return True
        url = self._str_field('url', 'path', 'src', 'href')
        audio_exts = ('.wav', '.mp3', '.ogg', '.flac',
                      '.aac', '.m4a', '.opus', '.oga')
        if any(url.lower().endswith(ext) for ext in audio_exts if url):
            return True
        return False

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        t = self._type_str()
        if t in {'reset', 'clear', 'flush', 'restart', 'reset_command'}:
            return True
        cmd = self.raw.get('command') or self.raw.get(
            'op') or self.raw.get('action')
        if isinstance(cmd, str) and cmd.lower() in {'reset', 'clear', 'flush', 'restart'}:
            return True
        return False

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        t = self._type_str()
        if t in {'config', 'configuration', 'settings'}:
            return True
        if any(k in self.raw for k in ('config', 'configuration', 'settings', 'options', 'params')):
            return True
        return False

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        t = self._type_str()
        if t in {'mic_off', 'microphone_off', 'audio_stop', 'stop_microphone'}:
            return True
        mic = self.raw.get('mic')
        if mic in ('off', False, 0):
            return True
        microphone = self.raw.get('microphone')
        if microphone in ('off', 'disabled', False, 0):
            return True
        if (self.raw.get('enabled') is False) and any(k in self.raw for k in ('mic', 'microphone')):
            return True
        if self.raw.get('state') == 'off' and t in {'mic', 'microphone'}:
            return True
        return False
