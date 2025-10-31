import dataclasses
import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclasses.dataclass(frozen=True)
class MediaPart:
    '''A part of media data.'''
    raw: Any = field(default=None)
    type: Optional[str] = field(default=None)

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        '''Creates a Media Part from a JSON part.'''
        if not isinstance(json_part, str) or not json_part.strip():
            raise ValueError("json_part must be a non-empty JSON string")
        try:
            obj = json.loads(json_part)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}") from e

        if isinstance(obj, dict):
            t = (
                obj.get("type")
                or obj.get("kind")
                or obj.get("name")
                or (next(iter(obj)) if len(obj) == 1 and isinstance(next(iter(obj)), str) else None)
            )
            if isinstance(t, str):
                t = t.strip() or None
            return cls(raw=obj, type=t)
        else:
            # Wrap non-dict JSON into a dict for uniform handling
            return cls(raw={"value": obj}, type=None)

    def _type_str(self) -> str:
        return (self.type or "").lower()

    def _content_type(self) -> str:
        if isinstance(self.raw, dict):
            ct = self.raw.get("content_type") or self.raw.get(
                "mime") or self.raw.get("mimetype")
            if isinstance(ct, str):
                return ct.lower()
        return ""

    def is_image(self) -> bool:
        '''Returns whether the part is an image.'''
        t = self._type_str()
        ct = self._content_type()
        if ct.startswith("image/"):
            return True
        if t in {"image"}:
            return True
        # Common stream/event types containing image
        if "image" in t:
            return True
        # Heuristic based on keys
        if isinstance(self.raw, dict):
            if any(k in self.raw for k in ("image", "image_url", "images", "img")):
                return True
        return False

    def is_audio(self) -> bool:
        '''Returns whether the part is audio.'''
        t = self._type_str()
        ct = self._content_type()
        if ct.startswith("audio/"):
            return True
        if t in {"audio"}:
            return True
        if "audio" in t:
            return True
        if isinstance(self.raw, dict):
            if any(k in self.raw for k in ("audio", "audio_url", "audio_bytes", "sound")):
                return True
        return False

    def is_reset_command(self) -> bool:
        '''Returns whether the part is a reset command.'''
        t = self._type_str()
        if t in {"reset", "reset_thread", "clear", "input_audio_buffer.clear"}:
            return True
        if isinstance(self.raw, dict):
            cmd = self.raw.get("command") or self.raw.get("action")
            if isinstance(cmd, str) and cmd.lower() in {"reset", "clear", "reset_thread"}:
                return True
            flag = self.raw.get("reset") or self.raw.get("clear")
            if isinstance(flag, bool) and flag:
                return True
        return False

    def is_config(self) -> bool:
        '''Returns whether the part is a config.'''
        t = self._type_str()
        if t in {"config", "configuration", "session.update", "settings"}:
            return True
        if isinstance(self.raw, dict):
            if "config" in self.raw or "configuration" in self.raw or "settings" in self.raw:
                return True
            if self.raw.get("type") == "message" and self.raw.get("role") == "system":
                return True
        return False

    def is_mic_off(self) -> bool:
        '''Returns whether the part indicates the client has turned off the mic.'''
        t = self._type_str()
        if t in {"mic_off", "audio_stop", "input_audio_buffer.commit", "stop_listening"}:
            return True
        if isinstance(self.raw, dict):
            mic = self.raw.get("mic")
            if isinstance(mic, bool) and not mic:
                return True
            state = self.raw.get("state")
            if isinstance(state, str) and state.lower() in {"mic_off", "stopped", "muted"}:
                return True
        return False
