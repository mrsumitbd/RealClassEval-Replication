
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EvaluationResult:
    '''
    Result of program evaluation containing both metrics and optional artifacts
    This maintains backward compatibility with the existing dict[str, float] contract
    while adding a side-channel for arbitrary artifacts (text or binary data).
    IMPORTANT: For custom MAP-Elites features, metrics values must be raw continuous
    scores (e.g., actual counts, percentages, continuous measurements), NOT pre-computed
    bin indices. The database handles all binning internally using min-max scaling.
    Examples:
        ✅ Correct: {"combined_score": 0.85, "prompt_length": 1247, "execution_time": 0.234}
        ❌ Wrong:   {"combined_score": 0.85, "prompt_length": 7, "execution_time": 3}
    '''
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        '''Auto-wrap dict returns for backward compatibility'''
        return cls(metrics=metrics)

    def to_dict(self) -> Dict[str, float]:
        '''Backward compatibility - return just metrics'''
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        '''Check if this result contains any artifacts'''
        return bool(self.artifacts)

    def get_artifact_keys(self) -> list:
        return list(self.artifacts.keys()) if self.artifacts else []

    def get_artifact_size(self, key: str) -> int:
        if not self.artifacts or key not in self.artifacts:
            return 0
        value = self.artifacts[key]
        if isinstance(value, (bytes, bytearray)):
            return len(value)
        elif isinstance(value, str):
            return len(value.encode('utf-8'))
        elif hasattr(value, 'read') and hasattr(value, 'seek'):
            # File-like object: get size without changing position
            pos = value.tell()
            value.seek(0, 2)
            size = value.tell()
            value.seek(pos)
            return size
        else:
            # Fallback: try to get size of string representation
            return len(str(value).encode('utf-8'))

    def get_total_artifact_size(self) -> int:
        if not self.artifacts:
            return 0
        return sum(self.get_artifact_size(k) for k in self.artifacts)
