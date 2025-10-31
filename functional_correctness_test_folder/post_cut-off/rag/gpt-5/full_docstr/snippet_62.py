from dataclasses import dataclass, field
from typing import Dict, Union, List, Any


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
    artifacts: Dict[str, Union[bytes, bytearray, memoryview, str]] = field(
        default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        '''Auto-wrap dict returns for backward compatibility'''
        return cls(metrics=dict(metrics or {}))

    def to_dict(self) -> Dict[str, float]:
        '''Backward compatibility - return just metrics'''
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        '''Check if this result contains any artifacts'''
        return bool(self.artifacts)

    def get_artifact_keys(self) -> List[str]:
        '''Get list of artifact keys'''
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        '''Get size of a specific artifact in bytes'''
        if key not in self.artifacts:
            raise KeyError(f"Artifact '{key}' not found")
        return self._calc_size(self.artifacts[key])

    def get_total_artifact_size(self) -> int:
        '''Get total size of all artifacts in bytes'''
        return sum(self._calc_size(v) for v in self.artifacts.values())

    @staticmethod
    def _calc_size(value: Any) -> int:
        if value is None:
            return 0
        if isinstance(value, str):
            return len(value.encode('utf-8', errors='replace'))
        if isinstance(value, (bytes, bytearray)):
            return len(value)
        if isinstance(value, memoryview):
            return value.nbytes
        try:
            mv = memoryview(value)  # for other buffer-protocol types
            return mv.nbytes
        except Exception:
            return len(str(value).encode('utf-8', errors='replace'))
