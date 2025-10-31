
import os
from typing import List, Dict, Optional, Any


class UserInputError(Exception):
    pass


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class AppContext:
    def __init__(self, settings=None):
        self.settings = settings or {}


class PlayerMixin:
    '''
    Mixin class for BedrockServerManager that handles player database management.
    '''
    # Simulated in-memory player database for demonstration
    _player_db: Dict[str, Dict[str, str]] = {}

    def parse_player_cli_argument(self, player_string: str) -> None:
        if not isinstance(player_string, str) or not player_string.strip():
            raise UserInputError("Player string must be a non-empty string.")
        # This method is a stub; in a real implementation, it would parse and validate the player string.

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        if not isinstance(players_data, list):
            raise UserInputError("players_data must be a list of dicts.")
        changed = 0
        seen_xuids = set()
        for entry in players_data:
            if not isinstance(entry, dict):
                raise UserInputError("Each player entry must be a dict.")
            if "name" not in entry or "xuid" not in entry:
                raise UserInputError(
                    "Each player dict must have 'name' and 'xuid' keys.")
            name = entry["name"]
            xuid = entry["xuid"]
            if not isinstance(name, str) or not isinstance(xuid, str) or not name.strip() or not xuid.strip():
                raise UserInputError(
                    "Both 'name' and 'xuid' must be non-empty strings.")
            seen_xuids.add(xuid)
            existing = self._player_db.get(xuid)
            if existing is None:
                self._player_db[xuid] = {"name": name, "xuid": xuid}
                changed += 1
            else:
                if existing["name"] != name or existing["xuid"] != xuid:
                    self._player_db[xuid] = {"name": name, "xuid": xuid}
                    changed += 1
        return changed

    def get_known_players(self) -> List[Dict[str, str]]:
        return list(self._player_db.values())

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        # Get settings
        if app_context is not None:
            settings = app_context.settings
        elif hasattr(self, "settings"):
            settings = self.settings
        else:
            settings = {}
        servers_base = settings.get("paths.servers") if settings else None
        if not servers_base or not os.path.isdir(servers_base):
            raise AppFileNotFoundError(
                "Server base directory is not configured or does not exist.")
        total_entries_in_logs = 0
        unique_players = {}
        scan_errors = []
        # Simulate BedrockServer and ServerPlayerMixin

        class DummyServer:
            def __init__(self, path):
                self.path = path
                self.name = os.path.basename(path)
                self.installed = True

            class player_mixin:
                @staticmethod
                def scan_log_for_players():
                    # Simulate log scan: return list of dicts with 'name' and 'xuid'
                    # For demonstration, use file name as player name, and a fake xuid
                    return [{"name": "Player_" + os.path.basename(os.path.dirname(__file__)), "xuid": "XUID_" + os.path.basename(os.path.dirname(__file__))}]

            def scan_log_for_players(self):
                # For demonstration, simulate a few players
                return [
                    {"name": f"Player_{self.name}_1",
                        "xuid": f"XUID_{self.name}_1"},
                    {"name": f"Player_{self.name}_2",
                        "xuid": f"XUID_{self.name}_2"},
                    {"name": f"Player_{self.name}_1",
                        "xuid": f"XUID_{self.name}_1"},  # duplicate
                ]
        # Iterate subdirectories
        for entry in os.listdir(servers_base):
            server_dir = os.path.join(servers_base, entry)
            if not os.path.isdir(server_dir):
                continue
            try:
                server = DummyServer(server_dir)
                if not getattr(server, "installed", False):
                    continue
                try:
                    players = server.scan_log_for_players()
                except Exception as e:
                    scan_errors.append(
                        {"server": server.name, "error": str(e)})
                    continue
                total_entries_in_logs += len(players)
                for p in players:
                    xuid = p.get("xuid")
                    name = p.get("name")
                    if xuid and name and xuid not in unique_players:
                        unique_players[xuid] = {"name": name, "xuid": xuid}
            except Exception as e:
                scan_errors.append({"server": entry, "error": str(e)})
        unique_players_list = list(unique_players.values())
        actually_saved = 0
        try:
            actually_saved = self.save_player_data(unique_players_list)
        except Exception as e:
            scan_errors.append({"server": "GLOBAL_PLAYER_DB", "error": str(e)})
            raise FileOperationError(
                "Failed to save player data to database.") from e
        return {
            "total_entries_in_logs": total_entries_in_logs,
            "unique_players_submitted_for_saving": len(unique_players_list),
            "actually_saved_or_updated_in_db": actually_saved,
            "scan_errors": scan_errors
        }
