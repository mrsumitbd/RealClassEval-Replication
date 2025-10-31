from typing import Any, Dict, Optional, Tuple
from datetime import datetime


class EventDataNormalizer:

    @staticmethod
    def _get_from_path(d: Dict[str, Any], *paths: str) -> Optional[Any]:
        for path in paths:
            cur = d
            ok = True
            for key in path.split("."):
                if not isinstance(cur, dict) or key not in cur:
                    ok = False
                    break
                cur = cur[key]
            if ok:
                return cur
        return None

    @staticmethod
    def _to_str(value: Any) -> Optional[str]:
        if value is None:
            return None
        try:
            if isinstance(value, (str, int, float)):
                return str(value)
            # Common ID containers
            if isinstance(value, dict):
                for k in ("id", "ID", "_id"):
                    if k in value:
                        return str(value[k])
            return str(value)
        except Exception:
            return None

    @staticmethod
    def _to_timestamp(value: Any) -> Optional[float]:
        if value is None:
            return None
        # Already numeric
        if isinstance(value, (int, float)):
            return float(value)
        # Slack-like "1693929301.1234"
        if isinstance(value, str):
            v = value.strip()
            # ISO8601
            try:
                if any(ch in v for ch in ("T", "Z", "+")) and any(ch.isdigit() for ch in v):
                    dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                    return dt.timestamp()
            except Exception:
                pass
            # float or int string
            try:
                return float(v)
            except Exception:
                pass
        # Datetime object
        try:
            if isinstance(value, datetime):
                return value.timestamp()
        except Exception:
            pass
        return None

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        v = EventDataNormalizer._get_from_path(
            event_data,
            "user_id",
            "uid",
            "userId",
            "user.id",
            "sender.user_id",
            "sender.uid",
            "sender.id",
            "author.id",
            "from.id",
            "from_user.id",
            "origin.user.id",
            "message.from.id",
            "event.user",
            "event.user_id",
            "context.user_id",
            "source.userId",
            "source.user_id",
            "initiator.id",
            "requester.id",
            "member.user.id",
            "sender",
            "user"  # Slack/Generic
        )
        return EventDataNormalizer._to_str(v)

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        # Telegram
        chat_type = EventDataNormalizer._get_from_path(
            event_data, "chat.type", "message.chat.type")
        chat_id = EventDataNormalizer._get_from_path(
            event_data, "chat.id", "message.chat.id")

        # OneBot/QQ
        group_id = EventDataNormalizer._get_from_path(event_data, "group_id")
        guild_id = EventDataNormalizer._get_from_path(event_data, "guild_id")
        channel_id = EventDataNormalizer._get_from_path(
            event_data, "channel_id")

        # Discord
        discord_guild_id = EventDataNormalizer._get_from_path(
            event_data, "guild.id")
        discord_channel_id = EventDataNormalizer._get_from_path(
            event_data, "channel.id")
        discord_dm = EventDataNormalizer._get_from_path(event_data, "channel.type") == "dm" or bool(
            EventDataNormalizer._get_from_path(event_data, "is_dm")
        )

        # Slack
        slack_channel = EventDataNormalizer._get_from_path(
            event_data, "channel", "event.channel")

        # Matrix
        matrix_room = EventDataNormalizer._get_from_path(
            event_data, "room_id", "event.room_id")

        # Generic
        room_id = EventDataNormalizer._get_from_path(
            event_data, "room.id", "roomId")
        thread_id = EventDataNormalizer._get_from_path(
            event_data, "thread.id", "threadId")
        conv_id = EventDataNormalizer._get_from_path(
            event_data, "conversation.id", "conversationId")

        # Decision tree
        # Telegram
        if chat_id is not None:
            is_group = str(chat_type).lower() in {
                "group", "supergroup", "channel"} if chat_type else False
            return EventDataNormalizer._to_str(chat_id), is_group

        # OneBot/QQ
        if group_id is not None:
            return EventDataNormalizer._to_str(group_id), True
        if channel_id is not None and guild_id is not None:
            return EventDataNormalizer._to_str(channel_id), True
        if channel_id is not None and guild_id is None:
            return EventDataNormalizer._to_str(channel_id), False

        # Discord
        if discord_channel_id is not None and discord_guild_id is not None:
            return EventDataNormalizer._to_str(discord_channel_id), True
        if discord_channel_id is not None and (discord_dm or discord_guild_id is None):
            return EventDataNormalizer._to_str(discord_channel_id), False

        # Slack
        if isinstance(slack_channel, str):
            # Slack DM channels start with 'D', groups 'G', public 'C'
            if slack_channel[:1] == "D":
                return slack_channel, False
            return slack_channel, True

        # Matrix
        if matrix_room is not None:
            return EventDataNormalizer._to_str(matrix_room), True

        # Generic
        if room_id is not None:
            return EventDataNormalizer._to_str(room_id), True
        if thread_id is not None:
            return EventDataNormalizer._to_str(thread_id), True
        if conv_id is not None:
            return EventDataNormalizer._to_str(conv_id), True

        # Fallback: try generic "target_id" and "is_group"
        target_id = EventDataNormalizer._get_from_path(
            event_data, "target_id", "target.id", "to.id", "recipient.id")
        if target_id is not None:
            is_group = bool(
                EventDataNormalizer._get_from_path(
                    event_data, "is_group", "target.is_group", "target.isGroup", "conversation.is_group"
                )
            )
            return EventDataNormalizer._to_str(target_id), is_group

        return None, False

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)

        content_candidates = [
            ("message",),
            ("text",),
            ("content",),
            ("message.content",),
            ("message.text",),
            ("event.text",),
            ("event.message.text",),
            ("event.message",),
            ("data.text",),
            ("data.message",),
            ("payload.text",),
            ("payload.message",),
        ]

        content: Optional[str] = None
        for path_tuple in content_candidates:
            v = EventDataNormalizer._get_from_path(event_data, *path_tuple)
            if v is not None:
                # If message is a dict with 'content' or 'text'
                if isinstance(v, dict):
                    inner = EventDataNormalizer._get_from_path(
                        v, "content", "text", "body")
                    if inner is not None:
                        content = str(inner)
                        break
                content = str(v)
                break

        timestamp_candidates = [
            "timestamp",
            "time",
            "ts",
            "date",
            "created_at",
            "event_ts",
            "message.ts",
            "message.timestamp",
        ]
        ts_val: Optional[float] = None
        for p in timestamp_candidates:
            v = EventDataNormalizer._get_from_path(event_data, p)
            ts_val = EventDataNormalizer._to_timestamp(v)
            if ts_val is not None:
                break

        normalized = {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_group": bool(is_group),
            "content": content,
            "timestamp": ts_val,
            "raw": event_data,
        }
        return normalized
