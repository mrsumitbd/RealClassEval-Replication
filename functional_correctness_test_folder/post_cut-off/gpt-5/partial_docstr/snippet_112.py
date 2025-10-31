from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable, Optional, Tuple


class SessionResetHandler:
    '''Handles detection and recovery from Claude session resets'''

    def __init__(self, log_func: Optional[Callable[[str], None]] = None):
        '''Initialize the handler
        Args:
            log_func: Optional logging function
        '''
        self._log_func = log_func
        self._reset_pending: bool = False
        self._last_reset_command: Optional[str] = None
        self._last_reset_time: Optional[float] = None

    def _log(self, message: str) -> None:
        if self._log_func:
            try:
                self._log_func(message)
            except Exception:
                pass

    def check_for_reset_command(self, command: str) -> bool:
        '''Check if a command is a session reset command'''
        if not isinstance(command, str):
            return False
        cmd = command.strip().lower()
        if not cmd:
            return False
        is_reset = cmd.startswith("/clear") or cmd.startswith("/reset")
        return is_reset

    def mark_reset_detected(self, command: str) -> None:
        '''Mark that a session reset has been detected'''
        self._reset_pending = True
        self._last_reset_command = command
        self._last_reset_time = time.time()
        self._log(f"Session reset detected: {command!r}")

    def is_reset_pending(self) -> bool:
        return self._reset_pending

    def clear_reset_state(self) -> None:
        '''Clear the reset state after handling'''
        self._log("Clearing session reset state")
        self._reset_pending = False
        self._last_reset_command = None
        self._last_reset_time = None

    def get_reset_info(self) -> Tuple[Optional[str], Optional[float]]:
        return self._last_reset_command, self._last_reset_time

    def find_reset_session_file(
        self,
        project_dir: Path,
        current_file: Path,
        max_wait: float = 10.0,
    ) -> Optional[Path]:
        '''Find a JSONL session file in the project dir that begins with a clear/reset command'''
        start = time.time()
        project_dir = Path(project_dir)
        current_file = Path(current_file)

        search_dirs = []
        if current_file.is_file():
            search_dirs.append(current_file.parent)
        if project_dir.exists():
            search_dirs.append(project_dir)

        seen: set[Path] = set()

        def iter_jsonl_paths():
            yielded = set()
            for d in search_dirs:
                if not d.exists():
                    continue
                # search direct and recursive
                for p in d.glob("*.jsonl"):
                    if p not in yielded:
                        yielded.add(p)
                        yield p
                for p in d.rglob("*.jsonl"):
                    if p not in yielded:
                        yielded.add(p)
                        yield p

        while time.time() - start <= max_wait:
            newest_match: Optional[Path] = None
            newest_mtime = -1.0

            for path in iter_jsonl_paths():
                if path in seen:
                    # still consider if file changed
                    pass
                try:
                    if not path.exists() or path.stat().st_size == 0:
                        continue
                    if self._file_has_clear_command(path):
                        mtime = path.stat().st_mtime
                        if mtime > newest_mtime:
                            newest_mtime = mtime
                            newest_match = path
                except Exception:
                    continue

            if newest_match is not None:
                self._log(f"Found session reset file: {str(newest_match)}")
                return newest_match

            time.sleep(0.2)

        self._log("No session reset file found within timeout")
        return None

    def _file_has_clear_command(self, file: Path) -> bool:
        '''Check if a JSONL file starts with the /clear command'''
        try:
            with open(file, "r", encoding="utf-8") as f:
                first_nonempty = None
                for line in f:
                    if line.strip():
                        first_nonempty = line.strip()
                        break
                if first_nonempty is None:
                    return False

                content_text = None

                # Try JSON parse
                try:
                    obj = json.loads(first_nonempty)
                    # Common shapes:
                    # {"content": "/clear ..."}
                    if isinstance(obj, dict):
                        if "content" in obj:
                            cont = obj["content"]
                            if isinstance(cont, str):
                                content_text = cont
                            elif isinstance(cont, list):
                                # Claude-like message parts [{"type":"text","text":"..."}]
                                texts = []
                                for part in cont:
                                    if isinstance(part, dict):
                                        t = part.get("text")
                                        if isinstance(t, str):
                                            texts.append(t)
                                if texts:
                                    content_text = " ".join(texts)
                        # Fallback to "text" field
                        if content_text is None and isinstance(obj.get("text"), str):
                            content_text = obj["text"]
                except Exception:
                    # Not JSON; treat as plain text
                    content_text = first_nonempty

                if not isinstance(content_text, str):
                    return False

                cmd = content_text.lstrip().lower()
                return cmd.startswith("/clear") or cmd.startswith("/reset")
        except Exception:
            return False
