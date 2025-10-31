from typing import Any, Dict, Optional

from datetime import datetime


class EventDataNormalizer:
    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        timestamp = EventDataNormalizer._extract_timestamp(event_data)

        return {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_group": is_group,
            "timestamp": timestamp,
        }

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        def from_value(val: Any) -> Optional[str]:
            if val is None:
                return None
            if isinstance(val, (str, int)):
                return str(val)
            if isinstance(val, dict):
                for k in ("id", "user_id", "userId", "uid", "username", "name"):
                    if k in val and val[k] not in (None, ""):
                        return str(val[k])
            return None

        direct_keys = (
            "user_id",
            "userId",
            "uid",
            "user",
            "sender",
            "from",
            "actor",
            "author",
            "initiator",
            "account",
            "profile",
        )
        for k in direct_keys:
            if k in event_data:
                uid = from_value(event_data.get(k))
                if uid:
                    return uid

        nested_keys = ("context", "metadata", "payload", "data")
        for nk in nested_keys:
            v = event_data.get(nk)
            if isinstance(v, dict):
                for k in direct_keys:
                    if k in v:
                        uid = from_value(v.get(k))
                        if uid:
                            return uid

        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        def from_value(val: Any) -> Optional[str]:
            if val is None:
                return None
            if isinstance(val, (str, int)):
                return str(val)
            if isinstance(val, dict):
                for k in ("id", "channel_id", "room_id", "group_id", "team_id", "guild_id", "server_id", "conversation_id", "thread_id", "chat_id", "name"):
                    if k in val and val[k] not in (None, ""):
                        return str(val[k])
            return None

        def detect_is_group_by_container(val: Any) -> Optional[bool]:
            if isinstance(val, dict):
                # Explicit hints
                for k in ("is_group", "group", "isGroup", "is_room", "isChannel"):
                    if k in val and isinstance(val[k], bool):
                        return bool(val[k])
                # Type based hints
                t = val.get("type")
                if isinstance(t, str):
                    t_low = t.lower()
                    if t_low in ("group", "supergroup", "channel", "room", "guild", "server", "team", "thread"):
                        return True
                    if t_low in ("dm", "direct", "private", "user"):
                        return False
                # Platform specific
                chat_type = val.get("chat", {}).get(
                    "type") if isinstance(val.get("chat"), dict) else None
                if isinstance(chat_type, str):
                    if chat_type.lower() in ("group", "supergroup", "channel"):
                        return True
                    if chat_type.lower() in ("private", "dm"):
                        return False
            return None

        # Prefer group-like targets first
        group_keys = (
            "channel_id",
            "channel",
            "room_id",
            "room",
            "group_id",
            "group",
            "team_id",
            "team",
            "guild_id",
            "guild",
            "server_id",
            "server",
            "conversation_id",
            "conversation",
            "thread_id",
            "thread",
            "chat",  # may be group or private
        )
        for k in group_keys:
            if k in event_data:
                container = event_data.get(k)
                tid = from_value(container)
                if tid:
                    is_group = detect_is_group_by_container(container)
                    if is_group is None:
                        # Heuristic by key name
                        # chat ambiguous; default False later
                        is_group = k not in ("chat",)
                    if k == "chat" and is_group is None:
                        # Telegram-like
                        chat_type = None
                        if isinstance(container, dict):
                            chat_type = container.get("type")
                        if isinstance(chat_type, str) and chat_type.lower() in ("group", "supergroup", "channel"):
                            is_group = True
                        elif isinstance(chat_type, str) and chat_type.lower() in ("private", "dm"):
                            is_group = False
                        else:
                            is_group = False
                    return tid, bool(is_group)

        # Recipient-like keys (user target)
        user_target_keys = ("recipient", "to", "target",
                            "peer", "user", "user_id", "userId")
        for k in user_target_keys:
            if k in event_data:
                tid = from_value(event_data.get(k))
                if tid:
                    return tid, False

        # Nested containers
        for nk in ("context", "payload", "metadata", "data"):
            v = event_data.get(nk)
            if isinstance(v, dict):
                for k in group_keys:
                    if k in v:
                        tid = from_value(v.get(k))
                        if tid:
                            is_group = detect_is_group_by_container(v.get(k))
                            if is_group is None:
                                is_group = k not in ("chat",)
                            return tid, bool(is_group)
                for k in user_target_keys:
                    if k in v:
                        tid = from_value(v.get(k))
                        if tid:
                            return tid, False

        return None, False

    @staticmethod
    def _extract_timestamp(event_data: Dict[str, Any]) -> Optional[int]:
        # Returns Unix timestamp in seconds
        def normalize_num(n: float) -> int:
            # Heuristic: if milliseconds, convert to seconds
            if n > 1_000_000_000_000:  # > ~2001-09-09 in ms
                return int(n // 1000)
            if n > 1_000_000_000:  # seconds already
                return int(n)
            # Could be seconds (before 2001) or ms small test; default as seconds
            return int(n)

        candidate_keys = ("timestamp", "time", "ts",
                          "created_at", "createdAt", "date", "datetime")
        for k in candidate_keys:
            if k in event_data:
                val = event_data.get(k)
                if val is None or val == "":
                    continue
                # Numeric
                if isinstance(val, (int, float)):
                    return normalize_num(float(val))
                # ISO string or numeric string
                if isinstance(val, str):
                    s = val.strip()
                    # numeric-like
                    try:
                        num = float(s)
                        return normalize_num(num)
                    except ValueError:
                        pass
                    # try ISO 8601
                    try:
                        # Support Z
                        if s.endswith("Z"):
                            dt = datetime.fromisoformat(
                                s.replace("Z", "+00:00"))
                        else:
                            dt = datetime.fromisoformat(s)
                        return int(dt.timestamp())
                    except Exception:
                        pass

        # Nested containers
        for nk in ("context", "metadata", "payload", "data"):
            v = event_data.get(nk)
            if isinstance(v, dict):
                ts = EventDataNormalizer._extract_timestamp(v)
                if ts is not None:
                    return ts
        return None
