
from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        return cls(metrics=metrics)

    def to_dict(self) -> Dict[str, float]:
        return self.metrics

    def has_artifacts(self) -> bool:
        return self.artifacts is not None and len(self.artifacts) > 0

    def get_artifact_keys(self) -> list:
        if not self.has_artifacts():
            return []
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        if not self.has_artifacts() or key not in self.artifacts:
            return 0
        return len(self.artifacts[key])

    def get_total_artifact_size(self) -> int:
        if not self.has_artifacts():
            return 0
        return sum(len(artifact) for artifact in self.artifacts.values())
