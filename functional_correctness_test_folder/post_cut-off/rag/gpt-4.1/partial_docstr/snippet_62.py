from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


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
        return bool(self.artifacts) and len(self.artifacts) > 0

    def get_artifact_keys(self) -> list:
        '''Get list of artifact keys'''
        if self.artifacts:
            return list(self.artifacts.keys())
        return []

    def get_artifact_size(self, key: str) -> int:
        '''Get size of a specific artifact in bytes'''
        if not self.artifacts or key not in self.artifacts:
            return 0
        value = self.artifacts[key]
        if isinstance(value, bytes):
            return len(value)
        elif isinstance(value, str):
            return len(value.encode('utf-8'))
        else:
            # Try to serialize to bytes if possible
            try:
                import pickle
                return len(pickle.dumps(value))
            except Exception:
                return 0

    def get_total_artifact_size(self) -> int:
        '''Get total size of all artifacts in bytes'''
        if not self.artifacts:
            return 0
        return sum(self.get_artifact_size(k) for k in self.artifacts)
