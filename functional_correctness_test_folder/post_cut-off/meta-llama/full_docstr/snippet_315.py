
from typing import List, Dict, Optional, Any
import os
from pathlib import Path
from .core.bedrock_server import BedrockServer
from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from .app_context import AppContext


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        if not isinstance(player_string, str) or not player_string.strip():
            return

        players_data = []
        for player_pair in player_string.split(','):
            player_pair = player_pair.strip()
            try:
                name, xuid = player_pair.split(':')
                name, xuid = name.strip(), xuid.strip()
                if not name or not xuid:
                    raise UserInputError(
                        f"Invalid player pair: '{player_pair}'. Name and XUID must be non-empty.")
                players_data.append({"name": name, "xuid": xuid})
            except ValueError:
                raise UserInputError(
                    f"Invalid player pair: '{player_pair}'. Must be in 'name:xuid' format.")

        self.save_player_data(players_data)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        if not isinstance(players_data, list):
            raise UserInputError(
                "players_data must be a list of dictionaries.")

        existing_players = self.get_known_players()
        existing_players_dict = {player["xuid"]                                 : player for player in existing_players}

        updated_count = 0
        for player in players_data:
            if not isinstance(player, dict) or "name" not in player or "xuid" not in player:
                raise UserInputError(
                    "Each player dictionary must contain 'name' and 'xuid' keys.")
            if not isinstance(player["name"], str) or not isinstance(player["xuid"], str):
                raise UserInputError("Both 'name' and 'xuid' must be strings.")
            if not player["name"].strip() or not player["xuid"].strip():
                raise UserInputError(
                    "Both 'name' and 'xuid' must be non-empty.")

            xuid = player["xuid"]
            if xuid in existing_players_dict:
                if existing_players_dict[xuid]["name"] != player["name"]:
                    existing_players_dict[xuid]["name"] = player["name"]
                    updated_count += 1
            else:
                existing_players_dict[xuid] = player
                updated_count += 1

        # Assuming a database or storage mechanism is implemented elsewhere
        # For demonstration, we'll just store it in a hypothetical database
        # self.database["players"] = list(existing_players_dict.values())
        # For the sake of this example, let's assume we're directly updating a database or file
        # In a real application, you'd replace this with your actual database update logic
        # For now, we'll just return the count
        return updated_count

    def get_known_players(self) -> List[Dict[str, str]]:
        # Assuming a database or storage mechanism is implemented elsewhere
        # For demonstration, let's assume we're directly accessing a database or file
        # In a real application, you'd replace this with your actual database retrieval logic
        # For now, we'll just return an empty list
        return []  # Replace with actual database retrieval

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        servers_dir = Path(self.settings['paths.servers'])
        if not servers_dir.exists():
            raise AppFileNotFoundError(
                f"Server base directory '{servers_dir}' does not exist.")

        total_entries_in_logs = 0
        unique_players = {}
        scan_errors = []

        for server_dir in servers_dir.iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir, app_context)
                    if server.is_installed:
                        players = server.scan_log_for_players()
                        total_entries_in_logs += len(players)
                        for player in players:
                            unique_players[player["xuid"]] = player
                except Exception as e:
                    scan_errors.append(
                        {"server": server_dir.name, "error": str(e)})

        unique_players_list = list(unique_players.values())
        try:
            actually_saved_or_updated_in_db = self.save_player_data(
                unique_players_list)
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(
                "Failed to save player data to database.") from e

        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": len(unique_players_list),
            "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
            "scan_errors": scan_errors
        }
