from pathlib import Path
from typing import Optional, Tuple, Callable
import time
import re


class SessionResetHandler:

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        self._log = log_func or (lambda msg: None)
        self._reset_pending: bool = False
        self._last_reset_command: Optional[str] = None
        self._last_reset_time: Optional[float] = None
        self._reset_tokens = {
            "reset",
            "clear",
            "restart",
            "clear session",
            "reset session",
            "/reset",
            "/clear",
            "%%reset",
            ":reset",
        }
        token_words = [
            r"\breset\b",
            r"\bclear\b",
            r"\brestart\b",
            r"\bclear\s+session\b",
            r"\breset\s+session\b",
        ]
        self._content_regex = re.compile(
            "|".join(token_words), flags=re.IGNORECASE)

    def check_for_reset_command(self, command: str) -> bool:
        if command is None:
            return False
        text = command.strip().lower()
        if not text:
            return False
        if text in self._reset_tokens:
            return True
        for tok in self._reset_tokens:
            if text.startswith(tok + " ") or text.endswith(" " + tok):
                return True
        if self._content_regex.search(text) is not None:
            return True
        return False

    def mark_reset_detected(self, command: str) -> None:
        self._reset_pending = True
        self._last_reset_command = command
        self._last_reset_time = time.monotonic()
        self._log(f"Session reset detected: {command!r}")

    def is_reset_pending(self) -> bool:
        return self._reset_pending

    def clear_reset_state(self) -> None:
        self._reset_pending = False
        self._last_reset_command = None
        self._last_reset_time = None
        self._log("Session reset state cleared")

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return self._last_reset_command, self._last_reset_time

    def find_reset_session_file(self, project_dir: Path, current_file: Path, max_wait: float = 10.0) -> Optional[Path]:
        start = time.monotonic()
        candidates_specific = [
            ".reset",
            ".reset_session",
            "RESET",
            "RESET_SESSION",
            "reset",
            "reset_session",
            "clear_session",
            "CLEAR_SESSION",
            "clear_session.txt",
            "RESET.txt",
        ]
        name_patterns = ["*reset*", "*RESET*", "*clear*", "*CLEAR*"]

        def iter_candidates() -> Optional[Path]:
            try:
                if current_file and current_file.is_file() and self._file_has_clear_command(current_file):
                    return current_file
            except Exception:
                pass

            nearby = set()
            if current_file:
                p = current_file
                for _ in range(3):
                    p = p.parent
                    if not p or p == p.parent:
                        break
                    for nm in candidates_specific:
                        nearby.add(p / nm)
                    for nm in (".reset", ".reset_session"):
                        nearby.add(p / nm)

            for cand in nearby:
                try:
                    if cand.is_file():
                        if cand.suffix in ("", ".txt", ".reset") or cand.name.lower() in {"reset", "reset_session"}:
                            if self._file_has_clear_command(cand) or cand.stat().st_size == 0:
                                return cand
                except Exception:
                    continue

            search_root = project_dir if project_dir and project_dir.is_dir() else (
                current_file.parent if current_file else None)
            if search_root and search_root.is_dir():
                tried = set()
                for pat in name_patterns:
                    for path in search_root.rglob(pat):
                        if path in tried or not path.exists() or path.is_dir():
                            continue
                        tried.add(path)
                        try:
                            name_l = path.name.lower()
                            if any(key in name_l for key in ("reset", "clear")):
                                if self._file_has_clear_command(path) or path.suffix in ("", ".txt", ".reset"):
                                    return path
                        except Exception:
                            continue
            return None

        if max_wait <= 0:
            return iter_candidates()

        while True:
            found = iter_candidates()
            if found is not None:
                self._log(f"Found reset session file: {found}")
                return found
            if (time.monotonic() - start) >= max_wait:
                return None
            time.sleep(0.25)

    def _file_has_clear_command(self, file: Path) -> bool:
        try:
            if not file or not file.exists() or not file.is_file():
                return False
            name = file.name.lower()
            if name in {"reset", "reset_session", ".reset", ".reset_session", "clear_session"}:
                return True
            if any(k in name for k in ("reset", "clear")) and file.stat().st_size == 0:
                return True

            with file.open("r", encoding="utf-8", errors="ignore") as f:
                chunk = f.read(4096)
            if not chunk:
                return False
            text = chunk.strip().lower()
            if text.startswith(("#", "//", ";")) and len(text.splitlines()) == 1:
                text = text.lstrip("#/;").strip()
            if text in self._reset_tokens:
                return True
            if self._content_regex.search(text) is not None:
                return True
            for line in text.splitlines():
                s = line.strip().lower()
                if not s:
                    continue
                if s in self._reset_tokens:
                    return True
                if s.startswith(("!", "%", "%%", "/")):
                    s2 = s.lstrip("!%/").strip()
                    if s2 in self._reset_tokens:
                        return True
            return False
        except Exception:
            return False
