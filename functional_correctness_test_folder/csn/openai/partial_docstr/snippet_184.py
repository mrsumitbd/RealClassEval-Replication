
import re
from typing import List


class Encoder:
    """
    Simple percent‑encoding implementation.
    Safe characters are ASCII letters, digits, '-', '.', '_', '~'.
    """

    _safe_chars: set = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")

    def needsEncoding(self, s: str) -> bool:
        """
        Return True if the string contains any character that is not in the safe set.
        """
        for ch in s:
            if ch not in self._safe_chars:
                return True
        return False

    def encode(self, s: str) -> str:
        """
        Percent‑encode all characters that are not in the safe set.
        """
        result: List[str] = []
        for ch in s:
            if ch in self._safe_chars:
                result.append(ch)
            else:
                result.append(f"%{ord(ch):02X}")
        return "".join(result)

    def decode(self, s: str) -> str:
        """
        Decode percent‑encoded sequences back to their original characters.
        Invalid sequences are left unchanged.
        """
        def _replace(match: re.Match) -> str:
            hex_value = match.group(1)
            try:
                return chr(int(hex_value, 16))
            except ValueError:
                return match.group(0)

        return re.sub(r"%([0-9A-Fa-f]{2})", _replace, s)
