from dataclasses import asdict, dataclass, field, fields
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import time

@dataclass
class Program:
    """Represents a program in the database"""
    id: str
    code: str
    language: str = 'python'
    parent_id: Optional[str] = None
    generation: int = 0
    timestamp: float = field(default_factory=time.time)
    iteration_found: int = 0
    metrics: Dict[str, float] = field(default_factory=dict)
    complexity: float = 0.0
    diversity: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    prompts: Optional[Dict[str, Any]] = None
    artifacts_json: Optional[str] = None
    artifact_dir: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        """Create from dictionary representation"""
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        if len(filtered_data) != len(data):
            filtered_out = set(data.keys()) - set(filtered_data.keys())
            logger.debug(f'Filtered out unsupported fields when loading Program: {filtered_out}')
        return cls(**filtered_data)