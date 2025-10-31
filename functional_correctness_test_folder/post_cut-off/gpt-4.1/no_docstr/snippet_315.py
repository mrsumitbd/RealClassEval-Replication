
from typing import List, Dict, Optional, Any
import re
import os
import json


class AppContext:
    # Dummy placeholder for AppContext
    def __init__(self, log_dirs: List[str]):
        self.log_dirs = log_dirs


class PlayerMixin:
    _player_data_file = "players_data.json"

    def parse_player_cli_argument(self, player_string: str) -> None:
        # Example format: "name:JohnDoe,id:1234"
        player_info = {}
        for part in player_string.split(','):
            if ':' in part:
                key, value = part.split(':', 1)
                player_info[key.strip()] = value.strip()
        if player_info:
            self.save_player_data([player_info])

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        existing = self.get_known_players()
        existing_ids = set()
        for p in existing:
            if 'id' in p:
                existing_ids.add(p['id'])
        new_players = []
        for pdata in players_data:
            if 'id' in pdata and pdata['id'] not in existing_ids:
                new_players.append(pdata)
                existing_ids.add(pdata['id'])
        if new_players:
            all_players = existing + new_players
            with open(self._player_data_file, 'w', encoding='utf-8') as f:
                json.dump(all_players, f, indent=2)
            return len(new_players)
        return 0

    def get_known_players(self) -> List[Dict[str, str]]:
        if os.path.exists(self._player_data_file):
            with open(self._player_data_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional[AppContext] = None) -> Dict[str, Any]:
        found_players = []
        log_dirs = []
        if app_context and hasattr(app_context, 'log_dirs'):
            log_dirs = app_context.log_dirs
        else:
            log_dirs = ['logs']
        player_pattern = re.compile(
            r'Player\s+joined:\s*name=(\w+),\s*id=(\d+)')
        for log_dir in log_dirs:
            if not os.path.isdir(log_dir):
                continue
            for fname in os.listdir(log_dir):
                if not fname.endswith('.log'):
                    continue
                fpath = os.path.join(log_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        for line in f:
                            m = player_pattern.search(line)
                            if m:
                                name, pid = m.group(1), m.group(2)
                                found_players.append({'name': name, 'id': pid})
                except Exception:
                    continue
        added = self.save_player_data(found_players)
        return {
            'found': len(found_players),
            'added': added,
            'players': found_players
        }
