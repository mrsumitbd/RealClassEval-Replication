
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import the application‑specific exceptions and helpers.
# These imports are intentionally lazy to avoid circular dependencies.
try:
    from .exceptions import AppFileNotFoundError, FileOperationError, UserInputError
except Exception:  # pragma: no cover
    # In case the module structure differs, provide minimal stubs.
    class AppFileNotFoundError(Exception):
        pass

    class FileOperationError(Exception):
        pass

    class UserInputError(Exception):
        pass

try:
    from .settings import settings  # type: ignore
except Exception:  # pragma: no cover
    settings = {"paths": {"servers": ""}}

try:
    from .core.bedrock_server import BedrockServer  # type: ignore
except Exception:  # pragma: no cover
    BedrockServer = None  # type: ignore


class PlayerMixin:
    """
    Mixin class for BedrockServerManager that handles player database management.
    """

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------
    def _get_db_connection(self) -> sqlite3.Connection:
        """
        Return a SQLite connection to the player database.
        The database file is stored in the application data directory.
        """
        db_path = Path(settings.get("paths", {}).get(
            "data", ".")) / "players.db"
        conn = sqlite3.connect(db_path)
        self._ensure_db_table(conn)
        return conn

    def _ensure_db_table(self, conn: sqlite3.Connection) -> None:
        """
        Create the players table if it does not exist.
        """
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                xuid TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def parse_player_cli_argument(self, player_string: str) -> None:
        """
        Parse a CLI argument that represents a player.
        Accepted formats:
            - "name:xuid"
            - "xuid"
            - "name"
        The method validates the format but does not store the result.
        """
        if not isinstance(player_string, str) or not player_string.strip():
            raise UserInputError("Player argument must be a non‑empty string")

        parts = player_string.split(":")
        if len(parts) == 2:
            name, xuid = parts[0].strip(), parts[1].strip()
        elif len(parts) == 1:
            # Try to guess which part is xuid (numeric)
            part = parts[0].strip()
            if part.isdigit():
                xuid, name = part, ""
            else:
                name, xuid = part, ""
        else:
            raise UserInputError(
                f"Invalid player argument format: {player_string}")

        if not xuid:
            raise UserInputError("XUID is required in the player argument")
        if not name:
            raise UserInputError("Name is required in the player argument")

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        """
        Saves or updates player data in the database.
        """
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list")

        # Validate each entry
        for entry in players_data:
            if not isinstance(entry, dict):
                raise UserInputError("Each player entry must be a dict")
            if "name" not in entry or "xuid" not in entry:
                raise UserInputError(
                    "Each player entry must contain 'name' and 'xuid'")
            if not isinstance(entry["name"], str) or not isinstance(entry["xuid"], str):
                raise UserInputError("'name' and 'xuid' must be strings")
            if not entry["name"].strip() or not entry["xuid"].strip():
                raise UserInputError("'name' and 'xuid' cannot be empty")

        conn = self._get_db_connection()
        cursor = conn.cursor()

        # Fetch existing players
        cursor.execute("SELECT xuid, name FROM players")
        existing = {row[0]: row[1] for row in cursor.fetchall()}

        changes = 0
        for entry in players_data:
            xuid = entry["xuid"].strip()
            name = entry["name"].strip()
            if xuid in existing:
                if existing[xuid] != name:
                    cursor.execute(
                        "UPDATE players SET name = ? WHERE xuid = ?", (
                            name, xuid)
                    )
                    changes += 1
            else:
                cursor.execute(
                    "INSERT INTO players (xuid, name) VALUES (?, ?)", (xuid, name)
                )
                changes += 1

        if changes:
            conn.commit()
        conn.close()
        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        """
        Retrieves all known players from the database.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, xuid FROM players")
        rows = cursor.fetchall()
        conn.close()
        return [{"name": name, "xuid": xuid} for name, xuid in rows]

    def discover_and_store_players_from_all_server_logs(
        self, app_context: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Scans all server logs for player data and updates the central player database.
        """
        base_dir = settings.get("paths", {}).get("servers")
        if not base_dir:
            raise AppFileNotFoundError("Server base directory not configured")

        base_path = Path(base_dir)
        if not base_path.is_dir():
            raise AppFileNotFoundError(
                f"Server base directory does not exist: {base_dir}")

        all_entries: List[Dict[str, str]] = []
        scan_errors: List[Dict[str, str]] = []

        for server_dir in base_path.iterdir():
            if not server_dir.is_dir():
                continue
            server_name = server_dir.name
            try:
                if BedrockServer is None:
                    raise ImportError("BedrockServer class not available")
                server = BedrockServer(server_dir)
                if not server.is_installed:
                    continue
                # The server instance should expose a method to scan logs
                players = server.scan_log_for_players()
                if isinstance(players, list):
                    all_entries.extend(players)
                else:
                    raise ValueError(
                        "scan_log_for_players did not return a list")
            except Exception as exc:
                scan_errors.append(
                    {"server": server_name, "error": str(exc)}
                )

        total_entries_in_logs = len(all_entries)
        # Deduplicate by XUID
        unique_players_dict: Dict[str, str] = {}
        for entry in all_entries:
