
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        return cls(metrics=metrics)

    def to_dict(self) -> Dict[str, float]:
        return self.metrics.copy()

    def has_artifacts(self) -> bool:
        return bool(self.artifacts)

    def get_artifact_keys(self) -> List[str]:
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        return len(self.artifacts[key]) if key in self.artifacts else 0

    def get_total_artifact_size(self) -> int:
        return sum(len(artifact) for artifact in self.artifacts.values())
