class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
        '''

    def _get_setting(self, key_path, default=None):
        settings = getattr(self, 'settings', None)
        if not isinstance(settings, dict):
            return default
        if key_path in settings:
            return settings.get(key_path, default)
        curr = settings
        for part in str(key_path).split('.'):
            if isinstance(curr, dict) and part in curr:
                curr = curr[part]
            else:
                return default
        return curr

    def _ensure_player_db(self):
        if not hasattr(self, '_player_db'):
            # store as dict keyed by xuid -> name
            self._player_db = {}

    def _raise_user_input_error(self, msg):
        exc = globals().get('UserInputError', ValueError)
        raise exc(msg)

    def _raise_app_file_not_found(self, msg):
        exc = globals().get('AppFileNotFoundError', FileNotFoundError)
        raise exc(msg)

    def _raise_file_operation_error(self, msg):
        exc = globals().get('FileOperationError', OSError)
        raise exc(msg)

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
        entries = [s for s in (seg.strip()
                               for seg in player_string.split(',')) if s]
        players = []
        for entry in entries:
            if ':' not in entry:
                self._raise_user_input_error(
                    f"Invalid player entry (missing ':'): {entry}")
            name, xuid = entry.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                self._raise_user_input_error(
                    f"Invalid player entry (empty name or xuid): {entry}")
            players.append({'name': name, 'xuid': xuid})
        self.save_player_data(players)

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
            self._raise_user_input_error(
                "players_data must be a list of {'name': str, 'xuid': str} dicts")
        normalized = []
        for idx, item in enumerate(players_data):
            if not isinstance(item, dict):
                self._raise_user_input_error(
                    f"players_data[{idx}] is not a dict")
            if 'name' not in item or 'xuid' not in item:
                self._raise_user_input_error(
                    f"players_data[{idx}] missing 'name' or 'xuid'")
            name = item['name']
            xuid = item['xuid']
            if not isinstance(name, str) or not isinstance(xuid, str):
                self._raise_user_input_error(
                    f"players_data[{idx}] 'name' and 'xuid' must be strings")
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                self._raise_user_input_error(
                    f"players_data[{idx}] 'name' and 'xuid' cannot be empty")
            normalized.append({'name': name, 'xuid': xuid})

        self._ensure_player_db()
        changed = 0
        for p in normalized:
            xuid = p['xuid']
            name = p['name']
            if xuid not in self._player_db:
                self._player_db[xuid] = name
                changed += 1
            else:
                if self._player_db[xuid] != name:
                    self._player_db[xuid] = name
                    changed += 1
        return changed

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        self._ensure_player_db()
        return [{'name': name, 'xuid': xuid} for xuid, name in self._player_db.items()]

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional['AppContext'] = None) -> Dict[str, Any]:
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
        import os

        base_dir = self._get_setting('paths.servers')
        if not base_dir or not isinstance(base_dir, str):
            self._raise_app_file_not_found(
                "Base server directory not configured at settings['paths.servers']")
        if not os.path.isdir(base_dir):
            self._raise_app_file_not_found(
                f"Base server directory does not exist: {base_dir}")

        total_entries = 0
        players_by_xuid = {}
        scan_errors = []

        # Attempt to locate a BedrockServer factory if available
        bedrock_cls = globals().get('BedrockServer', None)

        # Optionally a factory method on self
        server_factory = None
        for attr in ('get_server_instance', 'create_server_from_path', 'server_from_path'):
            if hasattr(self, attr) and callable(getattr(self, attr)):
                server_factory = getattr(self, attr)
                break

        try:
            subdirs = [d for d in os.listdir(base_dir)]
        except Exception as e:
            self._raise_app_file_not_found(
                f"Unable to list server base directory '{base_dir}': {e}")

        for entry in subdirs:
            server_path = os.path.join(base_dir, entry)
            if not os.path.isdir(server_path):
                continue

            try:
                server_obj = None
                if server_factory:
                    server_obj = server_factory(server_path)
                elif bedrock_cls is not None:
                    try:
                        server_obj = bedrock_cls(server_path)
                    except Exception as _:
                        server_obj = None

                if server_obj is None:
                    raise RuntimeError("Unable to construct server instance")

                is_installed = getattr(server_obj, 'is_installed', None)
                if callable(is_installed):
                    installed = bool(is_installed())
                else:
                    installed = bool(
                        is_installed) if is_installed is not None else True

                if not installed:
                    continue

                scan_func = getattr(server_obj, 'scan_log_for_players', None)
                if not callable(scan_func):
                    raise RuntimeError(
                        "Server object has no scan_log_for_players method")

                found = scan_func()
                if not isinstance(found, list):
                    raise RuntimeError(
                        "scan_log_for_players did not return a list")

                total_entries += len(found)
                for item in found:
                    if not isinstance(item, dict):
                        continue
                    name = str(item.get('name', '')).strip()
                    xuid = str(item.get('xuid', '')).strip()
                    if not name or not xuid:
                        continue
                    # prefer keeping the first seen name; update if not set
                    if xuid not in players_by_xuid or not players_by_xuid[xuid]:
                        players_by_xuid[xuid] = name
            except Exception as e:
                scan_errors.append({'server': entry, 'error': str(e)})

        unique_players = [{'name': name, 'xuid': xuid}
                          for xuid, name in players_by_xuid.items()]

        saved_count = 0
        try:
            if unique_players:
                saved_count = self.save_player_data(unique_players)
            else:
                saved_count = 0
        except Exception as e:
            scan_errors.append({'server': 'GLOBAL_PLAYER_DB', 'error': str(e)})
            self._raise_file_operation_error(
                f"Failed saving discovered players to database: {e}")

        return {
            'total_entries_in_logs': total_entries,
            'unique_players_submitted_for_saving': len(unique_players),
            'actually_saved_or_updated_in_db': int(saved_count),
            'scan_errors': scan_errors,
        }
