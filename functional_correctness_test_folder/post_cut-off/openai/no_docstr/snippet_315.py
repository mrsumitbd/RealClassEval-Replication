
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Minimal placeholder for AppContext used in the mixin


@dataclass
class AppContext:
    logs_dir: Path | str  # directory containing server log files


class PlayerMixin:
    """
    Mixin providing player‑related utilities.

    The mixin keeps an in‑memory list of player dictionaries.  Each player
    dictionary must contain at least a ``name`` key; additional keys are
    accepted as provided by the caller.
    """

    # internal storage for player data
    _players_data: List[Dict[str, str]] = []

    def parse_player_cli_argument(self, player_string: str) -> Dict[str, str]:
        """
        Parse a CLI argument describing a player.

        The argument is expected to be a comma‑separated list of key=value
        pairs, e.g. ``"name=Alice,score=42"``.  Keys and values are stripped
        of surrounding whitespace.  Empty keys are ignored.

        Returns a dictionary mapping keys to values.
        """
        result: Dict[str, str] = {}
        if not player_string:
            return result

        for part in player_string.split(","):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key:
                result[key] = value
        return result

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        """
        Persist a list of player dictionaries.

        The data is appended to the internal list.  The method returns the
        new total number of stored players.
        """
        if not isinstance(players_data, list):
            raise TypeError("players_data must be a list of dicts")
        for entry in players_data:
            if not isinstance(entry, dict):
                raise TypeError("each player entry must be a dict")
            # Ensure at least a name key exists
            if "name" not in entry:
                raise ValueError("player entry missing required 'name' key")
            self._players_data.append(entry)
        return len(self._players_data)

    def get_known_players(self) -> List[Dict[str, str]]:
        """
        Return a shallow copy of the internal player list.
        """
        return list(self._players_data)

    def discover_and_store_players_from_all_server_logs(
        self, app_context: Optional[AppContext] = None
    ) -> Dict[str, Any]:
        """
        Scan all log files in the directory specified by ``app_context.logs_dir``
        for lines that contain player information and store the discovered
        players.

        Expected log line format (case‑insensitive):
            "Player: name=Bob,score=10"

        The method returns a dictionary containing:
            - ``found``: number of player entries discovered
            - ``stored``: number of entries actually stored
            - ``errors``: list of error messages encountered
        """
        if app_context is None:
            raise ValueError("app_context must be provided")

        logs_dir = Path(app_context.logs_dir)
        if not logs_dir.is_dir():
            raise FileNotFoundError(f"Logs directory not found: {logs_dir}")

        player_pattern = re.compile(r"Player:\s*(.+)", re.IGNORECASE)
        discovered: List[Dict[str, str]] = []
        errors: List[str] = []

        for log_file in logs_dir.glob("*.log"):
            try:
                with log_file.open("r", encoding="utf-8") as fh:
                    for line_no, line in enumerate(fh, start=1):
                        match = player_pattern.search(line)
                        if match:
                            raw = match.group(1)
                            try:
                                player = self.parse_player_cli_argument(raw)
                                if player:
                                    discovered.append(player)
                            except Exception as exc:
                                errors.append(
                                    f"{log_file}:{line_no} parse error: {exc}"
                                )
            except Exception as exc:
                errors.append(f"Failed to read {log_file}: {exc}")

        stored_count = self.save_player_data(discovered)

        return {
            "found": len(discovered),
            "stored": stored_count,
            "errors": errors,
        }
