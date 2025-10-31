
import os
import re
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------- #
# Exception definitions (fallbacks if the real ones are not available)
# --------------------------------------------------------------------------- #
try:
    from .exceptions import (
        UserInputError,
        AppFileNotFoundError,
        FileOperationError,
    )
except Exception:  # pragma: no cover
    class UserInputError(ValueError):
        """Raised for invalid user input."""

    class AppFileNotFoundError(FileNotFoundError):
        """Raised when an expected application file or directory is missing."""

    class FileOperationError(IOError):
        """Raised when a file operation fails."""


# --------------------------------------------------------------------------- #
# Settings import (fallback to empty dict if not configured)
# --------------------------------------------------------------------------- #
try:
    from . import settings  # type: ignore
except Exception:  # pragma: no cover
    settings = {"paths": {"servers": ""}}


# --------------------------------------------------------------------------- #
# BedrockServer import (fallback to dummy class if not available)
# --------------------------------------------------------------------------- #
try:
    from .core.bedrock_server import BedrockServer  # type: ignore
except Exception:  # pragma: no cover
    class BedrockServer:
        """Dummy BedrockServer used when the real implementation is unavailable."""

        def __init__(self, path: str):
            self.path = path
            self.installed = True

        def scan_log_for_players(self) -> List[Dict[str, str]]:
            """Return an empty list – real implementation should parse logs."""
            return []


# --------------------------------------------------------------------------- #
# PlayerMixin implementation
# --------------------------------------------------------------------------- #
class PlayerMixin:
    """
    Mixin class for BedrockServerManager that handles player database management.
    """

    # In‑memory player database: mapping from XUID to name
    _player_db: Dict[str, str] = {}

    # ----------------------------------------------------------------------- #
    # Helper methods
    # ----------------------------------------------------------------------- #
    @staticmethod
    def _validate_player_dict(player: Dict[str, str]) -> None:
        """Validate that a player dict contains non‑empty string 'name' and 'xuid'."""
        if not isinstance(player, dict):
            raise UserInputError("Player entry must be a dictionary.")
        if "name" not in player or "xuid" not in player:
            raise UserInputError(
                "Player entry must contain 'name' and 'xuid' keys.")
        name = player["name"]
        xuid = player["xuid"]
        if not isinstance(name, str) or not isinstance(xuid, str):
            raise UserInputError("'name' and 'xuid' must be strings.")
        if not name.strip() or not xuid.strip():
            raise UserInputError("'name' and 'xuid' cannot be empty.")

    # ----------------------------------------------------------------------- #
    # Public API
    # ----------------------------------------------------------------------- #
    def parse_player_cli_argument(self, player_string: str) -> List[Dict[str, str]]:
        """
        Parses a comma‑separated string of 'player_name:xuid' pairs and returns a list
        of player dictionaries. Whitespace around names, XUIDs, commas, and colons
        is ignored.

        Args:
            player_string (str): The comma‑separated string of player data.

        Returns:
            List[Dict[str, str]]: A list of player dictionaries.

        Raises:
            UserInputError: If any player pair does not conform to the
                "name:xuid" format, or if a name or XUID is empty after stripping.
        """
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players: List[Dict[str, str]] = []
        # Split on commas that are not inside quotes (simple split is fine here)
        for part in re.split(r",\s*", player_string.strip()):
            if not part:
                continue
            if ":" not in part:
                raise UserInputError(
                    f"Invalid player entry '{part}'. Expected format 'name:xuid'."
                )
            name, xuid = part.split(":", 1)
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                raise UserInputError(
                    f"Invalid player entry '{part}'. Name and XUID cannot be empty."
                )
            players.append({"name": name, "xuid": xuid})
        return players

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        """
        Saves or updates player data in the in‑memory database.

        Args:
            players_data (List[Dict[str, str]]): A list of player dictionaries.

        Returns:
            int: The total number of players that were newly added or had their
            existing entry updated.

        Raises:
            UserInputError: If `players_data` is not a list, or if any dictionary
                within it does not conform to the required format.
        """
        if not isinstance(players_data, list):
            raise UserInputError(
                "players_data must be a list of dictionaries.")

        changes = 0
        for player in players_data:
            self._validate_player_dict(player)
            xuid = player["xuid"]
            name = player["name"]
            existing_name = self._player_db.get(xuid)
            if existing_name is None:
                # New entry
                self._player_db[xuid] = name
                changes += 1
            elif existing_name != name:
                # Update existing entry
                self._player_db[xuid] = name
                changes += 1
        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        """
        Retrieves all known players from the in‑memory database.

        Returns:
            List[Dict[str, str]]: A list of player dictionaries.
        """
        return [{"name": name, "xuid": xuid} for xuid, name in self._player_db.items()]

    def discover_and_store_players_from_all_server_logs(
        self, app_context: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Scans all server logs for player data and updates the central player database.

        Args:
            app_context (Optional[Any]): Unused in this implementation but kept for
                API compatibility.

        Returns:
            Dict[str, Any]: Summary of the discovery and saving operation.
        """
        base_dir = settings.get("paths", {}).get("servers", "")
        if not base_dir or not os.path.isdir(base_dir):
            raise AppFileNotFoundError(
                f"Server
