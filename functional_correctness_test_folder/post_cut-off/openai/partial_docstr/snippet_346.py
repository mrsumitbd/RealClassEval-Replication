
from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化事件数据格式。

        1. 先把可能嵌套在 `data` 字段里的字典展开。
        2. 提取用户 ID、目标 ID 以及是否关注标识。
        3. 统一返回一个包含 `event_type`、`user_id`、`target_id`、`is_follow`、`timestamp` 与原始数据的字典。
        """
        # 展开可能的嵌套字典
        if "data" in event_data and isinstance(event_data["data"], dict):
            event_data = {**event_data, **event_data["data"]}

        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_follow = EventDataNormalizer.extract_target_info(
            event_data)

        # 统一时间戳字段
        timestamp = event_data.get("timestamp") or event_data.get(
            "time") or event_data.get("ts")

        normalized: Dict[str, Any] = {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_follow": is_follow,
            "timestamp": timestamp,
            "raw_data": event_data,
        }
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """
        从事件数据中提取用户 ID。

        支持常见字段名：`user_id`、`uid`、`userId`、`user_id_str`、`user`。
        """
        for key in ("user_id", "uid", "userId", "user_id_str", "user"):
            if key in event_data:
                val = event_data[key]
                if isinstance(val, (str, int)):
                    return str(val)
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        """
        从事件数据中提取目标 ID 与是否关注标识。

        目标 ID 支持字段名：`target_id`、`targetId`、`target_id_str`、`target`。
        是否关注标识支持字段名：`is_follow`、`follow`、`is_following`、`followed`。
        """
        target_id: Optional[str] = None
        for key in ("target_id", "targetId", "target_id_str", "target"):
            if key in event_data:
                val = event_data[key]
                if isinstance(val, (str, int)):
                    target_id = str(val)
                    break

        is_follow: bool = False
        for key in ("is_follow", "follow", "is_following", "followed"):
            if key in event_data:
                val = event_data[key]
                if isinstance(val, bool):
                    is_follow = val
                elif isinstance(val, str):
                    lowered = val.lower()
                    if lowered in ("true", "1", "yes", "y"):
                        is_follow = True
                    elif lowered in ("false", "0", "no", "n"):
                        is_follow = False
                elif isinstance(val, int):
                    is_follow = bool(val)
                break

        return target_id, is_follow
