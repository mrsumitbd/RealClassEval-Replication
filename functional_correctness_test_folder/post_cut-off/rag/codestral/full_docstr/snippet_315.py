
from typing import List, Dict, Any, Optional
from app.core.errors import UserInputError, AppFileNotFoundError, FileOperationError
from app.core.context import AppContext
from app.core.bedrock_server import BedrockServer
import os


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
        player_pairs = [pair.strip() for pair in player_string.split(',')]

        for pair in player_pairs:
            if ':' not in pair:
                raise UserInputError(
                    f"Invalid player format: '{pair}'. Expected 'name:xuid'.")

            name, xuid = pair.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()

            if not name or not xuid:
                raise UserInputError(f"Empty name or XUID in pair: '{pair}'.")

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
                "players_data must be a list of dictionaries.")

        changes = 0
        existing_players = {
            player['xuid']: player for player in self.get_known_players()}

        for player in players_data:
            if not isinstance(player, dict) or 'name' not in player or 'xuid' not in player:
                raise UserInputError(
                    "Each player must be a dictionary with 'name' and 'xuid' keys.")

            name = player['name']
            xuid = player['xuid']

            if not isinstance(name, str) or not isinstance(xuid, str) or not name.strip() or not xuid.strip():
                raise UserInputError(
                    "Player name and XUID must be non-empty strings.")

            if xuid in existing_players:
                if existing_players[xuid]['name'] != name:
                    existing_players[xuid]['name'] = name
                    changes += 1
            else:
                existing_players[xuid] = {'name': name, 'xuid': xuid}
                changes += 1

        # Save the updated player data to the database
        self._save_players_to_database(list(existing_players.values()))
        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        # Implementation depends on the actual database storage mechanism
        # This is a placeholder for the actual implementation
        return self._load_players_from_database()

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
            app_context = self.app_context

        servers_base_dir = app_context.settings.get('paths.servers')
        if not servers_base_dir or not os.path.isdir(servers_base_dir):
            raise AppFileNotFoundError(
                f"Servers base directory not found: {servers_base_dir}")

        scan_results = {
            'total_entries_in_logs': 0,
            'unique_players_submitted_for_saving': 0,
            'actually_saved_or_updated_in_db': 0,
            'scan_errors': []
        }

        all_players = []

        for server_name in os.listdir(servers_base_dir):
            server_dir = os.path.join(servers_base_dir, server_name)
            if not os.path.isdir(server_dir):
                continue

            try:
                server = BedrockServer(server_name, app_context)
                if not server.is_installed():
                    continue

                players = server.scan_log_for_players()
                scan_results['total_entries_in_logs'] += len(players)
                all_players.extend(players)

            except Exception as e:
                scan_results['scan_errors'].append({
                    'server': server_name,
                    'error': str(e)
                })

        # Remove duplicates based on XUID
        unique_players = {}
        for player in all_players:
            if player['xuid'] not in unique_players:
                unique_players[player['xuid']] = player

        unique_players_list = list(unique_players.values())
        scan_results['unique_players_submitted_for_saving'] = len(
            unique_players_list)

        try:
            scan_results['actually_saved_or_updated_in_db'] = self.save_player_data(
                unique_players_list)
        except Exception as e:
            scan_results['scan_errors'].append({
                'server': 'GLOBAL_PLAYER_DB',
                'error': str(e)
            })
            raise FileOperationError(
                f"Failed to save player data to database: {str(e)}")

        return scan_results
