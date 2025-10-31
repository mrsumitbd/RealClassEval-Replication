
from typing import Any, Dict, List, Optional
from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from .core.bedrock_server import BedrockServer
from .core.context import AppContext


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.'''
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players = []
        for player_pair in player_string.split(','):
            player_pair = player_pair.strip()
            if not player_pair:
                continue

            if ':' not in player_pair:
                raise UserInputError(
                    f'Player pair "{player_pair}" does not contain a colon separator')

            name, xuid = player_pair.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()

            if not name:
                raise UserInputError(
                    f'Player name cannot be empty in pair "{player_pair}"')
            if not xuid:
                raise UserInputError(
                    f'XUID cannot be empty in pair "{player_pair}"')

            players.append({'name': name, 'xuid': xuid})

        return players

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        '''Saves or updates player data in the database.'''
        if not isinstance(players_data, list):
            raise UserInputError('players_data must be a list')

        current_players = self.get_known_players()
        current_xuids = {p['xuid']: p for p in current_players}
        changes = 0

        for player in players_data:
            if not isinstance(player, dict):
                raise UserInputError('Each player entry must be a dictionary')
            if 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    'Each player dictionary must contain "name" and "xuid" keys')
            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError('Player name and XUID must be strings')
            if not player['name'].strip() or not player['xuid'].strip():
                raise UserInputError('Player name and XUID cannot be empty')

            xuid = player['xuid']
            if xuid in current_xuids:
                if current_xuids[xuid]['name'] != player['name']:
                    current_xuids[xuid]['name'] = player['name']
                    changes += 1
            else:
                current_xuids[xuid] = player
                changes += 1

        if changes > 0:
            try:
                self._save_player_db(list(current_xuids.values()))
            except Exception as e:
                raise FileOperationError(
                    f'Failed to save player database: {str(e)}')

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.'''
        try:
            return self._load_player_db()
        except Exception:
            return []

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        '''Scans all server logs for player data and updates the central player database.'''
        result = {
            'total_entries_in_logs': 0,
            'unique_players_submitted_for_saving': 0,
            'actually_saved_or_updated_in_db': 0,
            'scan_errors': []
        }

        servers_dir = self._get_servers_base_dir()
        if not servers_dir.exists():
            raise AppFileNotFoundError(
                f'Servers directory not found: {servers_dir}')

        all_players = {}

        for server_dir in servers_dir.iterdir():
            if not server_dir.is_dir():
                continue

            try:
                server = BedrockServer(server_dir.name, app_context)
                if not server.is_installed():
                    continue

                players = server.scan_log_for_players()
                result['total_entries_in_logs'] += len(players)

                for player in players:
                    all_players[player['xuid']] = player

            except Exception as e:
                result['scan_errors'].append({
                    'server': server_dir.name,
                    'error': str(e)
                })

        result['unique_players_submitted_for_saving'] = len(all_players)

        try:
            changes = self.save_player_data(list(all_players.values()))
            result['actually_saved_or_updated_in_db'] = changes
        except Exception as e:
            result['scan_errors'].append({
                'server': 'GLOBAL_PLAYER_DB',
                'error': str(e)
            })
            raise FileOperationError(
                f'Failed to save player database: {str(e)}')

        return result
