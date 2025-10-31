from dataclasses import dataclass, field, is_dataclass, asdict
from typing import Any, Dict, Mapping, Iterable


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if not isinstance(self.attributes, dict):
            raise TypeError("attributes must be a dictionary")
        self.attributes = self._sanitize(self.attributes)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return self._sanitize(self.attributes)

    @classmethod
    def _serialize(cls, value: Any) -> Any:
        if value is None:
            return None
        if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
            return cls._serialize(value.to_dict())
        if is_dataclass(value):
            return cls._serialize(asdict(value))
        if isinstance(value, Mapping):
            return {str(k): cls._serialize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [cls._serialize(v) for v in value]
        return value

    @classmethod
    def _sanitize(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        serialized = cls._serialize(payload)
        # remove keys with None values recursively

        def prune_none(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: prune_none(v) for k, v in obj.items() if v is not None}
            if isinstance(obj, list):
                return [prune_none(v) for v in obj if v is not None]
            return obj
        return prune_none(serialized)
