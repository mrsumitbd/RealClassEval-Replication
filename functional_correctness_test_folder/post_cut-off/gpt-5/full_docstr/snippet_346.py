from typing import Any, Dict, Optional, Iterable
from datetime import datetime
import time


class EventDataNormalizer:
    '''事件数据标准化器'''

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        if not isinstance(event_data, dict):
            event_data = {}

        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)

        content = EventDataNormalizer._get_first(
            event_data,
            (
                "message",
                "content",
                "text",
                "body",
                "msg",
                "raw_message",
                "payload.message",
                "payload.text",
                "data.content",
                "data.text",
            ),
        )

        ts = EventDataNormalizer._extract_timestamp(event_data)

        normalized: Dict[str, Any] = {
            "event_type": event_type,
            "user_id": str(user_id) if user_id is not None else None,
            "target_id": str(target_id) if target_id is not None else None,
            "is_group": bool(is_group),
            "content": content,
            "timestamp": ts,
            "raw": event_data,
        }
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        if not isinstance(event_data, dict):
            return None

        candidates: Iterable[str] = (
            # common flat keys
            "user_id",
            "userId",
            "uid",
            "openid",
            "open_id",
            "qq",
            "wxid",
            "author_id",
            "from_id",
            "sender_id",
            "operator_id",
            "member_id",
            "member.user_id",
            "member.id",
            # nested sender/author/from
            "sender.user_id",
            "sender.id",
            "sender.uid",
            "sender.qq",
            "sender.openid",
            "author.user_id",
            "author.id",
            "from.user_id",
            "from.id",
            "user.id",
            "user.user_id",
            "account.id",
            "member.user.id",
            # telegram-like
            "message.from.id",
            "message.from_id",
            "effective_user.id",
            # discord-like
            "author.id",
            # lark/dingtalk-like
            "event.sender.sender_id.user_id",
            "event.sender.user_id",
            "header.user_id",
        )

        val = EventDataNormalizer._get_first(event_data, candidates)
        if val is None:
            return None
        try:
            return str(EventDataNormalizer._to_scalar(val))
        except Exception:
            return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        if not isinstance(event_data, dict):
            return (None, False)

        # Determine chat context from explicit flags/types if any
        chat_type = EventDataNormalizer._get_first(
            event_data,
            (
                "chat_type",
                "message.chat.type",
                "chat.type",
                "conversation.type",
                "channel_type",
                "thread.type",
                "room.type",
                "guild.type",
                "group_type",
                "payload.chat.type",
            ),
        )
        type_to_group = {"group", "supergroup", "channel",
                         "guild", "room", "thread", "community"}

        # Candidate keys for group-like targets
        group_keys: Iterable[str] = (
            "group_id",
            "gid",
            "group.id",
            "message.group_id",
            "message.group.id",
            "chat_id",
            "chat.id",
            "message.chat.id",
            "channel_id",
            "channel.id",
            "guild_id",
            "guild.id",
            "server_id",
            "room_id",
            "room.id",
            "thread_id",
            "thread.id",
            "conversation_id",
            "conversation.id",
            "target.group_id",
            "to_chat_id",
            "to.id",
        )

        # Candidate keys for private/direct targets
        private_keys: Iterable[str] = (
            "peer_id",
            "target_id",
            "to_user_id",
            "to.id",
            "recipient_id",
            "dm_id",
            "message.peer_id",
        )

        # If explicit chat object exists, use it
        chat_id = EventDataNormalizer._get_first(
            event_data,
            (
                "chat.id",
                "message.chat.id",
                "message.to_id",
                "conversation_id",
                "conversation.id",
            ),
        )

        # Fallback detection
        target_id = (
            EventDataNormalizer._get_first(event_data, group_keys)
            or chat_id
            or EventDataNormalizer._get_first(event_data, private_keys)
        )

        # Determine is_group
        is_group = False
        if isinstance(chat_type, str) and chat_type.lower() in type_to_group:
            is_group = True
        else:
            # Heuristic by key presence
            if EventDataNormalizer._get_first(event_data, group_keys) is not None:
                is_group = True

        if target_id is None:
            return (None, False)

        try:
            target_id_s = str(EventDataNormalizer._to_scalar(target_id))
        except Exception:
            target_id_s = None

        return (target_id_s, is_group)

    # Helpers

    @staticmethod
    def _get_first(data: Dict[str, Any], keys: Iterable[str]) -> Any:
        for k in keys:
            val = EventDataNormalizer._get_path(data, k)
            if val is not None:
                return val
        return None

    @staticmethod
    def _get_path(data: Any, path: str) -> Any:
        if not isinstance(data, dict):
            return None
        cur: Any = data
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur

    @staticmethod
    def _to_scalar(value: Any) -> Any:
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, dict):
            # common id fields inside object
            for k in ("id", "user_id", "gid", "uid"):
                if k in value:
                    return value[k]
        # Fallback to string
        return str(value)

    @staticmethod
    def _extract_timestamp(event_data: Dict[str, Any]) -> Optional[int]:
        ts_val = EventDataNormalizer._get_first(
            event_data,
            (
                "timestamp",
                "time",
                "ts",
                "date",
                "created_at",
                "message.date",
                "message.timestamp",
                "header.create_time",
                "event_time",
            ),
        )
        if ts_val is None:
            return None

        # numeric epoch seconds or milliseconds
        if isinstance(ts_val, (int, float)):
            # Heuristic: treat > 10^12 as ms, > 10^9 as s
            if ts_val > 1e12:
                return int(ts_val // 1000)
            if ts_val > 1e10:
                # likely milliseconds as float
                return int(ts_val / 1000)
            return int(ts_val)

        # ISO8601 string or other parsable date string
        if isinstance(ts_val, str):
            s = ts_val.strip()
            # If it's a pure digit string
            if s.isdigit():
                num = int(s)
                if num > 1_000_000_000_000:  # ms
                    return num // 1000
                return num
            # Try to parse common formats
            for fmt in (
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ):
                try:
                    dt = datetime.strptime(s, fmt)
                    if dt.tzinfo is None:
                        # treat as local time; convert to epoch
                        return int(time.mktime(dt.timetuple()))
                    return int(dt.timestamp())
                except Exception:
                    continue
            try:
                # Last resort: fromisoformat (Python's flexible parser)
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None:
                    return int(time.mktime(dt.timetuple()))
                return int(dt.timestamp())
            except Exception:
                return None

        return None
