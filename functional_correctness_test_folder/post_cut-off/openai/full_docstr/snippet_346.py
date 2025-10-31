
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化事件数据格式。

        1. 统一用户 ID 字段为 `user_id`。
        2. 统一目标 ID 字段为 `target_id`，并根据字段名推断是否为群组。
        3. 添加 `event_type` 字段。
        4. 过滤掉 None 值字段。
        """
        normalized: Dict[str, Any] = {"event_type": event_type}

        # 用户 ID
        user_id = EventDataNormalizer.extract_user_id(event_data)
        if user_id is not None:
            normalized["user_id"] = user_id

        # 目标信息
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        if target_id is not None:
            normalized["target_id"] = target_id
            normalized["is_group"] = is_group

        # 其它字段（保留原始字段，除去已处理的字段）
        for k, v in event_data.items():
            if k in {"user_id", "sender_id", "from_user", "user", "target_id", "group_id", "chat_id", "channel_id"}:
                continue
            if v is not None:
                normalized[k] = v

        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """
        从事件数据中提取用户 ID。

        支持常见字段名：
        - user_id
        - sender_id
        - from_user
        - user
        """
        for key in ("user_id", "sender_id", "from_user", "user"):
            if key in event_data:
                val = event_data[key]
                if val is not None:
                    return str(val)
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        """
        从事件数据中提取目标信息，返回 (target_id, is_group)。

        目标字段优先级：
        1. group_id → is_group = True
        2. chat_id  → is_group = True
        3. channel_id → is_group = True
        4. target_id → is_group = False
        5. user_id  → is_group = False
        """
        # 群组相关字段
        for key in ("group_id", "chat_id", "channel_id"):
            if key in event_data:
                val = event_data[key]
                if val is not None:
                    return str(val), True

        # 单一目标字段
        for key in ("target_id", "user_id"):
            if key in event_data:
                val = event_data[key]
                if val is not None:
                    return str(val), False

        return None, False
