import dataclasses
import json
from typing import Any, Dict, Optional


@dataclasses.dataclass(frozen=True)
class MediaPart:
    kind: str
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        def classify(d: Dict[str, Any]) -> str:
            t_candidates = []
            for key in ('type', 'kind', 'event', 'action', 'mediaType', 'role'):
                v = d.get(key)
                if isinstance(v, str):
                    t_candidates.append(v.lower())

            # Heuristics for mic state
            if isinstance(d.get('mic'), bool) and d.get('mic') is False:
                return 'mic_off'
            if 'mute' in d or 'muted' in d:
                val = d.get('mute', d.get('muted'))
                if isinstance(val, bool) and val is True:
                    return 'mic_off'

            # Heuristics for MIME/content type
            mime = None
            for k in ('mime', 'mimeType', 'contentType'):
                v = d.get(k)
                if isinstance(v, str):
                    mime = v.lower()
                    break

            # Image detection
            if mime and mime.startswith('image/'):
                return 'image'
            if any('image' in c for c in t_candidates):
                return 'image'
            # URL or data hints
            for k in ('image', 'image_url', 'url', 'src', 'data'):
                v = d.get(k)
                if isinstance(v, str):
                    lv = v.lower()
                    if lv.startswith('data:image/') or lv.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')):
                        return 'image'
                if isinstance(v, dict):
                    ct = v.get('contentType') or v.get(
                        'mime') or v.get('mimeType')
                    if isinstance(ct, str) and ct.lower().startswith('image/'):
                        return 'image'

            # Audio detection
            if mime and mime.startswith('audio/'):
                return 'audio'
            if any('audio' in c for c in t_candidates):
                return 'audio'
            for k in ('audio', 'audio_url', 'url', 'src', 'data'):
                v = d.get(k)
                if isinstance(v, str):
                    lv = v.lower()
                    if lv.startswith('data:audio/') or lv.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac', '.opus')):
                        return 'audio'
                if isinstance(v, dict):
                    ct = v.get('contentType') or v.get(
                        'mime') or v.get('mimeType')
                    if isinstance(ct, str) and ct.lower().startswith('audio/'):
                        return 'audio'

            # Reset
            reset_markers = {'reset', 'reset_command', 'restart', 'clear'}
            if any(c in reset_markers for c in t_candidates):
                return 'reset'

            # Config
            config_markers = {'config', 'configuration',
                              'settings', 'setup', 'options'}
            if any(c in config_markers for c in t_candidates) or 'config' in d:
                return 'config'

            # Mic off
            mic_off_markers = {'mic_off', 'microphone_off', 'mute', 'muted'}
            if any(c in mic_off_markers for c in t_candidates):
                return 'mic_off'

            return 'other'

        s = json_part.strip()
        # Handle simple symbolic strings
        simple = s.lower().strip('"').strip("'")
        if simple in ('reset', 'reset_command'):
            return cls(kind='reset', data=None)
        if simple in ('config', 'configuration', 'settings'):
            return cls(kind='config', data=None)
        if simple in ('mic_off', 'microphone_off', 'mute'):
            return cls(kind='mic_off', data=None)
        if simple.startswith('data:image/') or simple.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')):
            return cls(kind='image', data=None)
        if simple.startswith('data:audio/') or simple.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac', '.opus')):
            return cls(kind='audio', data=None)

        try:
            parsed = json.loads(json_part)
        except Exception:
            return cls(kind='other', data=None)

        if isinstance(parsed, dict):
            return cls(kind=classify(parsed), data=parsed)

        # If it's a list, try first dict element
        if isinstance(parsed, list) and parsed:
            first = parsed[0]
            if isinstance(first, dict):
                return cls(kind=classify(first), data=first)

        return cls(kind='other', data=None)

    def is_image(self) -> bool:
        return self.kind == 'image'

    def is_audio(self) -> bool:
        return self.kind == 'audio'

    def is_reset_command(self) -> bool:
        return self.kind == 'reset'

    def is_config(self) -> bool:
        return self.kind == 'config'

    def is_mic_off(self) -> bool:
        return self.kind == 'mic_off'
