
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Assuming these are defined elsewhere in the project
from .core.bedrock_server import BedrockServer
from .core.server.player_mixin import ServerPlayerMixin
from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from .app_context import AppContext
from .settings import settings


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        # For demonstration purposes, this method is left unimplemented
        pass

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.
        This method merges the provided ``players_data`` with any existing player
        data in the database.
        The merging logic is as follows:
            - If a player's XUID from ``players_data`` already exists in the database,
              their entry (name and XUID) is updated if different.
            - If a player's XUID is new, their entry is added to the database.
        Args:
            players_data (List[Dict[str, str]]): A list of player dictionaries.
                Each dictionary must contain string values for ``"name"`` and ``"xuid"`` keys.
                Both name and XUID must be non-empty.
        Returns:
            int: The total number of players that were newly added or had their
            existing entry updated. Returns 0 if no changes were made.
        Raises:
            UserInputError: If ``players_data`` is not a list, or if any dictionary
                within it does not conform to the required format (missing keys,
                non-string values, or empty name/XUID).
        '''
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list")

        existing_players = self.get_known_players()
        existing_players_dict = {player['xuid']                                 : player for player in existing_players}

        updated_count = 0
        for player in players_data:
            if not isinstance(player, dict) or 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    "Each player must be a dictionary with 'name' and 'xuid' keys")
            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError("Both 'name' and 'xuid' must be strings")
            if not player['name'] or not player['xuid']:
                raise UserInputError(
                    "Both 'name' and 'xuid' must be non-empty")

            xuid = player['xuid']
            if xuid in existing_players_dict:
                if existing_players_dict[xuid] != player:
                    existing_players_dict[xuid] = player
                    updated_count += 1
            else:
                existing_players_dict[xuid] = player
                updated_count += 1

        # Assuming a database or data storage mechanism is available
        # For demonstration, we'll just store it in a file
        try:
            with open('players.json', 'w') as f:
                import json
                json.dump(list(existing_players_dict.values()), f)
        except Exception as e:
            raise FileOperationError("Failed to save player data") from e

        return updated_count

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        try:
            with open('players.json', 'r') as f:
                import json
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            logging.error("Failed to load known players: %s", e)
            return []

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.
        This comprehensive method performs the following actions:
            1. Iterates through all subdirectories within the application's base server
               directory (defined by ``settings['paths.servers']``).
            2. For each subdirectory, it attempts to instantiate a
               :class:`~.core.bedrock_server.BedrockServer` object.
            3. If the server instance is valid and installed, it calls the server's
               :meth:`~.core.server.player_mixin.ServerPlayerMixin.scan_log_for_players`
               method to extract player names and XUIDs from its logs.
            4. All player data discovered from all server logs is aggregated.
            5. Unique player entries (based on XUID) are then saved to the database
               using :meth:`.save_player_data`.
        Args:
            None
        Returns:
            Dict[str, Any]: A dictionary summarizing the discovery and saving operation,
            containing the following keys:
                - ``"total_entries_in_logs"`` (int): The total number of player entries
                  (possibly non-unique) found across all server logs.
                - ``"unique_players_submitted_for_saving"`` (int): The number of unique
                  player entries (by XUID) that were attempted to be saved.
                - ``"actually_saved_or_updated_in_db"`` (int): The number of players
                  that were newly added or updated in the database
                  by the :meth:`.save_player_data` call.
                - ``"scan_errors"`` (List[Dict[str, str]]): A list of dictionaries,
                  where each entry represents an error encountered while scanning a
                  specific server's logs or saving the global player DB. Each error
                  dictionary contains ``"server"`` (str, server name or "GLOBAL_PLAYER_DB")
                  and ``"error"`` (str, error message).
        Raises:
            AppFileNotFoundError: If the main server base directory
                (``settings['paths.servers']``) is not configured or does not exist.
            FileOperationError: If the final save operation to the database
                (via :meth:`.save_player_data`) fails.
                Note that errors during individual server log scans are caught and
                reported in the ``"scan_errors"`` part of the return value.
        '''
        servers_dir = Path(settings['paths.servers'])
        if not servers_dir.exists():
            raise AppFileNotFoundError("Server base directory does not exist")

        total_entries_in_logs = 0
        all_players = {}
        scan_errors = []

        for server_dir in servers_dir.iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir)
                    if server.is_installed():
                        players = server.scan_log_for_players()
                        total_entries_in_logs += len(players)
                        for player in players:
                            all_players[player['xuid']] = player
                except Exception as e:
                    scan_errors.append(
                        {"server": server_dir.name, "error": str(e)})

        unique_players_submitted_for_saving = len(all_players)
        try:
            actually_saved_or_updated_in_db = self.save_player_data(
                list(all_players.values()))
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(
                "Failed to save player data to database") from e

        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": unique_players_submitted_for_saving,
            "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
            "scan_errors": scan_errors
        }
