from typing import List, Dict, Optional, Any
import os


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.'''
        if not isinstance(player_string, str) or not player_string.strip():
            return []
        players = []
        for entry in player_string.split(','):
            entry = entry.strip()
            if not entry:
                continue
            if ':' not in entry:
                raise UserInputError(
                    f"Player entry '{entry}' does not contain a ':' separator.")
            name, xuid = entry.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                raise UserInputError(
                    f"Player entry '{entry}' must have both a non-empty name and xuid.")
            players.append({'name': name, 'xuid': xuid})
        self.save_player_data(players)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.'''
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list of dicts.")
        for player in players_data:
            if not isinstance(player, dict):
                raise UserInputError("Each player entry must be a dict.")
            if 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    "Each player dict must have 'name' and 'xuid' keys.")
            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError(
                    "Player 'name' and 'xuid' must be strings.")
            if not player['name'].strip() or not player['xuid'].strip():
                raise UserInputError(
                    "Player 'name' and 'xuid' must be non-empty strings.")

        # Load current database
        db_players = self.get_known_players()
        db_by_xuid = {p['xuid']: p for p in db_players}
        changed = 0

        for player in players_data:
            xuid = player['xuid']
            name = player['name']
            if xuid in db_by_xuid:
                if db_by_xuid[xuid]['name'] != name or db_by_xuid[xuid]['xuid'] != xuid:
                    db_by_xuid[xuid]['name'] = name
                    db_by_xuid[xuid]['xuid'] = xuid
                    changed += 1
            else:
                db_by_xuid[xuid] = {'name': name, 'xuid': xuid}
                changed += 1

        # Save back to database
        self._save_player_db(list(db_by_xuid.values()))
        return changed

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.'''
        return self._load_player_db()

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional['AppContext'] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.'''
        from .exceptions import AppFileNotFoundError, FileOperationError, UserInputError
        from .core.bedrock_server import BedrockServer
        from .core.server.player_mixin import ServerPlayerMixin

        settings = self.settings if hasattr(self, 'settings') else {}
        servers_base = settings.get('paths.servers')
        if not servers_base or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                "Server base directory is not configured or does not exist.")

        all_players = []
        scan_errors = []
        total_entries_in_logs = 0
        unique_players = {}

        for server_name in os.listdir(servers_base):
            server_path = os.path.join(servers_base, server_name)
            if not os.path.isdir(server_path):
                continue
            try:
                server = BedrockServer(server_path, app_context=app_context)
                if not getattr(server, 'is_installed', False):
                    continue
                if not hasattr(server, 'scan_log_for_players'):
                    continue
                players = server.scan_log_for_players()
                if not isinstance(players, list):
                    raise Exception(
                        "scan_log_for_players did not return a list")
                total_entries_in_logs += len(players)
                for p in players:
                    xuid = p.get('xuid')
                    name = p.get('name')
                    if not xuid or not name:
                        continue
                    unique_players[xuid] = {'name': name, 'xuid': xuid}
            except Exception as e:
                scan_errors.append({'server': server_name, 'error': str(e)})

        unique_players_list = list(unique_players.values())
        actually_saved = 0
        try:
            actually_saved = self.save_player_data(unique_players_list)
        except Exception as e:
            scan_errors.append({'server': 'GLOBAL_PLAYER_DB', 'error': str(e)})
            raise FileOperationError(f"Failed to save player database: {e}")

        return {
            'total_entries_in_logs': total_entries_in_logs,
            'unique_players_submitted_for_saving': len(unique_players_list),
            'actually_saved_or_updated_in_db': actually_saved,
            'scan_errors': scan_errors
        }

    # --- Internal helpers (assumed to exist in the real class) ---

    def _load_player_db(self) -> List[Dict[str, str]]:
        '''Load the player database from storage.'''
        # Placeholder: In real code, this would load from a file or database.
        if not hasattr(self, '_player_db'):
            self._player_db = []
        return list(self._player_db)

    def _save_player_db(self, players: List[Dict[str, str]]) -> None:
        '''Save the player database to storage.'''
        # Placeholder: In real code, this would save to a file or database.
        self._player_db = list(players)

# --- Exceptions assumed to exist elsewhere ---


class UserInputError(Exception):
    pass


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass
