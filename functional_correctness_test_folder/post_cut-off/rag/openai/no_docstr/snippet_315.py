
# -*- coding: utf-8 -*-
"""
PlayerMixin implementation for BedrockServerManager.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

# Import the settings module – the project is expected to expose a `settings`
# dictionary that contains the path configuration.
try:
    from .settings import settings  # type: ignore
except Exception:  # pragma: no cover
    # Fallback for environments where the settings module is not available.
    settings = {}

# Import the BedrockServer class – this is the class used to instantiate
# individual server instances.
try:
    from .core.bedrock_server import BedrockServer  # type: ignore
except Exception:  # pragma: no cover
    BedrockServer = None  # type: ignore

# Import the AppContext type – used only for type hints.
try:
    from .core.app_context import AppContext  # type: ignore
except Exception:  # pragma: no cover
    AppContext = None  # type: ignore

# Import custom exception classes – if they are not available we create
# lightweight substitutes so that the mixin can still be used.
try:
    from .exceptions import (
        UserInputError,
        AppFileNotFoundError,
        FileOperationError,
    )  # type: ignore
except Exception:  # pragma: no cover
    class UserInputError(ValueError):
        """Raised when user input is invalid."""

    class AppFileNotFoundError(FileNotFoundError):
        """Raised when an application file or directory is missing."""

    class FileOperationError(IOError):
        """Raised when a file operation fails."""


class PlayerMixin:
    """
    Mixin class for BedrockServerManager that handles player database management.
    """

    # The mixin expects the host class to provide a ``_player_db`` attribute
    # that behaves like a mapping from XUID to player name.  If the attribute
    # does not exist, an in‑memory dictionary is created lazily.
    @property
    def _player_db(self) -> Dict[str, str]:
        if not hasattr(self, "_player_db_storage"):
            self._player_db_storage = {}
        return self._player_db_storage

    # --------------------------------------------------------------------- #
    # 1. CLI argument parsing
    # --------------------------------------------------------------------- #
    def parse_player_cli_argument(self, player_string: str) -> List[Dict[str, str]]:
        """
        Parses a comma-separated string of 'player_name:xuid' pairs and
        returns a list of dictionaries with keys ``name`` and ``xuid``.
        """
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players: List[Dict[str, str]] = []

        for part in player_string.split(","):
            part = part.strip()
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
                    f"Invalid player entry '{part}'. Name and XUID must be non‑empty."
                )

            players.append({"name": name, "xuid": xuid})

        return players

    # --------------------------------------------------------------------- #
    # 2. Persisting player data
    # --------------------------------------------------------------------- #
    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        """
        Saves or updates player data in the database.
        """
        if not isinstance(players_data, list):
            raise UserInputError(
                "players_data must be a list of dictionaries.")

        changes = 0
        db = self._player_db

        for entry in players_data:
            if not isinstance(entry, dict):
                raise UserInputError("Each player entry must
