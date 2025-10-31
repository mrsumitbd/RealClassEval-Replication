import json
from typing import Any, Dict, Iterable, Union


class CkClass:
    FLAG_NAMES: Union[Dict[int, str], Iterable[str]] = {}
    STATE_NAMES: Dict[Any, str] = {}

    def __init__(self, flags: Any = None, state: Any = None, **kwargs):
        self.flags = flags
        self.state = state
        for k, v in kwargs.items():
            setattr(self, k, v)

    def flags2text(self) -> str:
        f = getattr(self, "flags", None)

        if f is None:
            return ""

        # If already textual or a collection of strings
        if isinstance(f, str):
            return f
        if isinstance(f, (set, list, tuple)) and all(isinstance(x, str) for x in f):
            return ", ".join(sorted(f))

        # If numeric bitmask, try to map using FLAG_NAMES
        if isinstance(f, int):
            names = []
            extras = 0

            # Dict mapping bit -> name
            if isinstance(self.FLAG_NAMES, dict) and self.FLAG_NAMES:
                for bit, name in self.FLAG_NAMES.items():
                    try:
                        bit_int = int(bit)
                    except Exception:
                        continue
                    if bit_int != 0 and (f & bit_int) == bit_int:
                        names.append(str(name))
                # compute extras not covered by known bits
                known_mask = 0
                for bit in self.FLAG_NAMES:
                    try:
                        known_mask |= int(bit)
                    except Exception:
                        continue
                extras = f & ~known_mask

            # Sequence mapping by bit position
            elif isinstance(self.FLAG_NAMES, (list, tuple)) and self.FLAG_NAMES:
                for idx, name in enumerate(self.FLAG_NAMES):
                    if name and (f & (1 << idx)):
                        names.append(str(name))
                # extras beyond provided names
                max_known_mask = (1 << len(self.FLAG_NAMES)) - 1
                extras = f & ~max_known_mask
            else:
                # No names available, just return numeric forms
                return f"0x{f:X} ({f})"

            parts = []
            if names:
                parts.append(", ".join(sorted(names)))
            if extras:
                parts.append(f"extra=0x{extras:X}")
            if not parts:
                parts.append("0")
            return " | ".join(parts)

        # Fallback textualization
        return str(f)

    def state2text(self) -> str:
        s = getattr(self, "state", None)
        if s is None:
            return ""
        if self.STATE_NAMES:
            return self.STATE_NAMES.get(s, str(s))
        return str(s)

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            # Skip callables
            if callable(v):
                continue
            # Serialize simply
            try:
                json.dumps(v)
                out[k] = v
            except Exception:
                out[k] = str(v)

        # Augment with human-readable forms
        out["flags_text"] = self.flags2text()
        out["state_text"] = self.state2text()
        return out

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)
