from typing import Any, Dict, Optional


class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def _get_nested(data: Dict[str, Any], path: str) -> Any:
        """根据以点分隔的路径获取嵌套值"""
        cur: Any = data
        for key in path.split("."):
            if not isinstance(cur, dict):
                return None
            cur = cur.get(key)
            if cur is None:
                return None
        return cur

    @staticmethod
    def _first_non_empty(data: Dict[str, Any], paths: list[str]) -> Any:
        """从多个可能路径中返回第一个非空值"""
        for p in paths:
            v = EventDataNormalizer._get_nested(data, p)
            if v is not None and v != "":
                return v
        return None

    @staticmethod
    def _to_str_or_none(value: Any) -> Optional[str]:
        if value is None:
            return None
        try:
            return str(value)
        except Exception:
            return None

    @staticmethod
    def _infer_is_group(data: Dict[str, Any]) -> Optional[bool]:
        group_types = {
            "group",
            "group_chat",
            "supergroup",
            "channel",
            "guild",
            "team",
            "room",
            "discussion",
            "community",
            "thread",
        }
        private_types = {"private", "direct", "dm", "friend", "user", "single"}
        candidates = [
            "chat_type",
            "message_type",
            "peer_type",
            "conversation_type",
            "channel_type",
            "scene",
            "target_type",
            "session_type",
        ]
        for c in candidates:
            v = EventDataNormalizer._get_nested(data, c)
            if isinstance(v, str):
                vs = v.lower()
                if vs in group_types:
                    return True
                if vs in private_types:
                    return False
        # Fallback by presence of group-like id keys
        group_id_candidates = [
            "group_id",
            "chat_id",
            "channel_id",
            "room_id",
            "team_id",
            "guild_id",
            "server_id",
            "thread_id",
            "discussion_id",
            "community_id",
            "topic_id",
            "conversation_id",
            "message.chat_id",
            "message.channel_id",
            "chat.id",
            "channel.id",
        ]
        for p in group_id_candidates:
            v = EventDataNormalizer._get_nested(data, p)
            if v is not None and v != "":
                return True
        return None

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化事件数据格式"""
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)

        # timestamp normalization
        ts_candidates = [
            "timestamp",
            "time",
            "ts",
            "create_time",
            "event_time",
            "msg_time",
            "message_time",
            "date",
            "sent_at",
            "created_at",
            "message.ts",
            "message.create_time",
        ]
        raw_ts = EventDataNormalizer._first_non_empty(
            event_data, ts_candidates)

        normalized_ts: Optional[int] = None
        if isinstance(raw_ts, (int, float)):
            # Heuristic: if milliseconds, convert to seconds
            if raw_ts > 1_000_000_000_000:
                normalized_ts = int(raw_ts // 1000)
            else:
                normalized_ts = int(raw_ts)
        elif isinstance(raw_ts, str):
            try:
                num = float(raw_ts.strip())
                if num > 1_000_000_000_000:
                    normalized_ts = int(num // 1000)
                else:
                    normalized_ts = int(num)
            except Exception:
                normalized_ts = None

        # message id normalization
        mid = EventDataNormalizer._first_non_empty(
            event_data,
            [
                "message_id",
                "msg_id",
                "id",
                "event_id",
                "mid",
                "message.message_id",
                "message.id",
                "packet_id",
            ],
        )
        message_id = EventDataNormalizer._to_str_or_none(mid)

        return {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_group": is_group,
            "timestamp": normalized_ts,
            "message_id": message_id,
            "raw": event_data,
        }

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户ID"""
        paths = [
            "user_id",
            "uid",
            "from_user_id",
            "from_id",
            "sender_id",
            "author_id",
            "operator_id",
            "op_user_id",
            "openid",
            "open_id",
            "union_id",
            # nested
            "sender.user_id",
            "sender.id",
            "sender.uid",
            "sender.open_id",
            "user.user_id",
            "user.id",
            "user.uid",
            "author.id",
            "operator.id",
            "from.id",
            "message.from_id",
            "message.author_id",
        ]
        val = EventDataNormalizer._first_non_empty(event_data, paths)
        return EventDataNormalizer._to_str_or_none(val)

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """从事件数据中提取目标信息，返回(target_id, is_group)"""
        # Try to infer is_group explicitly first
        inferred_group = EventDataNormalizer._infer_is_group(event_data)

        group_id_candidates = [
            "group_id",
            "chat_id",
            "channel_id",
            "room_id",
            "team_id",
            "guild_id",
            "server_id",
            "thread_id",
            "discussion_id",
            "community_id",
            "topic_id",
            "conversation_id",
            "chat.id",
            "channel.id",
            "message.chat_id",
            "message.channel_id",
        ]
        private_target_candidates = [
            "to_user_id",
            "target_id",
            "peer_id",
            "to_id",
            "receive_id",
            "receiver_id",
            "to.uid",
            "message.to_id",
            "message.peer_id",
        ]

        target_id: Optional[str] = None
        is_group: bool = False

        if inferred_group is True:
            gid = EventDataNormalizer._first_non_empty(
                event_data, group_id_candidates)
            target_id = EventDataNormalizer._to_str_or_none(gid)
            is_group = True
        elif inferred_group is False:
            pid = EventDataNormalizer._first_non_empty(
                event_data, private_target_candidates)
            target_id = EventDataNormalizer._to_str_or_none(pid)
            is_group = False
        else:
            # Unknown: try group first, then private
            gid = EventDataNormalizer._first_non_empty(
                event_data, group_id_candidates)
            if gid is not None:
                target_id = EventDataNormalizer._to_str_or_none(gid)
                is_group = True
            else:
                pid = EventDataNormalizer._first_non_empty(
                    event_data, private_target_candidates)
                target_id = EventDataNormalizer._to_str_or_none(pid)
                is_group = False

        return target_id, is_group
