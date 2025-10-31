from typing import Any, Dict, List, Optional, TYPE_CHECKING
import os
import json

if TYPE_CHECKING:
    from .app_context import AppContext  # type: ignore[unused-ignore]

try:
    # type: ignore[unused-ignore]
    from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError
except Exception:  # Fallbacks if project-specific exceptions are unavailable
    class UserInputError(ValueError):
        pass

    class AppFileNotFoundError(FileNotFoundError):
        pass

    class FileOperationError(IOError):
        pass


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

        entries = [seg.strip() for seg in player_string.split(',')]
        players: List[Dict[str, str]] = []
        for idx, entry in enumerate(entries, start=1):
            if not entry:
                # Ignore empty segments created by extra commas
                continue
            if ':' not in entry:
                raise UserInputError(
                    f'Player #{idx} "{entry}" is missing a ":" separator.')
            name, xuid = entry.split(':', 1)
            name = name.strip()
            xuid = xuid.strip()
            if not name:
                raise UserInputError(f'Player #{idx} has an empty name.')
            if not xuid:
                raise UserInputError(f'Player #{idx} has an empty XUID.')
            players.append({'name': name, 'xuid': xuid})

        if players:
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
            raise UserInputError(
                'players_data must be a list of {"name": str, "xuid": str} dictionaries.')

        normalized: List[Dict[str, str]] = []
        for i, item in enumerate(players_data, start=1):
            if not isinstance(item, dict):
                raise UserInputError(f'players_data item #{i} is not a dict.')
            if 'name' not in item or 'xuid' not in item:
                raise UserInputError(
                    f'players_data item #{i} must contain "name" and "xuid" keys.')
            name, xuid = item['name'], item['xuid']
            if not isinstance(name, str) or not isinstance(xuid, str):
                raise UserInputError(
                    f'players_data item #{i} "name" and "xuid" must be strings.')
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                raise UserInputError(
                    f'players_data item #{i} has empty "name" or "xuid".')
            normalized.append({'name': name, 'xuid': xuid})

        existing = self.get_known_players()
        by_xuid: Dict[str, Dict[str, str]] = {p['xuid']: dict(
            p) for p in existing if 'xuid' in p and isinstance(p.get('xuid'), str)}

        changes = 0
        for new in normalized:
            xuid = new['xuid']
            name = new['name']
            if xuid in by_xuid:
                if by_xuid[xuid].get('name') != name:
                    by_xuid[xuid]['name'] = name
                    changes += 1
            else:
                by_xuid[xuid] = {'name': name, 'xuid': xuid}
                changes += 1

        if changes == 0:
            return 0

        merged_list = list(by_xuid.values())
        try:
            self._write_known_players(merged_list)
        except Exception as exc:
            raise FileOperationError(
                f'Failed to save player database: {exc}') from exc

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        # In-memory cache takes precedence if present.
        cache = getattr(self, '_players_db_cache', None)
        if isinstance(cache, list):
            return [dict(p) for p in cache if isinstance(p, dict)]

        path = self._players_db_path()
        players: List[Dict[str, str]] = []

        if path and os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name')
                            xuid = item.get('xuid')
                            if isinstance(name, str) and isinstance(xuid, str) and name.strip() and xuid.strip():
                                players.append(
                                    {'name': name.strip(), 'xuid': xuid.strip()})
            except Exception:
                # On read/parse failure, fall back to empty list.
                players = []

        setattr(self, '_players_db_cache', [dict(p) for p in players])
        return [dict(p) for p in players]

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
        servers_root = self._servers_base_path()
        if not servers_root or not os.path.isdir(servers_root):
            raise AppFileNotFoundError(
                'Server base directory (settings["paths.servers"]) is not configured or does not exist.')

        scan_errors: List[Dict[str, str]] = []
        aggregated: List[Dict[str, str]] = []

        try:
            subdirs = [d for d in os.listdir(servers_root)]
        except Exception as exc:
            raise AppFileNotFoundError(
                f'Unable to list server directories: {exc}') from exc

        for entry in sorted(subdirs):
            server_dir = os.path.join(servers_root, entry)
            if not os.path.isdir(server_dir):
                continue

            server_name = entry
            try:
                players_from_server = self._scan_single_server_for_players(
                    server_dir, app_context)
                # Validate and normalize
                for i, p in enumerate(players_from_server, start=1):
                    if not isinstance(p, dict):
                        raise UserInputError(
                            f'server "{server_name}" returned non-dict player at index {i}.')
                    name = p.get('name')
                    xuid = p.get('xuid')
                    if not isinstance(name, str) or not isinstance(xuid, str) or not name.strip() or not xuid.strip():
                        raise UserInputError(
                            f'server "{server_name}" returned invalid player at index {i}.')
                    aggregated.append(
                        {'name': name.strip(), 'xuid': xuid.strip()})
            except Exception as exc:
                scan_errors.append({'server': server_name, 'error': str(exc)})

        total_entries_in_logs = len(aggregated)

        # Deduplicate by XUID
        unique_by_xuid: Dict[str, Dict[str, str]] = {}
        for p in aggregated:
            unique_by_xuid[p['xuid']] = p
        unique_list = list(unique_by_xuid.values())

        actually_saved = 0
        try:
            if unique_list:
                actually_saved = self.save_player_data(unique_list)
        except Exception as exc:
            scan_errors.append(
                {'server': 'GLOBAL_PLAYER_DB', 'error': str(exc)})
            raise FileOperationError(
                f'Failed to save global player database: {exc}') from exc

        return {
            'total_entries_in_logs': total_entries_in_logs,
            'unique_players_submitted_for_saving': len(unique_list),
            'actually_saved_or_updated_in_db': actually_saved,
            'scan_errors': scan_errors,
        }

    # Internal helpers

    def _players_db_path(self) -> Optional[str]:
        # Try dotted key then nested dict
        settings = getattr(self, 'settings', {}) or {}
        path = None
        if isinstance(settings, dict):
            if 'paths.players_db' in settings and isinstance(settings['paths.players_db'], str):
                path = settings['paths.players_db']
            elif 'paths' in settings and isinstance(settings['paths'], dict):
                paths = settings['paths']
                if 'players_db' in paths and isinstance(paths['players_db'], str):
                    path = paths['players_db']
        if not path:
            servers_root = self._servers_base_path()
            if servers_root:
                path = os.path.join(servers_root, '.players.json')
        return path

    def _servers_base_path(self) -> Optional[str]:
        settings = getattr(self, 'settings', {}) or {}
        if not isinstance(settings, dict):
            return None
        if 'paths.servers' in settings and isinstance(settings['paths.servers'], str):
            return settings['paths.servers']
        paths = settings.get('paths')
        if isinstance(paths, dict) and isinstance(paths.get('servers'), str):
            return paths.get('servers')
        return None

    def _write_known_players(self, players: List[Dict[str, str]]) -> None:
        setattr(self, '_players_db_cache', [dict(p) for p in players])

        path = self._players_db_path()
        if not path:
            # No persistent path configured; in-memory only.
            return

        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = f'{path}.tmp'
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(players, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)

    def _scan_single_server_for_players(self, server_dir: str, app_context: Optional['AppContext']) -> List[Dict[str, str]]:
        # Prefer a server instance if the manager provides a factory/hook.
        server = None
        # Common hook names to obtain a server instance for a directory.
        for attr in ('get_server_instance', 'create_server_instance', 'server_factory'):
            factory = getattr(self, attr, None)
            if callable(factory):
                try:
                    # type: ignore[misc]
                    server = factory(server_dir, app_context)
                    break
                except Exception:
                    server = None

        # If we have a server object with scan capability, use it.
        if server is not None:
            scan_method = getattr(server, 'scan_log_for_players', None)
            if callable(scan_method):
                result = scan_method()
                if result is None:
                    return []
                if isinstance(result, list):
                    return result
                raise UserInputError(
                    'scan_log_for_players did not return a list.')

        # If the manager itself has a scanning hook, use it.
        manager_scan = getattr(self, 'scan_log_for_players', None)
        if callable(manager_scan):
            result = manager_scan(server_dir)  # type: ignore[misc]
            if result is None:
                return []
            if isinstance(result, list):
                return result
            raise UserInputError('scan_log_for_players did not return a list.')

        # No available scanner; return empty and let caller record an error.
        raise RuntimeError(
            'No available scanner to extract players from logs for this server.')
