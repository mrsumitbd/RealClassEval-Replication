from dataclasses import dataclass, asdict, is_dataclass
from datetime import datetime, timedelta
from typing import Any, Iterable, Optional
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''

    def _get_first_attr(self, names: Iterable[str]) -> Optional[Any]:
        for name in names:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    def _to_timestamp(self, v: Any) -> Optional[float]:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, datetime):
            return v.timestamp()
        if isinstance(v, str):
            # try parse float first
            try:
                return float(v)
            except ValueError:
                try:
                    return datetime.fromisoformat(v).timestamp()
                except Exception:
                    return None
        return None

    def _to_seconds(self, v: Any) -> Optional[float]:
        if v is None:
            return None
        if isinstance(v, timedelta):
            return v.total_seconds()
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return None

    def _resolve_expire_ts(self) -> Optional[float]:
        # Direct expire/end attributes
        expire_candidate = self._get_first_attr(
            (
                'expire_at',
                'expired_at',
                'expire_time',
                'expire_ts',
                'end_time',
                'end_at',
                'end_ts',
            )
        )
        expire_ts = self._to_timestamp(expire_candidate)
        if expire_ts is not None:
            return expire_ts

        # Derive from start + duration
        start_candidate = self._get_first_attr(
            (
                'start_time',
                'start_at',
                'start_ts',
                'ts',
                'create_time',
                'created_at',
                'created_ts',
            )
        )
        duration_candidate = self._get_first_attr(
            (
                'duration',
                'duration_seconds',
                'duration_secs',
                'dur',
                'length',
                'length_seconds',
                'time',
                'time_seconds',
            )
        )
        start_ts = self._to_timestamp(start_candidate)
        dur_sec = self._to_seconds(duration_candidate)
        if start_ts is not None and dur_sec is not None:
            return start_ts + dur_sec

        return None

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        expire_ts = self._resolve_expire_ts()
        if expire_ts is None:
            return False
        return time.time() >= expire_ts

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        expire_ts = self._resolve_expire_ts()
        if expire_ts is None:
            return 0.0
        return max(0.0, expire_ts - time.time())

    def _serialize_value(self, v: Any) -> Any:
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, timedelta):
            return v.total_seconds()
        if is_dataclass(v):
            return asdict(v)
        if isinstance(v, dict):
            return {k: self._serialize_value(val) for k, val in v.items()}
        if isinstance(v, (list, tuple, set)):
            return [self._serialize_value(item) for item in v]
        return v

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        data = asdict(self) if is_dataclass(
            self) else dict(getattr(self, '__dict__', {}))
        return {k: self._serialize_value(v) for k, v in data.items()}
