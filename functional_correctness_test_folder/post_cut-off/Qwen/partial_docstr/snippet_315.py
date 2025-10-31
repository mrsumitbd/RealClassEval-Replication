
from typing import List, Dict, Any, Optional
from pathlib import Path
import os
import json
from core.bedrock_server import BedrockServer
from core.server.player_mixin import ServerPlayerMixin
from settings import settings
from exceptions import UserInputError, AppFileNotFoundError, FileOperationError


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        # Assuming player_string is in the format "name:xuid"
        parts = player_string.split(':')
        if len(parts) != 2 or not all(parts):
            raise UserInputError(
                "Player string must be in the format 'name:xuid' with non-empty values.")
        name, xuid = parts
        self.save_player_data([{"name": name, "xuid": xuid}])

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.
        '''
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list.")

        for player in players_data:
            if not isinstance(player, dict) or "name" not in player or "xuid" not in player:
                raise UserInputError(
                    "Each player entry must be a dictionary with 'name' and 'xuid' keys.")
            if not isinstance(player["name"], str) or not isinstance(player["xuid"], str):
                raise UserInputError("Player name and XUID must be strings.")
            if not player["name"] or not player["xuid"]:
                raise UserInputError(
                    "Player name and XUID must be non-empty strings.")

        db_path = settings['paths.player_db']
        try:
            with open(db_path, 'r') as f:
                db = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            db = {}

        changes = 0
        for player in players_data:
            xuid = player["xuid"]
            if xuid not in db or db[xuid] != player:
                db[xuid] = player
                changes += 1

        if changes:
            try:
                with open(db_path, 'w') as f:
                    json.dump(db, f, indent=4)
            except IOError as e:
                raise FileOperationError(f"Failed to save player data: {e}")

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        '''
        db_path = settings['paths.player_db']
        try:
            with open(db_path, 'r') as f:
                db = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        return list(db.values())

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.
        '''
        base_dir = settings['paths.servers']
        if not base_dir or not os.path.exists(base_dir):
            raise AppFileNotFoundError(
                f"Server base directory '{base_dir}' is not configured or does not exist.")

        total_entries_in_logs = 0
        unique_players_submitted_for_saving = 0
        actually_saved_or_updated_in_db = 0
        scan_errors = []

        for server_dir in Path(base_dir).iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir.name, app_context)
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

        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": unique_players_submitted_for_saving,
            "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
            "scan_errors": scan_errors
        }
