
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    """事件数据标准化器"""

    # 统一使用的键名
    _USER_KEYS = {"user_id", "userId", "uid", "user", "actor"}
    _TARGET_KEYS = {"target_id", "targetId", "target", "object_id", "objectId"}
    _GROUP_KEYS = {"is_group", "group", "isGroup", "is_group_flag"}
    _TIMESTAMP_KEYS = {"timestamp", "time", "ts", "created_at", "createdAt"}

    @staticmethod
    def _find_value(keys: set[str], data: Dict[str, Any]) -> Optional[Any]:
        """在 data 中查找给定键集合中的第一个值。"""
        for key in keys:
            if key in data:
                return data[key]
        return None

    @staticmethod
    def _convert_timestamp(value: Any) -> Optional[str]:
        """将时间戳或 datetime 转换为 ISO 8601 字符串。"""
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(value).isoformat()
            except Exception:
                return None
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, str):
            # 尝试解析 ISO 字符串
            try:
                return datetime.fromisoformat(value).isoformat()
            except Exception:
                return None
        return None

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化事件数据格式。

        1. 统一事件类型字段为 `event_type`。
        2. 统一用户 ID 字段为 `user_id`。
        3. 统一目标 ID 字段为 `target_id`。
        4. 统一是否为组字段为 `is_group`（布尔值）。
        5. 统一时间戳字段为 `timestamp`（ISO 8601 字符串）。
        6. 其余字段保持原样。
        """
        normalized: Dict[str, Any] = {"event_type": event_type}

        # 处理用户 ID
        user_id = EventDataNormalizer._find_value(
            EventDataNormalizer._USER_KEYS, event_data)
        if user_id is not None:
            normalized["user_id"] = str(user_id)

        # 处理目标 ID
        target_id = EventDataNormalizer._find_value(
            EventDataNormalizer._TARGET_KEYS, event_data)
        if target_id is not None:
            normalized["target_id"] = str(target_id)

        # 处理是否为组
        is_group_val = EventDataNormalizer._find_value(
            EventDataNormalizer._GROUP_KEYS, event_data)
        if is_group_val is not None:
            # 兼容多种表示方式
            if isinstance(is_group_val, str):
                normalized["is_group"] = is_group_val.lower() in {
                    "true", "1", "yes", "y"}
            else:
                normalized["is_group"] = bool(is_group_val)

        # 处理时间戳
        ts_val = EventDataNormalizer._find_value(
            EventDataNormalizer._TIMESTAMP_KEYS, event_data)
        if ts_val is not None:
            iso_ts = EventDataNormalizer._convert_timestamp(ts_val)
            if iso_ts:
                normalized["timestamp"] = iso_ts

        # 复制其余字段
        for k, v in event_data.items():
            if k in EventDataNormalizer._USER_KEYS | EventDataNormalizer._TARGET_KEYS | EventDataNormalizer._GROUP_KEYS | EventDataNormalizer._TIMESTAMP_KEYS:
                continue
            normalized[k] = v

        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户 ID。"""
        user_id = EventDataNormalizer._find_value(
            EventDataNormalizer._USER_KEYS, event_data)
        return str(user_id) if user_id is not None else None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        """
        从事件数据中提取目标信息，返回 (target_id, is_group)。

        - target_id: 目标 ID（字符串），若不存在返回 None。
        - is_group: 是否为组（布尔值），默认 False。
        """
        target_id = EventDataNormalizer._find_value(
            EventDataNormalizer._TARGET_KEYS, event_data)
        target_id_str = str(target_id) if target_id is not None else None

        is_group_val = EventDataNormalizer._find_value(
            EventDataNormalizer._GROUP_KEYS, event_data)
        if is_group_val is None:
            is_group = False
        else:
            if isinstance(is_group_val, str):
                is_group = is_group_val.lower() in {"true", "1", "yes", "y"}
            else:
                is_group = bool(is_group_val)

        return target_id_str, is_group
