
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

# Import the required exceptions and utilities.  These are expected to be
# defined elsewhere in the project.  Importing them lazily allows the mixin
# to be used in environments where the full application context is not
# available (e.g. unit tests that mock the database).
try:
    from .exceptions import (
        UserInputError,
        AppFileNotFoundError,
        FileOperationError,
    )
except Exception:  # pragma: no cover
    # Fallback definitions for environments where the real exceptions are not
    # available.  These are minimal stand‑ins that preserve the public API.
    class UserInputError(ValueError):
        pass

    class AppFileNotFoundError(FileNotFoundError):
        pass

    class FileOperationError(RuntimeError):
        pass

# The settings module is expected to expose a dictionary with the
# application configuration.  Import it lazily to avoid circular imports.
try:
    from .settings import settings
except Exception:  # pragma: no cover
    settings = {}

# BedrockServer is the class that knows how to scan its own logs for
# player data.  Import it lazily as well.
try:
    from .core.bedrock_server import BedrockServer
except Exception:  # pragma: no cover
    BedrockServer = None  # type: ignore

# Optional type for the application context.  It is not used directly in
# the mixin but is part of the public signature.
try:
    from .core.app_context import AppContext
except Exception:  # pragma: no cover
    AppContext = None  # type: ignore


class PlayerMixin:
    """
    Mixin class for BedrockServerManager that handles player database management.
    """

    # ----------------------------------------------------------------------
    #  Helper methods
    # ----------------------------------------------------------------------
    @staticmethod
    def _validate_player_pair(name: str, xuid: str) -> Tuple[str, str]:
        """
        Validate a single player name/xuid pair.

        Raises:
            UserInputError: If either component is empty after stripping.
        """
        if not name:
            raise UserInputError("Player name cannot be empty.")
        if not xuid:
            raise UserInputError("Player XUID cannot be empty.")
        return name, xuid

    # ----------------------------------------------------------------------
    #  Public API
    # ----------------------------------------------------------------------
    def parse_player_cli_argument(self, player_string: str) -> List[Dict[str, str]]:
        """
        Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.

        Example:
            ``"Player One:12345, PlayerTwo:67890"``

        Args:
            player_string (str): The comma-separated string of player data.
                If empty or not a string, an empty list is returned.

        Raises:
            UserInputError: If any player pair within the string does not conform
                to the "name:xuid" format, or if a name or XUID is empty after stripping.
        """
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players: List[Dict[str, str]] = []
        for pair in player_string.split(","):
            pair = pair.strip()
            if not pair:
                continue
            if ":" not in pair:
                raise UserInputError(
                    f"Invalid player pair '{pair}'. Expected format 'name:xuid'.")
            name, xuid = pair.split(":", 1)
            name, xuid = name.strip(), xuid.strip()
            name, xuid = self._validate_player_pair(name, xuid)
            players.append({"name": name, "xuid": xuid})
        return players

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        """
        Saves or updates player data in the database.

        This method merges the provided ``players_data`` with any existing player
        data in the database.

        The merging logic is as follows:
