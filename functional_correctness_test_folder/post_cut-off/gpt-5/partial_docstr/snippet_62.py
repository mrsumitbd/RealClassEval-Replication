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
    artifacts: Dict[str, Union[str, bytes, bytearray,
                               memoryview]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        '''Auto-wrap dict returns for backward compatibility'''
        return cls(metrics=dict(metrics or {}), artifacts={})

    def to_dict(self) -> Dict[str, float]:
        '''Backward compatibility - return just metrics'''
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        '''Check if this result contains any artifacts'''
        return bool(self.artifacts)

    def get_artifact_keys(self) -> List[str]:
        return list(self.artifacts.keys())

    def _artifact_size_bytes(self, value: Any) -> int:
        if isinstance(value, (bytes, bytearray, memoryview)):
            return len(value)
        if isinstance(value, str):
            return len(value.encode('utf-8'))
        # Fallback: stringify and encode
        return len(str(value).encode('utf-8'))

    def get_artifact_size(self, key: str) -> int:
        if key not in self.artifacts:
            raise KeyError(f"Artifact not found: {key}")
        return self._artifact_size_bytes(self.artifacts[key])

    def get_total_artifact_size(self) -> int:
        return sum(self._artifact_size_bytes(v) for v in self.artifacts.values())
