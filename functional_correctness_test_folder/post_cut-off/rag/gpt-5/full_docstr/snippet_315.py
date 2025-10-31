from typing import List, Dict, Optional, Any, Iterable, Tuple, Union
from pathlib import Path
import re


try:
    # Attempt to import project-specific exceptions if available.
    from .exceptions import UserInputError, AppFileNotFoundError, FileOperationError  # type: ignore
except Exception:  # Fallbacks if project-specific exceptions are unavailable.
    class UserInputError(Exception):
        pass

    class AppFileNotFoundError(FileNotFoundError):
        pass

    class FileOperationError(Exception):
        pass


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''

    # Internal key for in-memory DB map: xuid -> name
    _PLAYER_DB_ATTR = "_player_db_map"

    def _ensure_player_db(self) -> Dict[str, str]:
        """Ensures an in-memory player DB mapping is available on the instance."""
        if not hasattr(self, self._PLAYER_DB_ATTR) or not isinstance(getattr(self, self._PLAYER_DB_ATTR), dict):
            setattr(self, self._PLAYER_DB_ATTR, {})
        return getattr(self, self._PLAYER_DB_ATTR)

    def _normalize_players_input(self, players_data: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Validates and normalizes players input into a list of {'name': str, 'xuid': str} dicts."""
        if not isinstance(players_data, Iterable) or isinstance(players_data, (str, bytes)):
            raise UserInputError(
                "players_data must be a list of dictionaries.")

        normalized: List[Dict[str, str]] = []
        for idx, entry in enumerate(players_data):
            if not isinstance(entry, dict):
                raise UserInputError(
                    f"Entry at index {idx} is not a dictionary.")

            if "name" not in entry or "xuid" not in entry:
                raise UserInputError(
                    f"Entry at index {idx} must contain 'name' and 'xuid' keys.")

            name = entry.get("name")
            xuid = entry.get("xuid")

            if not isinstance(name, str) or not isinstance(xuid, str):
                raise UserInputError(
                    f"Entry at index {idx} must have string values for 'name' and 'xuid'.")

            name = name.strip()
            xuid = xuid.strip()

            if not name or not xuid:
                raise UserInputError(
                    f"Entry at index {idx} has empty 'name' or 'xuid' after stripping.")

            normalized.append({"name": name, "xuid": xuid})
        return normalized

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

        # Split by commas, respecting general whitespace.
        raw_pairs = [segment.strip()
                     for segment in player_string.split(',') if segment.strip()]
        if not raw_pairs:
            return

        players: List[Dict[str, str]] = []
        for idx, pair in enumerate(raw_pairs):
            # Split on first colon only to allow colons in names if needed later
            if ':' not in pair:
                raise UserInputError(
                    f"Invalid player pair at position {idx}: '{pair}'. Expected 'name:xuid'.")
            name_part, xuid_part = pair.split(':', 1)
            name = name_part.strip()
            xuid = xuid_part.strip()
            if not name or not xuid:
                raise UserInputError(
                    f"Invalid player pair at position {idx}: '{pair}'. Name or XUID empty after stripping.")
            players.append({"name": name, "xuid": xuid})

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
        normalized = self._normalize_players_input(players_data)
        db = self._ensure_player_db()

        changes = 0
        # Merge by XUID. Keep the last seen name for the same XUID from input.
        for entry in normalized:
            xuid = entry["xuid"]
            name = entry["name"]
            existing = db.get(xuid)

            if existing is None:
                db[xuid] = name
                changes += 1
            elif existing != name:
                db[xuid] = name
                changes += 1

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        db = self._ensure_player_db()
        # Return a stable ordering, by name then xuid.
        return sorted(
            [{"name": name, "xuid": xuid} for xuid, name in db.items()],
            key=lambda d: (d["name"].lower(), d["xuid"])
        )

    def _resolve_servers_base_path(self, app_context: Optional[Any] = None) -> Path:
        """Attempts to resolve the base path for servers from various sources."""
        # Priority: explicit app_context, then self, with multiple possible settings shapes.
        def _extract_settings(obj: Any) -> Optional[dict]:
            if obj is None:
                return None
            s = getattr(obj, "settings", None)
            if isinstance(s, dict):
                return s
            return None

        settings = _extract_settings(
            app_context) or _extract_settings(self) or {}

        base_path: Optional[Union[str, Path]] = None

        # Support flattened key: 'paths.servers'
        if isinstance(settings, dict) and 'paths.servers' in settings:
            base_path = settings.get('paths.servers')

        # Support nested dict: settings['paths']['servers']
        if base_path is None and isinstance(settings, dict):
            paths = settings.get('paths')
            if isinstance(paths, dict):
                base_path = paths.get('servers')

        # As a final fallback, check common attribute names.
        if base_path is None:
            cand = getattr(self, "servers_base_path", None) or getattr(
                self, "servers_path", None)
            if isinstance(cand, (str, Path)):
                base_path = cand

        if base_path is None:
            raise AppFileNotFoundError(
                "Server base directory path is not configured (missing settings['paths.servers']).")

        base = Path(base_path)
        if not base.exists() or not base.is_dir():
            raise AppFileNotFoundError(
                f"Server base directory not found: {base}")

        return base

    def _collect_players_from_server(self, server_obj: Any) -> List[Dict[str, str]]:
        """Collects players from a server object if it provides the expected API."""
        players: List[Dict[str, str]] = []
        if server_obj is None:
            return players

        is_installed = getattr(server_obj, "is_installed", True)
        if callable(is_installed):
            try:
                if not bool(is_installed()):
                    return players
            except Exception:
                pass
        else:
            if not bool(is_installed):
                return players

        scan_func = getattr(server_obj, "scan_log_for_players", None)
        if callable(scan_func):
            result = scan_func()
            if isinstance(result, list):
                for entry in result:
                    if isinstance(entry, dict) and "name" in entry and "xuid" in entry:
                        name = str(entry["name"]).strip()
                        xuid = str(entry["xuid"]).strip()
                        if name and xuid:
                            players.append({"name": name, "xuid": xuid})
        return players

    def _try_instantiate_server(self, server_dir: Path, app_context: Optional[Any]) -> Any:
        """Attempts to instantiate a BedrockServer-like object for a given directory."""
        # Try instance methods on manager that can create a server from path.
        creator = getattr(self, "create_server_from_path", None)
        if callable(creator):
            try:
                return creator(server_dir, app_context=app_context)
            except TypeError:
                try:
                    return creator(server_dir)
                except Exception:
                    pass
            except Exception:
                pass

        # Try using a server class attribute on the manager.
        for attr_name in ("BedrockServer", "Server", "ServerClass"):
            server_cls = getattr(self, attr_name, None)
            if server_cls:
                try:
                    try:
                        return server_cls(server_dir, app_context=app_context)
                    except TypeError:
                        return server_cls(server_dir)
                except Exception:
                    pass

        # Try importing a likely server class if available.
        for mod_path in ("core.bedrock_server", ".core.bedrock_server", "bedrock.core.bedrock_server"):
            try:
                module = __import__(mod_path, fromlist=["BedrockServer"])
                server_cls = getattr(module, "BedrockServer", None)
                if server_cls:
                    try:
                        return server_cls(server_dir, app_context=app_context)
                    except TypeError:
                        return server_cls(server_dir)
            except Exception:
                continue

        # Fallback: return a minimal shim with no players.
        return None

    def _scan_directory_for_players(self, server_dir: Path, app_context: Optional[Any]) -> Tuple[str, List[Dict[str, str]], Optional[str]]:
        """Scans a single server directory for players and returns (server_name, players, error)."""
        server_name = server_dir.name
        # If manager provides a direct scanning utility, use it first.
        for method_name in ("scan_log_for_players_in_server_dir", "scan_log_for_players"):
            method = getattr(self, method_name, None)
            if callable(method):
                try:
                    try:
                        result = method(server_dir=server_dir)
                    except TypeError:
                        try:
                            result = method(server_dir)
                        except TypeError:
                            result = method()
                    players: List[Dict[str, str]] = []
                    if isinstance(result, list):
                        for entry in result:
                            if isinstance(entry, dict) and "name" in entry and "xuid" in entry:
                                name = str(entry["name"]).strip()
                                xuid = str(entry["xuid"]).strip()
                                if name and xuid:
                                    players.append(
                                        {"name": name, "xuid": xuid})
                    return server_name, players, None
                except Exception as e:
                    return server_name, [], str(e)

        # Otherwise attempt to instantiate a server and call its scan method.
        try:
            server_obj = self._try_instantiate_server(server_dir, app_context)
            players = self._collect_players_from_server(server_obj)
            return server_name, players, None
        except Exception as e:
            return server_name, [], str(e)

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[Any] = None) -> Dict[str, Any]:
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
        base_dir = self._resolve_servers_base_path(app_context)

        total_entries: int = 0
        aggregated: List[Dict[str, str]] = []
        scan_errors: List[Dict[str, str]] = []

        for entry in base_dir.iterdir():
            if not entry.is_dir():
                continue
            server_name, players, err = self._scan_directory_for_players(
                entry, app_context)
            if err:
                scan_errors.append({"server": server_name, "error": err})
            total_entries += len(players)
            aggregated.extend(players)

        # Deduplicate by XUID, preserve last occurrence's name.
        unique_by_xuid: Dict[str, str] = {}
        for p in aggregated:
            xuid = p["xuid"].strip()
            name = p["name"].strip()
            if xuid and name:
                unique_by_xuid[xuid] = name

        unique_players = [{"name": name, "xuid": xuid}
                          for xuid, name in unique_by_xuid.items()]

        try:
            saved_count = self.save_player_data(
                unique_players) if unique_players else 0
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(
                f"Failed to save global player database: {e}") from e

        return {
            "total_entries_in_logs": total_entries,
            "unique_players_submitted_for_saving": len(unique_players),
            "actually_saved_or_updated_in_db": saved_count,
            "scan_errors": scan_errors,
        }
