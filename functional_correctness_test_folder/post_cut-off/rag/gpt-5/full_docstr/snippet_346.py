from typing import Any, Dict, Optional


class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化事件数据格式"""
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        return {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_group": is_group,
            "payload": event_data,
        }

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户ID"""
        # Direct id-like fields
        direct_user_id_keys = [
            "user_id",
            "userid",
            "uid",
            "from_id",
            "author_id",
            "operator_id",
            "sender_id",
            "account_id",
            "member_id",
            "actor_id",
            "owner_id",
            "creator_id",
        ]
        for k in direct_user_id_keys:
            if k in event_data:
                v = event_data.get(k)
                sid = EventDataNormalizer._to_str_id(v)
                if sid:
                    return sid

        # Nested common user containers
        nested_user_keys = [
            "user",
            "sender",
            "from",
            "from_user",
            "author",
            "operator",
            "account",
            "member",
            "actor",
            "owner",
            "creator",
            "initiator",
            "profile",
            "source",
            "participant",
        ]
        for k in nested_user_keys:
            obj = event_data.get(k)
            sid = EventDataNormalizer._extract_id_from_obj(obj)
            if sid:
                return sid

        # Look into typical nested envelopes one level
        envelope_keys = ["message", "event",
                         "data", "detail", "payload", "body"]
        for env in envelope_keys:
            sub = event_data.get(env)
            if isinstance(sub, dict):
                # Try direct fields inside envelope
                for k in direct_user_id_keys:
                    if k in sub:
                        sid = EventDataNormalizer._to_str_id(sub.get(k))
                        if sid:
                            return sid
                # Try nested inside envelope
                for k in nested_user_keys:
                    sid = EventDataNormalizer._extract_id_from_obj(sub.get(k))
                    if sid:
                        return sid

        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """从事件数据中提取目标信息，返回(target_id, is_group)"""
        # Initial is_group from explicit flag or type hints
        is_group = bool(event_data.get("is_group", False))

        type_hint_keys = [
            "message_type",
            "chat_type",
            "conversation_type",
            "target_type",
            "channel_type",
            "room_type",
            "peer_type",
            "thread_type",
        ]
        group_like_types = {
            "group",
            "guild",
            "room",
            "channel",
            "team",
            "server",
            "community",
            "supergroup",
            "forum",
            "thread",
        }
        private_like_types = {"private", "dm",
                              "direct", "one_to_one", "personal"}
        for k in type_hint_keys:
            v = event_data.get(k)
            if isinstance(v, str):
                lv = v.lower()
                if lv in group_like_types:
                    is_group = True
                elif lv in private_like_types:
                    is_group = False

        # Try to get target id according to is_group
        target_id = None

        # 1) Telegram-like chat object
        chat = event_data.get("chat")
        if isinstance(chat, dict):
            chat_type = str(chat.get("type", "")).lower()
            if chat_type in group_like_types:
                is_group = True
            elif chat_type in private_like_types:
                is_group = False
            cid = EventDataNormalizer._extract_id_from_obj(chat)
            if cid:
                target_id = cid

        # 2) Direct group id keys
        group_id_keys = [
            "group_id",
            "gid",
            "guild_id",
            "room_id",
            "channel_id",
            "team_id",
            "server_id",
            "community_id",
            "forum_id",
            "thread_id",
        ]
        # 3) Neutral/other target id keys
        neutral_target_id_keys = [
            "target_id",
            "to_id",
            "recipient_id",
            "conversation_id",
            "chat_id",
            "peer_id",
            "session_id",
        ]

        # Prefer group keys if is_group
        if is_group and target_id is None:
            for k in group_id_keys:
                if k in event_data:
                    sid = EventDataNormalizer._to_str_id(event_data.get(k))
                    if sid:
                        target_id = sid
                        break

        # Nested group objects
        if is_group and target_id is None:
            nested_group_keys = [
                "group",
                "guild",
                "room",
                "channel",
                "team",
                "server",
                "community",
                "forum",
                "thread",
            ]
            for k in nested_group_keys:
                sid = EventDataNormalizer._extract_id_from_obj(
                    event_data.get(k))
                if sid:
                    target_id = sid
                    break

        # If not group or still not found, try neutral keys
        if target_id is None:
            for k in neutral_target_id_keys:
                if k in event_data:
                    sid = EventDataNormalizer._to_str_id(event_data.get(k))
                    if sid:
                        target_id = sid
                        break

        # Other nested candidates
        if target_id is None:
            nested_neutral_keys = ["target", "to", "recipient", "conversation"]
            for k in nested_neutral_keys:
                sid = EventDataNormalizer._extract_id_from_obj(
                    event_data.get(k))
                if sid:
                    target_id = sid
                    break

        # Dive into envelopes if still missing
        if target_id is None:
            envelope_keys = ["message", "event",
                             "data", "detail", "payload", "body"]
            for env in envelope_keys:
                sub = event_data.get(env)
                if not isinstance(sub, dict):
                    continue
                # chat nested
                chat = sub.get("chat")
                if isinstance(chat, dict):
                    chat_type = str(chat.get("type", "")).lower()
                    if chat_type in group_like_types:
                        is_group = True
                    elif chat_type in private_like_types:
                        is_group = False
                    sid = EventDataNormalizer._extract_id_from_obj(chat)
                    if sid:
                        target_id = sid
                        break
                # direct group keys
                if is_group and target_id is None:
                    for k in group_id_keys:
                        if k in sub:
                            sid = EventDataNormalizer._to_str_id(sub.get(k))
                            if sid:
                                target_id = sid
                                break
                if target_id is not None:
                    break
                # neutral keys
                for k in neutral_target_id_keys:
                    if k in sub:
                        sid = EventDataNormalizer._to_str_id(sub.get(k))
                        if sid:
                            target_id = sid
                            break
                if target_id is not None:
                    break
                # nested objects
                for k in ["group", "guild", "room", "channel", "team", "server", "community", "forum", "thread", "target", "to", "recipient", "conversation"]:
                    sid = EventDataNormalizer._extract_id_from_obj(sub.get(k))
                    if sid:
                        target_id = sid
                        break
                if target_id is not None:
                    break

        # If a group-like id was found via group keys, ensure is_group True
        if not is_group and target_id is not None:
            # Heuristic: If the id came from clear group key or object, set is_group True
            for k in group_id_keys:
                if k in event_data and EventDataNormalizer._to_str_id(event_data.get(k)) == target_id:
                    is_group = True
                    break

        return target_id, is_group

    @staticmethod
    def _to_str_id(v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, (str, int)):
            s = str(v).strip()
            return s if s else None
        if isinstance(v, dict):
            # Try common id fields
            for k in ("id", "user_id", "gid", "group_id"):
                if k in v:
                    return EventDataNormalizer._to_str_id(v.get(k))
        return None

    @staticmethod
    def _extract_id_from_obj(obj: Any) -> Optional[str]:
        if obj is None:
            return None
        if isinstance(obj, (str, int)):
            return EventDataNormalizer._to_str_id(obj)
        if isinstance(obj, dict):
            # Prefer explicit id fields
            for k in ("id", "user_id", "group_id", "guild_id", "room_id", "channel_id", "thread_id"):
                if k in obj:
                    sid = EventDataNormalizer._to_str_id(obj.get(k))
                    if sid:
                        return sid
            # Fallback: find any *_id field
            for k, v in obj.items():
                if isinstance(k, str) and k.endswith("_id"):
                    sid = EventDataNormalizer._to_str_id(v)
                    if sid:
                        return sid
        return None
