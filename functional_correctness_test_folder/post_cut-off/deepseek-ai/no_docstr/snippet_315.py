
from typing import List, Dict, Any, Optional


class PlayerMixin:

    def parse_player_cli_argument(self, player_string: str) -> None:
        pass

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        pass

    def get_known_players(self) -> List[Dict[str, str]]:
        pass

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[Any] = None) -> Dict[str, Any]:
        pass
