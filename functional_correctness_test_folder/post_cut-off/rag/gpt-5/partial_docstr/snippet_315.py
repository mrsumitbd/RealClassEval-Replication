from typing import List, Dict, Any, Optional
import os

# Fallback exception definitions if the host app does not provide them.
try:
    from .errors import UserInputError, AppFileNotFoundError, FileOperationError  # type: ignore
except Exception:  # pragma: no cover - fallback for standalone use
    class UserInputError(ValueError):
        pass

    class AppFileNotFoundError(FileNotFoundError):
        pass

    class FileOperationError(RuntimeError):
        pass


# Fallback AppContext if not available from the host app.
try:
    from .core.app_context import AppContext  # type: ignore
except Exception:  # pragma: no cover - fallback stub
    class AppContext:
        def __init__(self, settings: Optional[Dict[str, Any]] = None):
            self.settings = settings or {}


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
        '''

    def _ensure_player_store(self) -> Dict[str, str]:
        # Internal helper: ensures an in-memory player store exists.
        # The store maps xuid -> name.
        if not hasattr(self, '_player_store') or not isinstance(getattr(self, '_player_store'), dict):
            setattr(self, '_player_store', {})
        return getattr(self, '_player_store')

    def _coerce_settings(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        # Internal helper to obtain settings dict from provided or attached context.
        if app_context and hasattr(app_context, 'settings'):
            return app_context.settings or {}
        if hasattr(self, 'app_context') and getattr(self, 'app_context') is not None and hasattr(self.app_context, 'settings'):
            return self.app_context.settings or {}
        if hasattr(self, 'settings'):
            return getattr(self, 'settings') or {}
        return {}

    def parse_player_cli_argument(self, player_string: str) -> None:
        '''Parses a comma-separated string of 'player_name:xuid' pairs and saves them to the database.
        This utility method is designed to process player data provided as a
        single string, typically from a command-line argument. Each player entry
        in the string should be in the format "PlayerName:PlayerXUID", and multiple
        entries should be separated by commas. Whitespace around names, XUIDs,
        commas, and colons is generally handled.
        Example:
            "Player One:12345, PlayerTwo:67890"
        Args:
            player_string (str): The comma-separated string of player data.
                If empty or not a string, an empty list is returned.
        Raises:
            UserInputError: If any player pair within the string does not conform
                to the "name:xuid" format, or if a name or XUID is empty after stripping.
        '''
        if not isinstance(player_string, str) or not player_string.strip():
            return

        entries = [e.strip() for e in player_string.split(',') if e.strip()]
        players: List[Dict[str, str]] = []

        for entry in entries:
            if ':' not in entry:
                raise UserInputError(
                    f'Player entry "{entry}" is not in "name:xuid" format.')
            name_part, xuid_part = entry.split(':', 1)
            name = name_part.strip().strip('"').strip("'")
            xuid = xuid_part.strip().strip('"').strip("'")
            if not name or not xuid:
                raise UserInputError(
                    f'Player entry "{entry}" must have non-empty name and xuid.')
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
            raise UserInputError(
                'players_data must be a list of {"name": str, "xuid": str} dicts.')

        # Validate input and normalize whitespace.
        normalized: List[Dict[str, str]] = []
        for idx, item in enumerate(players_data):
            if not isinstance(item, dict):
                raise UserInputError(f'Item at index {idx} is not a dict.')
            if 'name' not in item or 'xuid' not in item:
                raise UserInputError(
                    f'Item at index {idx} must contain "name" and "xuid" keys.')
            name = item['name']
            xuid = item['xuid']
            if not isinstance(name, str) or not isinstance(xuid, str):
                raise UserInputError(
                    f'Item at index {idx} must have string "name" and "xuid" values.')
            name = name.strip()
            xuid = xuid.strip()
            if not name or not xuid:
                raise UserInputError(
                    f'Item at index {idx} must have non-empty "name" and "xuid".')
            normalized.append({'name': name, 'xuid': xuid})

        store = self._ensure_player_store()
        changes = 0

        for entry in normalized:
            name = entry['name']
            xuid = entry['xuid']
            if xuid not in store:
                store[xuid] = name
                changes += 1
            else:
                if store[xuid] != name:
                    store[xuid] = name
                    changes += 1

        # Persist in-memory; host application can override with durable storage if desired.
        setattr(self, '_player_store', store)
        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains "name" and "xuid" keys.
        '''
        store = self._ensure_player_store()
        return [{'name': name, 'xuid': xuid} for xuid, name in store.items()]

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
                - "total_entries_in_logs" (int)
                - "unique_players_submitted_for_saving" (int)
                - "actually_saved_or_updated_in_db" (int)
                - "scan_errors" (List[Dict[str, str]])
        Raises:
            AppFileNotFoundError: If the main server base directory is not configured or missing.
            FileOperationError: If saving the aggregated players to the database fails.
        '''
        settings = self._coerce_settings(app_context)
        base_servers_path = (
            settings.get('paths.servers')
            if isinstance(settings.get('paths.servers', None), (str, os.PathLike))
            else settings.get('paths', {}).get('servers') if isinstance(settings.get('paths', {}), dict) else None
        )

        if not base_servers_path or not isinstance(base_servers_path, str) or not os.path.isdir(base_servers_path):
            raise AppFileNotFoundError(
                'Base servers directory (settings["paths.servers"]) not configured or does not exist.')

        try:
            # Try importing BedrockServer dynamically; proceed best-effort if unavailable.
            BedrockServer = None  # type: ignore
            try:
                from .core.bedrock_server import BedrockServer as _BedrockServer  # type: ignore
                BedrockServer = _BedrockServer
            except Exception:
                try:
                    from core.bedrock_server import BedrockServer as _BedrockServer  # type: ignore
                    BedrockServer = _BedrockServer
                except Exception:
                    BedrockServer = None  # pragma: no cover
        except Exception:
            BedrockServer = None  # pragma: no cover

        total_entries = 0
        aggregated_unique: Dict[str, str] = {}
        scan_errors: List[Dict[str, str]] = []

        for entry in os.listdir(base_servers_path):
            server_dir = os.path.join(base_servers_path, entry)
            if not os.path.isdir(server_dir):
                continue

            server_label = entry
            try:
                server_obj = None
                if BedrockServer is not None:
                    # Try a few common constructor signatures.
                    try:
                        server_obj = BedrockServer(
                            server_dir, app_context=app_context)  # type: ignore
                    except Exception:
                        try:
                            server_obj = BedrockServer(
                                server_dir)  # type: ignore
                        except Exception:
                            try:
                                server_obj = BedrockServer(
                                    name=server_label, app_context=app_context)  # type: ignore
                            except Exception:
                                server_obj = None

                # Validate server is installed (best-effort)
                is_installed = True
                if server_obj is not None:
                    try:
                        attr = getattr(server_obj, 'is_installed', True)
                        is_installed = attr() if callable(attr) else bool(attr)
                    except Exception:
                        is_installed = True

                if not is_installed:
                    continue

                # Scan for players
                players_from_server: List[Dict[str, str]] = []

                if server_obj is not None and hasattr(server_obj, 'scan_log_for_players'):
                    try:
                        res = server_obj.scan_log_for_players()  # type: ignore
                        if isinstance(res, list):
                            players_from_server = res
                        elif isinstance(res, dict):
                            # Accept dict of xuid->name or name->xuid heuristically
                            # Prefer dicts with keys 'name'/'xuid'
                            if 'name' in res and 'xuid' in res:
                                players_from_server = [res]  # single entry
                            else:
                                # Try to coerce mapping to list
                                for k, v in res.items():
                                    # Guess which is xuid: prefer numeric-looking key/value
                                    if isinstance(k, str) and isinstance(v, str):
                                        if k.strip().isdigit():
                                            players_from_server.append(
                                                {'xuid': k.strip(), 'name': v.strip()})
                                        elif v.strip().isdigit():
                                            players_from_server.append(
                                                {'xuid': v.strip(), 'name': k.strip()})
                    except Exception as e:
                        scan_errors.append(
                            {'server': server_label, 'error': str(e)})
                        continue
                else:
                    # If no BedrockServer API available, skip gracefully.
                    continue

                # Normalize and aggregate
                for p in players_from_server:
                    if not isinstance(p, dict):
                        continue
                    name = str(p.get('name', '')).strip()
                    xuid = str(p.get('xuid', '')).strip()
                    if not name or not xuid:
                        continue
                    total_entries += 1
                    aggregated_unique[xuid] = name  # last seen wins

            except Exception as e:
                scan_errors.append({'server': server_label, 'error': str(e)})

        unique_list = [{'name': n, 'xuid': x}
                       for x, n in aggregated_unique.items()]
        unique_count = len(unique_list)

        try:
            saved_count = self.save_player_data(
                unique_list) if unique_list else 0
        except Exception as e:
            scan_errors.append({'server': 'GLOBAL_PLAYER_DB', 'error': str(e)})
            raise FileOperationError(
                f'Failed to save discovered players to database: {e}') from e

        return {
            'total_entries_in_logs': total_entries,
            'unique_players_submitted_for_saving': unique_count,
            'actually_saved_or_updated_in_db': saved_count,
            'scan_errors': scan_errors,
        }
