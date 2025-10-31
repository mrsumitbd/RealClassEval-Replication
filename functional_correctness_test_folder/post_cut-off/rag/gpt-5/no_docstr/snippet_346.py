from typing import Any, Dict, Optional


class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化事件数据格式"""
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)

        def _pick_timestamp(data: Dict[str, Any]) -> Any:
            # 平铺字段
            for k in ("timestamp", "ts", "time", "date", "created_at", "occurred_at"):
                if k in data and data[k] is not None:
                    return data[k]
            # 常见嵌套字段
            nested_paths = [
                ("message", "timestamp"),
                ("message", "ts"),
                ("chat", "timestamp"),
                ("event", "timestamp"),
            ]
            for path in nested_paths:
                v = EventDataNormalizer._get_in(data, path)
                if v is not None:
                    return v
            return None

        def _pick_content(data: Dict[str, Any]) -> Optional[str]:
            # 平铺字段
            for k in ("message", "text", "content", "body", "msg", "messageText"):
                v = data.get(k)
                if isinstance(v, str) and v:
                    return v
                # 允许 message 为 dict
                if isinstance(v, dict):
                    for kk in ("text", "content", "body"):
                        vv = v.get(kk)
                        if isinstance(vv, str) and vv:
                            return vv
            # 常见嵌套字段
            nested_paths = [
                ("message", "text"),
                ("message", "content"),
                ("message", "body"),
                ("data", "text"),
                ("data", "content"),
            ]
            for path in nested_paths:
                v = EventDataNormalizer._get_in(data, path)
                if isinstance(v, str) and v:
                    return v
            return None

        normalized: Dict[str, Any] = {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_group": is_group,
            "timestamp": _pick_timestamp(event_data),
            "content": _pick_content(event_data),
            "raw": event_data,
        }
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户ID"""
        # 直接字段
        direct_keys = ("user_id", "uid", "userId",
                       "from_user_id", "sender_id", "author_id")
        for k in direct_keys:
            v = event_data.get(k)
            if v is not None:
                s = EventDataNormalizer._to_str(v)
                if s:
                    return s

        # 常见嵌套结构
        nested_candidates = [
            ("sender", "id"),
            ("sender", "user_id"),
            ("user", "id"),
            ("user", "user_id"),
            ("from", "id"),
            ("author", "id"),
            ("message", "from", "id"),
            ("message", "sender", "id"),
            ("event", "user", "id"),
            ("context", "user", "id"),
        ]
        for path in nested_candidates:
            v = EventDataNormalizer._get_in(event_data, path)
            if v is not None:
                s = EventDataNormalizer._to_str(v)
                if s:
                    return s

        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """从事件数据中提取目标信息，返回(target_id, is_group)"""

        # 如果事件自身已有 is_group 标志
        is_group = bool(event_data.get("is_group")) if isinstance(
            event_data.get("is_group"), bool) else False

        # 显式群聊/频道标识
        group_keys = (
            "group_id",
            "room_id",
            "chat_id",
            "channel_id",
            "guild_id",
            "team_id",
            "discussion_id",
            "conversation_id",
        )
        for k in group_keys:
            v = event_data.get(k)
            if v is not None:
                s = EventDataNormalizer._to_str(v)
                if s:
                    return s, True or is_group  # 一旦命中群标识，视为群聊

        # 私聊/用户目标标识
        private_keys = (
            "to_user_id",
            "target_user_id",
            "peer_id",
            "friend_id",
            "dm_id",
            "recipient_id",
            "receiver_id",
        )
        for k in private_keys:
            v = event_data.get(k)
            if v is not None:
                s = EventDataNormalizer._to_str(v)
                if s:
                    return s, False

        # 依据 message/chat 对象内的信息判断
        # 一些平台 chat.type in {"group", "supergroup", "channel", "private"}
        chat_type = EventDataNormalizer._get_in(event_data, ("chat", "type")) or EventDataNormalizer._get_in(
            event_data, ("message", "chat", "type")
        )
        chat_id = (
            EventDataNormalizer._get_in(event_data, ("chat", "id"))
            or EventDataNormalizer._get_in(event_data, ("message", "chat", "id"))
            or EventDataNormalizer._get_in(event_data, ("channel", "id"))
        )
        if chat_id is not None:
            chat_id_str = EventDataNormalizer._to_str(chat_id)
            if chat_id_str:
                if isinstance(chat_type, str):
                    is_grp = chat_type.lower() in {
                        "group", "supergroup", "channel", "guild", "room"}
                else:
                    is_grp = is_group
                return chat_id_str, is_grp

        # 根据 message_type / conversation_type 推断
        msg_type = (
            event_data.get("message_type")
            or event_data.get("conversation_type")
            or EventDataNormalizer._get_in(event_data, ("message", "type"))
        )
        if isinstance(msg_type, str):
            lower = msg_type.lower()
            if lower in {"group", "supergroup", "channel", "guild", "room"}:
                # 尝试通用目标键
                for k in ("target_id", "chat_id", "group_id", "channel_id"):
                    v = event_data.get(k) or EventDataNormalizer._get_in(
                        event_data, ("message", k))
                    if v is not None:
                        s = EventDataNormalizer._to_str(v)
                        if s:
                            return s, True
            if lower in {"private", "direct", "dm"}:
                for k in ("target_id", "to_user_id", "peer_id", "recipient_id"):
                    v = event_data.get(k) or EventDataNormalizer._get_in(
                        event_data, ("message", k))
                    if v is not None:
                        s = EventDataNormalizer._to_str(v)
                        if s:
                            return s, False

        # 回退：尝试通用 target_id
        v = event_data.get("target_id")
        if v is not None:
            s = EventDataNormalizer._to_str(v)
            if s:
                return s, is_group

        # 无法确定，返回 None
        return None, is_group

    @staticmethod
    def _to_str(v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            return s or None
        try:
            return str(v)
        except Exception:
            return None

    @staticmethod
    def _get_in(data: Dict[str, Any], path: tuple[str, ...]) -> Any:
        cur: Any = data
        for key in path:
            if not isinstance(cur, dict) or key not in cur:
                return None
            cur = cur[key]
        return cur
