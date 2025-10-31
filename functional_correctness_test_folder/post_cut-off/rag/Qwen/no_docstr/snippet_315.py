
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
import re
from core.server.player_mixin import ServerPlayerMixin
from core.bedrock_server import BedrockServer
from core.exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from core.settings import settings


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.
        '''
        if not isinstance(player_string, str) or not player_string.strip():
            raise UserInputError("Player string must be a non-empty string.")

        player_pattern = re.compile(r'\s*([\w\s]+)\s*:\s*(\d+)\s*')
        players_data = []
        for player_entry in player_string.split(','):
            match = player_pattern.match(player_entry)
            if not match:
                raise UserInputError(
                    f"Invalid player entry format: {player_entry.strip()}")
            name, xuid = match.groups()
            if not name.strip() or not xuid.strip():
                raise UserInputError(
                    f"Player name or XUID cannot be empty: {player_entry.strip()}")
            players_data.append({"name": name.strip(), "xuid": xuid.strip()})

        self.save_player_data(players_data)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.
        '''
        if not isinstance(players_data, list):
            raise UserInputError(
                "Players data must be a list of dictionaries.")

        existing_players = {
            player['xuid']: player for player in self.get_known_players()}
        new_or_updated_players = []

        for player in players_data:
            if not isinstance(player, dict) or 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    "Each player entry must be a dictionary with 'name' and 'xuid' keys.")
            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError("Player name and XUID must be strings.")
            if not player['name'].strip() or not player['xuid'].strip():
                raise UserInputError("Player name and XUID must be non-empty.")

            xuid = player['xuid']
            if xuid in existing_players:
                existing_player = existing_players[xuid]
                if existing_player['name'] != player['name']:
                    existing_player['name'] = player['name']
                    new_or_updated_players.append(existing_player)
            else:
                new_or_updated_players.append(player)

        if not new_or_updated_players:
            return 0

        # Assuming there's a method to save players to the database
        self._save_to_database(new_or_updated_players)
        return len(new_or_updated_players)

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        '''
        # Assuming there's a method to retrieve players from the database
        return self._retrieve_from_database()

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.
        '''
        server_base_dir = settings['paths.servers']
        if not server_base_dir or not Path(server_base_dir).is_dir():
            raise AppFileNotFoundError(
                f"Server base directory not found: {server_base_dir}")

        total_entries_in_logs = 0
        unique_players_submitted_for_saving = 0
        actually_saved_or_updated_in_db = 0
        scan_errors = []

        for server_dir in Path(server_base_dir).iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir, app_context)
                    if server.is_valid and server.is_installed:
                        players = server.scan_log_for_players()
                        total_entries_in_logs += len(players)
                        unique_players = {
                            player['xuid']: player for player in players}
                        unique_players_submitted_for_saving += len(
                            unique_players)
                        actually_saved_or_updated_in_db += self.save_player_data(
                            list(unique_players.values()))
                except Exception as e:
                    scan_errors.append(
                        {"server": server_dir.name, "error": str(e)})

        try:
            # Final save operation to ensure all data is committed
            self._save_to_database()
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(
                "Failed to save player data to the database.") from e

        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": unique_players_submitted_for_saving,
            "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
            "scan_errors": scan_errors
        }

    def _save_to_database(self, players: Optional[List[Dict[str, str]]] = None) -> None:
        # Placeholder for actual database save logic
        pass

    def _retrieve_from_database(self) -> List[Dict[str, str]]:
        # Placeholder for actual database retrieve logic
        return []
