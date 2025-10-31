import dataclasses
import json
from typing import Any, Dict, Optional


@dataclasses.dataclass(frozen=True)
class MediaPart:
    type: str
    payload: Any

    @classmethod
    def from_json(cls, json_part: str) -> 'MediaPart':
        try:
            obj = json.loads(json_part)
        except Exception:
            # If it's not valid JSON, treat it as a raw string payload
            raw = json_part.strip()
            inferred_type = cls._infer_type_from_str(raw)
            return cls(type=inferred_type, payload=raw)

        inferred_type = cls._infer_type_from_obj(obj)
        return cls(type=inferred_type, payload=obj)

    def is_image(self) -> bool:
        if self.type.lower() in {"image", "input_image", "image_url", "image_file"}:
            return True
        if isinstance(self.payload, dict):
            return any([
                "image" in self.payload,
                "image_url" in self.payload,
                self._has_mime_prefix(self.payload, "image/"),
                self._has_nested_key(self.payload, {"type": "image"}),
            ])
        return False

    def is_audio(self) -> bool:
        if self.type.lower() in {"audio", "input_audio", "audio_url", "audio_file"}:
            return True
        if isinstance(self.payload, dict):
            return any([
                "audio" in self.payload,
                "audio_url" in self.payload,
                self._has_mime_prefix(self.payload, "audio/"),
                self._has_nested_key(self.payload, {"type": "audio"}),
            ])
        return False

    def is_reset_command(self) -> bool:
        if self.type.lower() in {"reset", "reset_command"}:
            return True
        if isinstance(self.payload, str):
            return self._matches_reset_str(self.payload)
        if isinstance(self.payload, dict):
            cmd = self._get_first_str(
                self.payload, ["command", "cmd", "action", "type"])
            if cmd and cmd.lower() in {"reset", "reset_command"}:
                return True
            val = self._get_first_bool(self.payload, ["reset"])
            if val is True:
                return True
        return False

    def is_config(self) -> bool:
        if self.type.lower() in {"config", "configuration", "settings"}:
            return True
        if isinstance(self.payload, dict):
            t = self._get_first_str(self.payload, ["type", "kind"])
            if t and t.lower() in {"config", "configuration", "settings"}:
                return True
            if "config" in self.payload or "configuration" in self.payload or "settings" in self.payload:
                return True
        return False

    def is_mic_off(self) -> bool:
        if self.type.lower() in {"mic_off", "mute", "microphone_off"}:
            return True
        if isinstance(self.payload, str):
            s = self.payload.strip().lower()
            if s in {"mic_off", "microphone_off", "mute", "/mic_off", "/mute"}:
                return True
        if isinstance(self.payload, dict):
            if self._get_first_bool(self.payload, ["mic_off", "micOff", "mute", "microphone_off", "microphoneOff"]) is True:
                return True
            cmd = self._get_first_str(
                self.payload, ["command", "action", "type"])
            if cmd and cmd.lower() in {"mic_off", "microphone_off", "mute"}:
                return True
            mic = self._get_first_str(self.payload, ["mic", "microphone"])
            if mic and mic.lower() in {"off", "mute", "muted"}:
                return True
        return False

    @staticmethod
    def _infer_type_from_str(s: str) -> str:
        low = s.strip().lower()
        if MediaPart._matches_reset_str(low):
            return "reset"
        if low in {"mic_off", "microphone_off", "mute", "/mic_off", "/mute"}:
            return "mic_off"
        return "unknown"

    @staticmethod
    def _matches_reset_str(s: str) -> bool:
        low = s.strip().lower()
        return low in {"reset", "/reset", "reset_command"}

    @staticmethod
    def _infer_type_from_obj(obj: Any) -> str:
        if isinstance(obj, dict):
            # Priority: explicit type
            t = MediaPart._get_first_str(obj, ["type", "kind"])
            if t:
                tl = t.lower()
                if tl in {
                    "image", "input_image", "image_url", "image_file",
                    "audio", "input_audio", "audio_url", "audio_file",
                    "reset", "reset_command",
                    "config", "configuration", "settings",
                    "mic_off", "microphone_off", "mute"
                }:
                    return tl
            # Heuristics for image
            if any(k in obj for k in ["image", "image_url", "imageUrl"]):
                return "image"
            if MediaPart._has_mime_prefix(obj, "image/"):
                return "image"
            # Heuristics for audio
            if any(k in obj for k in ["audio", "audio_url", "audioUrl"]):
                return "audio"
            if MediaPart._has_mime_prefix(obj, "audio/"):
                return "audio"
            # Reset
            if MediaPart._get_first_bool(obj, ["reset"]) is True:
                return "reset"
            cmd = MediaPart._get_first_str(obj, ["command", "cmd", "action"])
            if cmd and cmd.lower() in {"reset", "reset_command"}:
                return "reset"
            # Config
            if any(k in obj for k in ["config", "configuration", "settings"]):
                return "config"
            # Mic off
            if MediaPart._get_first_bool(obj, ["mic_off", "micOff", "mute", "microphone_off", "microphoneOff"]) is True:
                return "mic_off"
            mic = MediaPart._get_first_str(obj, ["mic", "microphone"])
            if mic and mic.lower() in {"off", "mute", "muted"}:
                return "mic_off"
        elif isinstance(obj, str):
            return MediaPart._infer_type_from_str(obj)
        return "unknown"

    @staticmethod
    def _has_mime_prefix(obj: Dict[str, Any], prefix: str) -> bool:
        mime = MediaPart._get_first_str(
            obj, ["mime", "mime_type", "mimeType", "content_type", "contentType"])
        if mime and mime.lower().startswith(prefix.lower()):
            return True
        # Sometimes nested under a 'file' or 'media' object
        for key in ("file", "media", "source"):
            sub = obj.get(key)
            if isinstance(sub, dict):
                sub_mime = MediaPart._get_first_str(
                    sub, ["mime", "mime_type", "mimeType", "content_type", "contentType"])
                if sub_mime and sub_mime.lower().startswith(prefix.lower()):
                    return True
        return False

    @staticmethod
    def _has_nested_key(obj: Dict[str, Any], required: Dict[str, Any]) -> bool:
        if not isinstance(obj, dict):
            return False
        for k, v in required.items():
            if obj.get(k) == v:
                return True
        for val in obj.values():
            if isinstance(val, dict) and MediaPart._has_nested_key(val, required):
                return True
        return False

    @staticmethod
    def _get_first_str(obj: Dict[str, Any], keys: Any) -> Optional[str]:
        for k in keys:
            v = obj.get(k)
            if isinstance(v, str):
                return v
        return None

    @staticmethod
    def _get_first_bool(obj: Dict[str, Any], keys: Any) -> Optional[bool]:
        for k in keys:
            v = obj.get(k)
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                lv = v.strip().lower()
                if lv in {"true", "yes", "1"}:
                    return True
                if lv in {"false", "no", "0"}:
                    return False
        return None
