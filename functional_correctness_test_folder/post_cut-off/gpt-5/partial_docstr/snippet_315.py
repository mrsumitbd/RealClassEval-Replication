from typing import List, Dict, Any, Optional
import os


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
        '''

    def _ensure_player_db(self) -> None:
        if not hasattr(self, "_player_db") or not isinstance(self._player_db, list):
            self._player_db: List[Dict[str, str]] = []

    def _get_setting(self, dotted_key: str, default: Optional[Any] = None) -> Any:
        settings = getattr(self, "settings", None)
        if not isinstance(settings, dict):
            return default
        # Try dotted access like "paths.servers"
        if dotted_key in settings:
            return settings[dotted_key]
        parts = dotted_key.split(".")
        cur = settings
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return default
        return cur

    def parse_player_cli_argument(self, player_string: str) -> None:
        if not isinstance(player_string, str) or not player_string.strip():
            raise UserInputError("Player string must be a non-empty string.")
        s = player_string.strip()

        # Accept delimiters: ':', '=', ',', whitespace
        delimiters = [":", "=", ","]
        tokens: List[str] = []

        # Try split by known single delimiters first
        for d in delimiters:
            if d in s:
                tokens = [t.strip() for t in s.split(d)]
                break

        # If still no tokens, split by whitespace
        if not tokens:
            tokens = [t.strip() for t in s.split()]

        tokens = [t for t in tokens if t]  # remove empties

        if len(tokens) < 2:
            raise UserInputError(
                "Player string must contain both name and XUID.")
        name, xuid = tokens[0], tokens[1]

        if not isinstance(name, str) or not name.strip():
            raise UserInputError("Player name must be a non-empty string.")
        if not isinstance(xuid, str) or not xuid.strip():
            raise UserInputError("Player XUID must be a non-empty string.")

        # Save/update single player
        self.save_player_data([{"name": name.strip(), "xuid": xuid.strip()}])

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

        cleaned_incoming: Dict[str, Dict[str, str]] = {}

        for idx, item in enumerate(players_data):
            if not isinstance(item, dict):
                raise UserInputError(
                    f"players_data[{idx}] must be a dictionary.")
            if "name" not in item or "xuid" not in item:
                raise UserInputError(
                    f"players_data[{idx}] must contain 'name' and 'xuid' keys.")
            name = item["name"]
            xuid = item["xuid"]
            if not isinstance(name, str) or not name.strip():
                raise UserInputError(
                    f"players_data[{idx}]['name'] must be a non-empty string.")
            if not isinstance(xuid, str) or not xuid.strip():
                raise UserInputError(
                    f"players_data[{idx}]['xuid'] must be a non-empty string.")
            # Normalize
            name = name.strip()
            xuid = xuid.strip()
            cleaned_incoming[xuid] = {"name": name, "xuid": xuid}

        self._ensure_player_db()

        # Build current map by XUID
        current_by_xuid: Dict[str, Dict[str, str]] = {}
        for item in self._player_db:
            try:
                x = item.get("xuid", "").strip()
                n = item.get("name", "").strip()
                if x and isinstance(x, str) and isinstance(n, str):
                    current_by_xuid[x] = {"name": n, "xuid": x}
            except Exception:
                # Skip malformed existing entries
                continue

        changes = 0

        for xuid, incoming in cleaned_incoming.items():
            if xuid not in current_by_xuid:
                current_by_xuid[xuid] = {
                    "name": incoming["name"], "xuid": xuid}
                changes += 1
            else:
                # Update if different
                if current_by_xuid[xuid].get("name") != incoming["name"]:
                    current_by_xuid[xuid]["name"] = incoming["name"]
                    changes += 1

        # Persist back to list (deterministic order by xuid for stability)
        self._player_db = [{"name": v["name"], "xuid": v["xuid"]}
                           for k, v in sorted(current_by_xuid.items(), key=lambda kv: kv[0])]

        return changes

    def get_known_players(self) -> List[Dict[str, str]]:
        '''Retrieves all known players from the database.
        Returns:
            List[Dict[str, str]]: A list of player dictionaries, where each
            dictionary typically contains ``"name"`` and ``"xuid"`` keys.
        '''
        self._ensure_player_db()
        # Return a shallow copy to avoid external mutation
        return [dict(p) for p in self._player_db]

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
        servers_base = self._get_setting("paths.servers")
        if not servers_base or not isinstance(servers_base, str) or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                "Server base directory is not configured or does not exist.")

        scan_errors: List[Dict[str, str]] = []
        total_entries_in_logs = 0
        aggregated_by_xuid: Dict[str, Dict[str, str]] = {}

        # Resolve server class/factory
        server_cls = getattr(self, "BedrockServer", None)
        if server_cls is None:
            server_cls = getattr(self, "server_class", None)
        if server_cls is None:
            server_cls = getattr(self, "server_factory", None)

        # Iterate subdirectories (servers)
        try:
            entries = os.listdir(servers_base)
        except Exception as e:
            raise AppFileNotFoundError(
                f"Unable to list server base directory: {e}")

        for entry in entries:
            server_path = os.path.join(servers_base, entry)
            if not os.path.isdir(server_path):
                continue

            server_name = entry
            try:
                if server_cls is None:
                    raise RuntimeError(
                        "No server class/factory available on manager instance.")
                # Try common ctor signatures
                server_instance = None
                ctor_errors = []

                for ctor in (
                    lambda: server_cls(server_path, app_context=app_context),
                    lambda: server_cls(server_path),
                    lambda: server_cls(path=server_path),
                    lambda: server_cls(root=server_path),
                ):
                    try:
                        server_instance = ctor()
                        break
                    except TypeError as te:
                        ctor_errors.append(str(te))
                    except Exception as e:
                        ctor_errors.append(str(e))
                if server_instance is None:
                    raise RuntimeError(
                        "Could not instantiate server: " + " | ".join(ctor_errors))

                # Determine if installed/valid (best-effort)
                is_installed = True
                if hasattr(server_instance, "is_installed") and callable(getattr(server_instance, "is_installed")):
                    try:
                        is_installed = bool(server_instance.is_installed())
                    except Exception:
                        is_installed = True
                elif hasattr(server_instance, "installed"):
                    try:
                        is_installed = bool(
                            getattr(server_instance, "installed"))
                    except Exception:
                        is_installed = True

                if not is_installed:
                    continue

                if not hasattr(server_instance, "scan_log_for_players") or not callable(getattr(server_instance, "scan_log_for_players")):
                    raise RuntimeError(
                        "Server does not support scanning logs for players.")

                scanned = server_instance.scan_log_for_players()
                if not isinstance(scanned, list):
                    raise RuntimeError(
                        "scan_log_for_players did not return a list.")

                total_entries_in_logs += len(scanned)

                for idx, p in enumerate(scanned):
                    try:
                        name = p.get("name", "").strip(
                        ) if isinstance(p, dict) else ""
                        xuid = p.get("xuid", "").strip(
                        ) if isinstance(p, dict) else ""
                        if isinstance(name, str) and isinstance(xuid, str) and name and xuid:
                            aggregated_by_xuid[xuid] = {
                                "name": name, "xuid": xuid}
                    except Exception:
                        # Skip malformed item
                        continue

            except Exception as e:
                scan_errors.append({"server": server_name, "error": str(e)})
                continue

        unique_list = list(aggregated_by_xuid.values())
        actually_saved = 0
        try:
            actually_saved = self.save_player_data(
                unique_list) if unique_list else 0
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(f"Failed to save discovered players: {e}")

        return {
            "total_entries_in_logs": int(total_entries_in_logs),
            "unique_players_submitted_for_saving": int(len(unique_list)),
            "actually_saved_or_updated_in_db": int(actually_saved),
            "scan_errors": scan_errors,
        }
