
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class EvaluationResult:
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, bytes] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, metrics: Dict[str, float]) -> 'EvaluationResult':
        """Create an EvaluationResult from a metrics dictionary."""
        return cls(metrics=dict(metrics))

    def to_dict(self) -> Dict[str, float]:
        """Return the metrics dictionary."""
        return dict(self.metrics)

    def has_artifacts(self) -> bool:
        """Return True if any artifacts are present."""
        return bool(self.artifacts)

    def get_artifact_keys(self) -> List[str]:
        """Return a list of artifact keys."""
        return list(self.artifacts.keys())

    def get_artifact_size(self, key: str) -> int:
        """Return the size in bytes of the artifact identified by key."""
        if key not in self.artifacts:
            raise KeyError(f"Artifact key '{key}' not found.")
        return len(self.artifacts[key])

    def get_total_artifact_size(self) -> int:
        """Return the total size in bytes of all artifacts."""
        return sum(len(data) for data in self.artifacts.values())
