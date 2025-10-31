
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, bytes] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        return cls(metrics=metrics)

    def to_dict(self) -> Dict[str, float]:
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        return bool(self.artifacts)

    def get_artifact_keys(self) -> list:
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        if key not in self.artifacts:
            raise KeyError(f"Artifact key '{key}' not found.")
        return len(self.artifacts[key])

    def get_total_artifact_size(self) -> int:
        return sum(len(data) for data in self.artifacts.values())
