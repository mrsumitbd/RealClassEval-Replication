
import re
from typing import List, Dict, Optional, Any
from workbench.utils.exceptions import UserInputError, AppFileNotFoundError, FileOperationError
from workbench.core.bedrock_server import BedrockServer
from workbench.utils.app_context import AppContext


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
            return
        players_data = []
        for player_pair in re.split(r'\s*,\s*', player_string):
            match = re.match(
                r'\s*(?P<name>[^:]+?)\s*:\s*(?P<xuid>\S+)\s*$', player_pair)
            if not match:
                raise UserInputError(
                    f'Invalid player format: "{player_pair}". Expected "name:xuid".')
            name, xuid = match.group(
                'name').strip(), match.group('xuid').strip()
            if not name or not xuid:
                raise UserInputError(
                    f'Empty name or XUID in player pair: "{player_pair}"')
            players_data.append({'name': name, 'xuid': xuid})
        self.save_player_data(players_data)

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
            raise UserInputError('players_data must be a list of dictionaries')
        count = 0
        known_players = self.get_known_players()
        known_xuids = {player['xuid'] for player in known_players}
        for player in players_data:
            if not isinstance(player, dict) or 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    'Each player must be a dictionary with "name" and "xuid" keys')
            if not isinstance(player['name'], str) or not isinstance(player['xuid'], str):
                raise UserInputError(
                    'Both "name" and "xuid" must be non-empty strings')
            if not player['name'].strip() or not player['xuid'].strip():
                raise UserInputError(
                    'Both "name" and "xuid" must be non-empty strings')
            xuid = player['xuid'].strip()
            name = player['name'].strip()
            if xuid in known_xuids:
                existing_player = next(
                    (p for p in known_players if p['xuid'] == xuid), None)
                if existing_player and (existing_player['name'] != name):
                    # Update existing player
                    existing_player['name'] = name
                    count += 1
            else:
                # Add new player
                known_players.append({'name': name, 'xuid': xuid})
                known_xuids.add(xuid)
                count += 1
        # Save the updated list back to the database
        # Assuming there's a method to save the players list to the database
        # For demonstration, we'll assume it's handled by a fictional method
        # self._save_players_to_db(known_players)
        return count

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        # For demonstration, assume players are stored in a database or a file
        # and this method retrieves them. The actual implementation depends on
        # how the data is stored.
        # For now, returning an empty list as a placeholder.
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
        if app_context is None:
            app_context = AppContext()
        servers_dir = app_context.settings.get('paths.servers')
        if not servers_dir or not app_context.file_system.exists(servers_dir):
            raise AppFileNotFoundError(
                f'Servers directory not found or not configured: {servers_dir}')
        total_entries_in_logs = 0
        players_data = []
        scan_errors = []
        for server_name in app_context.file_system.listdir(servers_dir):
            server_path = app_context.file_system.join(
                servers_dir, server_name)
            if app_context.file_system.isdir(server_path):
                try:
                    server = BedrockServer(server_path, app_context)
                    if server.is_installed:
                        log_players = server.scan_log_for_players()
                        total_entries_in_logs += len(log_players)
                        players_data.extend(log_players)
                except Exception as e:
                    scan_errors.append(
                        {'server': server_name, 'error': str(e)})
        unique_players = {}
        for player in players_data:
            unique_players[player['xuid']] = player
        unique_players_submitted_for_saving = len(unique_players)
        try:
            actually_saved_or_updated_in_db = self.save_player_data(
                list(unique_players.values()))
        except Exception as e:
            scan_errors.append({'server': 'GLOBAL_PLAYER_DB', 'error': str(e)})
            raise FileOperationError(
                'Failed to save player data to database') from e
        return {
            'total_entries_in_logs': total_entries_in_logs,
            'unique_players_submitted_for_saving': unique_players_submitted_for_saving,
            'actually_saved_or_updated_in_db': actually_saved_or_updated_in_db,
            'scan_errors': scan_errors
        }
