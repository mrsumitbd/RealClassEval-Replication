
from typing import List, Dict, Any, Optional
from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from .core.app_context import AppContext
from .core.bedrock_server import BedrockServer


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.
        This utility method is designed to process player data provided as a
        single string, typically from a command-line argument. Each player entry
        in the string should be in the format "PlayerName:PlayerXUID", and multiple
        entries should be separated by commas. Whitespace around names, XUIDs,
        commas, and colons is generally handled.
        Example:
            ``"Player One:12345, PlayerTwo:67890"``
        Args:
            player_string (str): The comma-separated string of player data.
                If empty or not a string, an empty list is returned.
        Raises:
            UserInputError: If any player pair within the string does not conform
                to the "name:xuid" format, or if a name or XUID is empty after stripping.
        '''
        if not isinstance(player_string, str) or not player_string.strip():
            return []

        players_data = []
        for player_pair in player_string.split(','):
            player_pair = player_pair.strip()
            if not player_pair:
                continue

            if ':' not in player_pair:
                raise UserInputError(
                    f'Invalid player format: "{player_pair}". Expected "name:xuid".')

            name, xuid = player_pair.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()

            if not name or not xuid:
                raise UserInputError(
                    f'Empty name or XUID in player pair: "{player_pair}".')

            players_data.append({'name': name, 'xuid': xuid})

        return self.save_player_data(players_data)

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
            raise UserInputError(
                'players_data must be a list of dictionaries.')

        valid_players = []
        for player in players_data:
            if not isinstance(player, dict):
                raise UserInputError('Each player entry must be a dictionary.')

            if 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    'Player dictionary must contain "name" and "xuid" keys.')

            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError('Player name and XUID must be strings.')

            if not player['name'].strip() or not player['xuid'].strip():
                raise UserInputError('Player name and XUID cannot be empty.')

            valid_players.append({
                'name': player['name'].strip(),
                'xuid': player['xuid'].strip()
            })

        existing_players = self.get_known_players()
        existing_xuids = {p['xuid']: p for p in existing_players}

        updated_count = 0
        for player in valid_players:
            xuid = player['xuid']
            if xuid in existing_xuids:
                if existing_xuids[xuid]['name'] != player['name']:
                    existing_xuids[xuid]['name'] = player['name']
                    updated_count += 1
            else:
                existing_xuids[xuid] = player
                updated_count += 1

        if updated_count > 0:
            self._save_player_db(list(existing_xuids.values()))

        return updated_count

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        return self._load_player_db()

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
        result = {
            'total_entries_in_logs': 0,
            'unique_players_submitted_for_saving': 0,
            'actually_saved_or_updated_in_db': 0,
            'scan_errors': []
        }

        servers_path = self.settings.get('paths.servers')
        if not servers_path:
            raise AppFileNotFoundError(
                'Server base directory not configured in settings.')

        if not os.path.isdir(servers_path):
            raise AppFileNotFoundError(
                f'Server base directory does not exist: {servers_path}')

        all_players = []
        for server_name in os.listdir(servers_path):
            server_path = os.path.join(servers_path, server_name)
            if not os.path.isdir(server_path):
                continue

            try:
                server = BedrockServer(server_name, app_context=app_context)
                if not server.is_installed():
                    continue

                players = server.scan_log_for_players()
                all_players.extend(players)
                result['total_entries_in_logs'] += len(players)
            except Exception as e:
                result['scan_errors'].append({
                    'server': server_name,
                    'error': str(e)
                })

        unique_players = {p['xuid']: p for p in all_players}.values()
        result['unique_players_submitted_for_saving'] = len(unique_players)

        try:
            saved_count = self.save_player_data(list(unique_players))
            result['actually_saved_or_updated_in_db'] = saved_count
        except Exception
