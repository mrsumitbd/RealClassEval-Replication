from __future__ import annotations

import gzip
import io
import os
import re
from typing import Any, Dict, List, Optional, Tuple


class PlayerMixin:
    _PLAYER_NAME_RE = re.compile(r"[A-Za-z0-9_]{1,32}")
    _UUID_RE = re.compile(
        r"[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}")

    _LOG_PATTERNS = [
        # Vanilla-style: "UUID of player <name> is <uuid>"
        re.compile(
            r"UUID of player\s+(?P<name>[A-Za-z0-9_]{1,32})\s+is\s+(?P<uuid>[0-9a-fA-F\-]{32,36})"
        ),
        # GameProfile{id=<uuid>, name=<name>}
        re.compile(
            r"GameProfile\{id=(?P<uuid>[0-9a-fA-F\-]{32,36}),\s*name=(?P<name>[A-Za-z0-9_]{1,32})\}"
        ),
        # [User Authenticator #N/INFO]: UUID of player <name> is <uuid>
        re.compile(
            r"UUID of player\s+(?P<name>[A-Za-z0-9_]{1,32})\s+is\s+(?P<uuid>[0-9a-fA-F\-]{32,36})",
            re.IGNORECASE,
        ),
        # "logged in with entity id" sometimes includes GameProfile(... name=..., id=...)
        re.compile(
            r"name=(?P<name>[A-Za-z0-9_]{1,32}).*?\bid=(?P<uuid>[0-9a-fA-F\-]{32,36})"
        ),
    ]

    def _ensure_store(self) -> None:
        if "_known_players" not in self.__dict__:
            self.__dict__["_known_players"]: List[Dict[str, str]] = []
        if "_player_index_by_uuid" not in self.__dict__:
            self.__dict__["_player_index_by_uuid"]: Dict[str, int] = {}
        if "_player_index_by_name" not in self.__dict__:
            self.__dict__["_player_index_by_name"]: Dict[str, int] = {}

    @staticmethod
    def _normalize_uuid(u: Optional[str]) -> Optional[str]:
        if not u:
            return None
        s = u.strip().lower()
        if s == "null" or s == "none":
            return None
        s = s.replace("{", "").replace("}", "")
        s = s.replace("-", "")
        if len(s) != 32 or not all(c in "0123456789abcdef" for c in s):
            return None
        # insert dashes 8-4-4-4-12
        return f"{s[0:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:32]}"

    @staticmethod
    def _normalize_name(n: Optional[str]) -> Optional[str]:
        if not n:
            return None
        s = n.strip()
        if not s:
            return None
        return s[:32]

    def _upsert_player(self, name: Optional[str], uuid: Optional[str]) -> bool:
        self._ensure_store()
        n = self._normalize_name(name) if name else None
        u = self._normalize_uuid(uuid) if uuid else None
        if not n and not u:
            return False

        players = self.__dict__["_known_players"]
        idx_by_uuid = self.__dict__["_player_index_by_uuid"]
        idx_by_name = self.__dict__["_player_index_by_name"]

        existing_idx: Optional[int] = None
        if u and u in idx_by_uuid:
            existing_idx = idx_by_uuid[u]
        elif n and n.lower() in idx_by_name:
            existing_idx = idx_by_name[n.lower()]

        if existing_idx is not None:
            record = players[existing_idx]
            changed = False
            if n and record.get("name") != n:
                record["name"] = n
                idx_by_name[n.lower()] = existing_idx
                changed = True
            if u and record.get("uuid") != u:
                old_uuid = record.get("uuid")
                record["uuid"] = u
                if old_uuid and old_uuid in idx_by_uuid:
                    del idx_by_uuid[old_uuid]
                idx_by_uuid[u] = existing_idx
                changed = True
            return changed

        record: Dict[str, str] = {}
        if n:
            record["name"] = n
        if u:
            record["uuid"] = u
        players.append(record)
        new_idx = len(players) - 1
        if u:
            idx_by_uuid[u] = new_idx
        if n:
            idx_by_name[n.lower()] = new_idx
        return True

    def parse_player_cli_argument(self, player_string: str) -> None:
        s = (player_string or "").strip()
        if not s:
            return

        # Support JSON-ish {name:..., uuid:...}
        if s.startswith("{") and s.endswith("}"):
            body = s[1:-1]
            parts = [p.strip() for p in body.split(",")]
            name = None
            uuid = None
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    k = k.strip().strip('"\'')
                    v = v.strip().strip('"\'')
                    if k.lower() == "name":
                        name = v
                    elif k.lower() == "uuid":
                        uuid = v
            self.save_player_data([{"name": name or "", "uuid": uuid or ""}])
            return

        # Support delimiters: name:uuid or name=uuid
        if ":" in s or "=" in s:
            delim = ":" if ":" in s else "="
            left, right = s.split(delim, 1)
            name = left.strip().strip('"\'') or None
            uuid = right.strip().strip('"\'') or None
            # If left looks like uuid and right looks like name, swap
            left_is_uuid = bool(self._UUID_RE.fullmatch(left.strip()))
            right_is_uuid = bool(self._UUID_RE.fullmatch(right.strip()))
            left_is_name = bool(self._PLAYER_NAME_RE.fullmatch(left.strip()))
            right_is_name = bool(self._PLAYER_NAME_RE.fullmatch(right.strip()))
            if left_is_uuid and right_is_name:
                name, uuid = right, left
            self.save_player_data([{"name": name or "", "uuid": uuid or ""}])
            return

        # If single token, detect whether it's a name or uuid
        token = s.strip().strip('"\'')
        if self._UUID_RE.fullmatch(token):
            self.save_player_data([{"uuid": token}])
        else:
            self.save_player_data([{"name": token}])

    def save_player_data(self, players_data: List[Dict[str, str]]) -> int:
        self._ensure_store()
        saved = 0
        for rec in players_data or []:
            name = rec.get("name")
            uuid = rec.get("uuid")
            if self._upsert_player(name, uuid):
                saved += 1
        return saved

    def get_known_players(self) -> List[Dict[str, str]]:
        self._ensure_store()
        # return a shallow copy to avoid external mutation
        return list(self.__dict__["_known_players"])

    def discover_and_store_players_from_all_server_logs(self, app_context: Optional["AppContext"] = None) -> Dict[str, Any]:
        ctx = app_context if app_context is not None else getattr(
            self, "app_context", None)
        candidate_dirs: List[str] = []
        for attr in ("logs_dir", "server_logs_dir", "log_dir", "logs_path"):
            val = getattr(ctx, attr, None) if ctx is not None else None
            if isinstance(val, str) and os.path.isdir(val):
                candidate_dirs.append(val)
            val_self = getattr(self, attr, None)
            if isinstance(val_self, str) and os.path.isdir(val_self):
                candidate_dirs.append(val_self)
        # Fallback: ./logs if exists
        if os.path.isdir("logs"):
            candidate_dirs.append("logs")

        # Deduplicate dirs
        seen_dirs = set()
        dirs = []
        for d in candidate_dirs:
            p = os.path.abspath(d)
            if p not in seen_dirs:
                seen_dirs.add(p)
                dirs.append(p)

        files: List[str] = []
        for d in dirs:
            try:
                for root, _, filenames in os.walk(d):
                    for fn in filenames:
                        if fn.endswith(".log") or fn.endswith(".log.gz") or fn.lower().startswith("latest"):
                            files.append(os.path.join(root, fn))
            except Exception:
                # ignore unreadable dirs
                continue

        discovered: List[Tuple[Optional[str], Optional[str]]] = []
        errors: List[str] = []
        for path in files:
            try:
                if path.endswith(".gz"):
                    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
                        self._scan_log_stream(f, discovered)
                else:
                    with io.open(path, "r", encoding="utf-8", errors="ignore") as f:
                        self._scan_log_stream(f, discovered)
            except Exception as e:
                errors.append(f"{path}: {e}")

        unique: Dict[Tuple[Optional[str], Optional[str]],
                     Tuple[Optional[str], Optional[str]]] = {}
        for name, uuid in discovered:
            key = (name.lower() if name else None,
                   self._normalize_uuid(uuid) if uuid else None)
            unique[key] = (name, self._normalize_uuid(uuid) if uuid else None)

        to_save: List[Dict[str, str]] = []
        for name, uuid in unique.values():
            rec: Dict[str, str] = {}
            if name:
                rec["name"] = name
            if uuid:
                rec["uuid"] = uuid
            if rec:
                to_save.append(rec)

        saved_new = self.save_player_data(to_save) if to_save else 0
        result = {
            "discovered": len(unique),
            "saved_new": saved_new,
            "total_known": len(self.get_known_players()),
            "files_scanned": len(files),
            "errors": errors,
        }
        return result

    def _scan_log_stream(self, stream: io.TextIOBase, out: List[Tuple[Optional[str], Optional[str]]]) -> None:
        for line in stream:
            text = line.strip()
            if not text:
                continue
            for pat in self._LOG_PATTERNS:
                m = pat.search(text)
                if m:
                    name = m.groupdict().get("name")
                    uuid = m.groupdict().get("uuid")
                    name = self._normalize_name(name) if name else None
                    uuid = self._normalize_uuid(uuid) if uuid else None
                    if name or uuid:
                        out.append((name, uuid))
            # Secondary heuristic: if just UUID present nearby "GameProfile" or "id="
            if "GameProfile" in text or "id=" in text:
                uuids = self._UUID_RE.findall(text)
                if uuids:
                    # Try to also find a plausible name nearby
                    name_match = self._PLAYER_NAME_RE.search(text)
                    name = name_match.group(0) if name_match else None
                    out.append((self._normalize_name(name),
                               self._normalize_uuid(uuids[0])))
