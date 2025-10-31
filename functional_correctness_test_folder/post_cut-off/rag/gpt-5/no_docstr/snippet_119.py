import dataclasses
import json
from typing import Any, Dict, Optional


@dataclasses.dataclass(frozen=True)
class MediaPart:
    """A part of media data."""
    raw: Dict[str, Any]

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        """Creates a Media Part from a JSON part."""
        try:
            data = json.loads(json_part)
        except Exception as e:
            raise ValueError(f'Invalid JSON for MediaPart: {e}') from e
        if not isinstance(data, dict):
            raise ValueError('MediaPart JSON must decode to an object')
        return cls(raw=data)

    def _get_lower_str(self, *keys: str) -> str:
        for k in keys:
            v = self.raw.get(k)
            if isinstance(v, str):
                return v.lower()
        return ''

    def _get_bool(self, *keys: str) -> Optional[bool]:
        for k in keys:
            v = self.raw.get(k)
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                vl = v.strip().lower()
                if vl in ('true', 'false'):
                    return vl == 'true'
        return None

    def _get_uri_or_name(self) -> str:
        for k in ('uri', 'url', 'href', 'source', 'src', 'name', 'filename', 'file'):
            v = self.raw.get(k)
            if isinstance(v, str):
                return v.lower()
        data = self.raw.get('data')
        if isinstance(data, dict):
            for k in ('uri', 'url', 'href', 'source', 'src', 'name', 'filename', 'file'):
                v = data.get(k)
                if isinstance(v, str):
                    return v.lower()
        return ''

    def _type_mime(self) -> tuple[str, str]:
        t = self._get_lower_str('type', 'kind', 'category')
        m = self._get_lower_str(
            'mime', 'mimetype', 'content_type', 'content-type', 'media_type', 'mediatype')
        if not m:
            ct = self.raw.get('headers') or self.raw.get(
                'meta') or self.raw.get('metadata')
            if isinstance(ct, dict):
                m = str(ct.get('content-type', '')).lower()
        return t, m

    def is_image(self) -> bool:
        """Returns whether the part is an image."""
        t, m = self._type_mime()
        if t in {'image', 'img', 'picture', 'photo', 'image-part'}:
            return True
        if m.startswith('image/'):
            return True
        uri = self._get_uri_or_name()
        if uri.startswith('data:image/'):
            return True
        for ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff', '.tif', '.heic', '.avif'):
            if uri.endswith(ext):
                return True
        return False

    def is_audio(self) -> bool:
        """Returns whether the part is audio."""
        t, m = self._type_mime()
        if t in {'audio', 'sound', 'voice', 'audio-part'}:
            return True
        if m.startswith('audio/'):
            return True
        uri = self._get_uri_or_name()
        if uri.startswith('data:audio/'):
            return True
        for ext in ('.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.oga', '.opus', '.amr', '.wma'):
            if uri.endswith(ext):
                return True
        return False

    def is_reset_command(self) -> bool:
        """Returns whether the part is a reset command."""
        t, m = self._type_mime()
        if t in {'reset', 'reset_command', 'reset-command', 'clear', 'clear_context', 'clear-context'}:
            return True
        cmd = self._get_lower_str('command', 'action', 'op')
        if cmd in {'reset', 'clear', 'clear_context', 'clear-context'}:
            return True
        if self._get_bool('reset') is True:
            return True
        event = self._get_lower_str('event')
        if event in {'reset', 'clear'}:
            return True
        return False

    def is_config(self) -> bool:
        """Returns whether the part is a config."""
        t, _ = self._type_mime()
        if t in {'config', 'configuration', 'settings', 'setup'}:
            return True
        if any(k in self.raw for k in ('config', 'configuration', 'settings')):
            return True
        return False

    def is_mic_off(self) -> bool:
        """Returns whether the part indicates the client has turned off the mic."""
        t, _ = self._type_mime()
        if t in {'mic_off', 'mic-off', 'microphone_off', 'microphone-off', 'mute', 'muted'}:
            return True
        status = self._get_lower_str(
            'status', 'mic_status', 'microphone_status')
        if status in {'off', 'mute', 'muted', 'disabled'}:
            return True
        mic = self.raw.get('mic') or self.raw.get('microphone')
        if isinstance(mic, str) and mic.lower() in {'off', 'mute', 'muted', 'disabled'}:
            return True
        mic_bool = self._get_bool('mic', 'microphone', 'muted')
        if mic_bool is False or (mic_bool is True and 'muted' in self.raw):
            # mic False => off; explicit muted True => off
            return mic_bool is False or bool(self.raw.get('muted'))
        event = self._get_lower_str('event')
        if event in {'mic_off', 'mic-off', 'mute', 'muted'}:
            return True
        return False
