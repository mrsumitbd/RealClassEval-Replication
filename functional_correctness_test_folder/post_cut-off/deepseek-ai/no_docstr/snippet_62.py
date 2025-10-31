
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = None
    artifacts: Dict[str, Any] = None

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        return cls(metrics=metrics, artifacts={})

    def to_dict(self) -> Dict[str, float]:
        return self.metrics.copy() if self.metrics else {}

    def has_artifacts(self) -> bool:
        return bool(self.artifacts)

    def get_artifact_keys(self) -> list:
        return list(self.artifacts.keys()) if self.artifacts else []

    def get_artifact_size(self, key: str) -> int:
        if not self.artifacts or key not in self.artifacts:
            return 0
        artifact = self.artifacts[key]
        if isinstance(artifact, bytes):
            return len(artifact)
        elif isinstance(artifact, str):
            return len(artifact.encode('utf-8'))
        else:
            return len(str(artifact).encode('utf-8'))

    def get_total_artifact_size(self) -> int:
        if not self.artifacts:
            return 0
        return sum(self.get_artifact_size(key) for key in self.artifacts)
