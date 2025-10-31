
from typing import List, Dict, Any, Optional
from pathlib import Path
from .core.bedrock_server import BedrockServer
from .core.server.player_mixin import ServerPlayerMixin
from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.'''
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players_data = []
        player_pairs = [pair.strip() for pair in player_string.split(',')]

        for pair in player_pairs:
            if ':' not in pair:
                raise UserInputError(
                    f"Invalid player pair format: {pair}. Expected 'name:xuid'.")

            name, xuid = [item.strip() for item in pair.split(':', 1)]
            if not name or not xuid:
                raise UserInputError(f"Empty name or XUID in pair: {pair}.")

            players_data.append({"name": name, "xuid": xuid})

        return self.save_player_data(players_data)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.'''
        if not isinstance(players_data, list):
            raise UserInputError(
                "players_data must be a list of dictionaries.")

        for player in players_data:
            if not isinstance(player, dict) or "name" not in player or "xuid" not in player:
                raise UserInputError(
                    "Each player dictionary must contain 'name' and 'xuid' keys.")
            if not isinstance(player["name"], str) or not isinstance(player["xuid"], str):
                raise UserInputError("Player name and XUID must be strings.")
            if not player["name"].strip() or not player["xuid"].strip():
                raise UserInputError("Player name and XUID must not be empty.")

        existing_players = self.get_known_players()
        existing_xuids = {player["xuid"]                          : player for player in existing_players}

        changes = 0
        for player in players_data:
            if player["xuid"] in existing_xuids:
                existing_player = existing_xuids[player["xuid"]]
                if existing_player["name"] != player["name"]:
                    existing_player["name"] = player["name"]
                    changes += 1
            else:
                existing_players.append(player)
                changes += 1

        if changes > 0:
            self._save_players_to_db(existing_players)

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.'''
        return self._load_players_from_db()

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.'''
        servers_base_path = Path(app_context.settings['paths.servers'])
        if not servers_base_path.exists():
            raise AppFileNotFoundError(
                f"Server base directory not found: {servers_base_path}")

        result = {
            "total_entries_in_logs": 0,
            "unique_players_submitted_for_saving": 0,
            "actually_saved_or_updated_in_db": 0,
            "scan_errors": []
        }

        all_players = []
        for server_dir in servers_base_path.iterdir():
            if server_dir.is_dir():
                try:
                    server = BedrockServer(server_dir, app_context)
                    if server.is_installed:
                        players = server.scan_log_for_players()
                        all_players.extend(players)
                        result["total_entries_in_logs"] += len(players)
                except Exception as e:
                    result["scan_errors"].append({
                        "server": server_dir.name,
                        "error": str(e)
                    })

        unique_players = {player["xuid"]                          : player for player in all_players}.values()
        result["unique_players_submitted_for_saving"] = len(unique_players)

        try:
            result["actually_saved_or_updated_in_db"] = self.save_player_data(
                list(unique_players))
        except Exception as e:
            raise FileOperationError(
                f"Failed to save player data to database: {e}")

        return result

    def _load_players_from_db(self) -> List[Dict[str, str]]:
        '''Loads player data from the database.'''
        # Implementation depends on the actual database used
        pass

    def _save_players_to_db(self, players_data: List[Dict[str, str]]) -> None:
        '''Saves player data to the database.'''
        # Implementation depends on the actual database used
        pass
