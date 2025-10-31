from dataclasses import dataclass, field
from typing import Dict, Union, List


ArtifactType = Union[bytes, bytearray, memoryview, str]


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
    artifacts: Dict[str, ArtifactType] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        '''Auto-wrap dict returns for backward compatibility'''
        if metrics is None:
            return cls()
        conv_metrics: Dict[str, float] = {}
        for k, v in metrics.items():
            try:
                conv_metrics[str(k)] = float(v)
            except Exception as e:
                raise TypeError(
                    f"Metric '{k}' must be a real number, got {type(v).__name__}") from e
        return cls(metrics=conv_metrics)

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
        val = self.artifacts[key]
        if isinstance(val, bytes):
            return len(val)
        if isinstance(val, bytearray):
            return len(val)
        if isinstance(val, memoryview):
            return val.nbytes
        if isinstance(val, str):
            return len(val.encode('utf-8'))
        raise TypeError(
            f"Unsupported artifact type for key '{key}': {type(val).__name__}")

    def get_total_artifact_size(self) -> int:
        '''Get total size of all artifacts in bytes'''
        total = 0
        for k in self.artifacts.keys():
            total += self.get_artifact_size(k)
        return total
