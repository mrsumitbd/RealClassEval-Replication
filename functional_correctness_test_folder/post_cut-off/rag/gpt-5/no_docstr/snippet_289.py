from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union


def _isoformat_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    s = dt.isoformat()
    if s.endswith("+00:00"):
        s = s[:-6] + "Z"
    return s


def _try_parse_iso_to_utc_z(s: str) -> Optional[str]:
    try:
        s2 = s.replace("Z", "+00:00") if s.endswith("Z") else s
        dt = datetime.fromisoformat(s2)
        return _isoformat_utc(dt)
    except Exception:
        return None


def _to_serializable(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return _isoformat_utc(obj)
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_to_serializable(v) for v in obj]
    return obj


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    status: Optional[str] = None
    enabled: Optional[bool] = None
    schedule_at: Optional[Union[str, datetime]] = None
    comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)
        if self.enabled is not None and not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a bool or None")
        if self.comment is not None and not isinstance(self.comment, str):
            self.comment = str(self.comment)
        if self.metadata is not None and not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict or None")
        if self.extra is None:
            self.extra = {}
        if not isinstance(self.extra, dict):
            raise TypeError("extra must be a dict")

        if isinstance(self.schedule_at, datetime):
            self.schedule_at = _isoformat_utc(self.schedule_at)
        elif isinstance(self.schedule_at, str):
            parsed = _try_parse_iso_to_utc_z(self.schedule_at)
            if parsed is not None:
                self.schedule_at = parsed
        elif self.schedule_at is not None:
            raise TypeError(
                "schedule_at must be a datetime, ISO-8601 string, or None")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        payload: Dict[str, Any] = {}
        if self.status is not None:
            payload['status'] = self.status
        if self.enabled is not None:
            payload['enabled'] = self.enabled
        if self.schedule_at is not None:
            payload['schedule_at'] = self.schedule_at
        if self.comment is not None:
            payload['comment'] = self.comment
        if self.metadata:
            payload['metadata'] = self.metadata

        for k, v in self.extra.items():
            if v is not None and k not in payload:
                payload[k] = v

        return _to_serializable(payload)
