
from typing import List, Dict, Any, Optional
import os
import re
from collections import defaultdict


class UserInputError(Exception):
    pass


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class AppContext:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings


class BedrockServer:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.is_valid = os.path.exists(server_path)
        self.is_installed = os.path.exists(
            os.path.join(server_path, 'server.properties'))

    def scan_log_for_players(self) -> List[Dict[str, str]]:
        log_file_path = os.path.join(self.server_path, 'server.log')
        players = []
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                for line in log_file:
                    match = re.search(r'Player (\w+): (\d+)', line)
                    if match:
                        players.append(
                            {'name': match.group(1), 'xuid': match.group(2)})
        return players


class PlayerMixin:
    def __init__(self):
        self.player_db = {}

    def parse_player_cli_argument(self, player_string: str) -> None:
        if not isinstance(player_string, str) or not player_string.strip():
            raise UserInputError("Player string is empty or not a string.")

        player_pairs = player_string.split(',')
        players_data = []
        for pair in player_pairs:
            parts = pair.split(':')
            if len(parts) != 2:
                raise UserInputError(
                    f"Invalid player pair format: {pair.strip()}")
            name, xuid = map(str.strip, parts)
            if not name or not xuid:
                raise UserInputError(
                    f"Name or XUID is empty in pair: {pair.strip()}")
            players_data.append({'name': name, 'xuid': xuid})

        self.save_player_data(players_data)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        if not isinstance(players_data, list):
            raise UserInputError("Players data is not a list.")

        changes = 0
        for player in players_data:
            if not isinstance(player, dict) or 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    "Player data dictionary is missing 'name' or 'xuid'.")
            name, xuid = player['name'], player['xuid']
            if not isinstance(name, str) or not isinstance(xuid, str) or not name or not xuid:
                raise UserInputError("Name or XUID is not a non-empty string.")

            if xuid in self.player_db:
                if self.player_db[xuid] != name:
                    self.player_db[xuid] = name
                    changes += 1
            else:
                self.player_db[xuid] = name
                changes += 1

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        return [{'name': name, 'xuid': xuid} for xuid, name in self.player_db.items()]

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        if app_context is None or 'paths' not in app_context.settings or 'servers' not in app_context.settings['paths']:
            raise AppFileNotFoundError(
                "Main server base directory is not configured or does not exist.")

        server_base_dir = app_context.settings['paths']['servers']
        if not os.path.exists(server_base_dir):
            raise AppFileNotFoundError(
                f"Server base directory does not exist: {server_base_dir}")

        total_entries_in_logs = 0
        unique_players_submitted_for_saving = 0
        actually_saved_or_updated_in_db = 0
        scan_errors = []

        all_players = defaultdict(set)
        for server_name in os.listdir(server_base_dir):
            server_path = os.path.join(server_base_dir, server_name)
            try:
                server = BedrockServer(server_path)
                if server.is_valid and server.is_installed:
                    players = server.scan_log_for_players()
                    total_entries_in_logs += len(players)
                    for player in players:
                        all_players[player['xuid']].add(player['name'])
            except Exception as e:
                scan_errors.append({"server": server_name, "error": str(e)})

        players_data = [{'name': next(iter(names)), 'xuid': xuid}
                        for xuid, names in all_players.items()]
        unique_players_submitted_for_saving = len(players_data)

        try:
            actually_saved_or_updated_in_db = self.save_player_data(
                players_data)
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})

        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": unique_players_submitted_for_saving,
            "actually_saved_or_updated_in_db": actually_saved_or_updated_in_db,
            "scan_errors": scan_errors
        }
