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
        for pair in player_string.split(','):
            pair = pair.strip()
            if not pair:
                continue
            if ':' not in pair:
                raise UserInputError(
                    f"Player entry '{pair}' is not in 'name:xuid' format.")
            name, xuid = pair.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                raise UserInputError(
                    f"Player entry '{pair}' must have non-empty name and xuid.")
            players.append({'name': name, 'xuid': xuid})
        self.save_player_data(players)

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.'''
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list of dicts.")
        for entry in players_data:
            if not isinstance(entry, dict):
                raise UserInputError("Each player entry must be a dict.")
            if 'name' not in entry or 'xuid' not in entry:
                raise UserInputError(
                    "Each player dict must have 'name' and 'xuid' keys.")
            if not isinstance(entry['name'], str) or not isinstance(entry['xuid'], str):
                raise UserInputError(
                    "Player 'name' and 'xuid' must be strings.")
            if not entry['name'].strip() or not entry['xuid'].strip():
                raise UserInputError(
                    "Player 'name' and 'xuid' must be non-empty strings.")

        # Load current DB
        db = self._load_player_db()
        changed = 0
        for entry in players_data:
            xuid = entry['xuid']
            name = entry['name']
            if xuid in db:
                if db[xuid]['name'] != name or db[xuid]['xuid'] != xuid:
                    db[xuid] = {'name': name, 'xuid': xuid}
                    changed += 1
            else:
                db[xuid] = {'name': name, 'xuid': xuid}
                changed += 1
        if changed:
            self._save_player_db(db)
        return changed

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.'''
        db = self._load_player_db()
        return list(db.values())

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional['AppContext'] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.'''
        from .exceptions import AppFileNotFoundError, FileOperationError, UserInputError
        from .core.bedrock_server import BedrockServer
        from .core.server.player_mixin import ServerPlayerMixin

        settings = self.settings if hasattr(self, 'settings') else None
        if not settings or 'paths.servers' not in settings or not settings['paths.servers']:
            raise AppFileNotFoundError(
                "Server base directory is not configured.")
        base_dir = settings['paths.servers']
        if not os.path.isdir(base_dir):
            raise AppFileNotFoundError(
                f"Server base directory '{base_dir}' does not exist.")

        all_players = []
        scan_errors = []
        for server_name in os.listdir(base_dir):
            server_path = os.path.join(base_dir, server_name)
            if not os.path.isdir(server_path):
                continue
            try:
                server = BedrockServer(server_path, app_context=app_context)
                if not getattr(server, 'is_installed', False):
                    continue
                if not hasattr(server, 'scan_log_for_players'):
                    continue
                players = server.scan_log_for_players()
                if players:
                    all_players.extend(players)
            except Exception as e:
                scan_errors.append({'server': server_name, 'error': str(e)})

        total_entries_in_logs = len(all_players)
        # Deduplicate by XUID
        unique_players = {}
        for entry in all_players:
            if not isinstance(entry, dict):
                continue
            xuid = entry.get('xuid')
            name = entry.get('name')
            if not xuid or not name:
                continue
            unique_players[xuid] = {'name': name, 'xuid': xuid}
        unique_players_list = list(unique_players.values())
        unique_players_submitted_for_saving = len(unique_players_list)
        try:
            actually_saved_or_updated_in_db = self.save_player_data(
                unique_players_list)
        except Exception as e:
            scan_errors.append({'server': 'GLOBAL_PLAYER_DB', 'error': str(e)})
            raise FileOperationError(f"Failed to save player data: {e}")
        return {
            'total_entries_in_logs': total_entries_in_logs,
            'unique_players_submitted_for_saving': unique_players_submitted_for_saving,
            'actually_saved_or_updated_in_db': actually_saved_or_updated_in_db,
            'scan_errors': scan_errors
        }

    # --- Internal helpers (assumed to exist or to be implemented) ---

    def _load_player_db(self) -> Dict[str, Dict[str, str]]:
        '''Loads the player database from storage.'''
        # This is a placeholder. In real code, this would load from a file or DB.
        if not hasattr(self, '_player_db'):
            self._player_db = {}
        return self._player_db

    def _save_player_db(self, db: Dict[str, Dict[str, str]]) -> None:
        '''Saves the player database to storage.'''
        # This is a placeholder. In real code, this would save to a file or DB.
        self._player_db = db

# Exception classes assumed to exist elsewhere:


class UserInputError(Exception):
    pass


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass
