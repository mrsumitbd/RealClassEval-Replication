
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        return cls(metrics=metrics)

    def to_dict(self) -> Dict[str, float]:
        return self.metrics

    def has_artifacts(self) -> bool:
        return bool(self.artifacts)

    def get_artifact_keys(self) -> list:
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        artifact = self.artifacts.get(key)
        if artifact is None:
            return 0
        if isinstance(artifact, str):
            return len(artifact.encode('utf-8'))
        elif hasattr(artifact, '__len__'):
            return len(artifact)
        return 0

    def get_total_artifact_size(self) -> int:
        return sum(self.get_artifact_size(key) for key in self.get_artifact_keys())
