from datetime import datetime
from lpm_kernel.L1.bio import Bio
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class L1GenerationResult:
    """L1 generation result data class"""
    bio: Bio
    clusters: Dict[str, List]
    chunk_topics: Dict[str, Dict]
    generate_time: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary format"""
        return {'bio': self.bio, 'clusters': self.clusters, 'chunk_topics': self.chunk_topics, 'generate_time': self.generate_time.isoformat()}

    @classmethod
    def from_dict(cls, data: dict) -> 'L1GenerationResult':
        """Create instance from dictionary"""
        return cls(bio=data.get('bio'), clusters=data.get('clusters', {'clusterList': []}), chunk_topics=data.get('chunk_topics', {}), generate_time=datetime.fromisoformat(data['generate_time']) if 'generate_time' in data else datetime.now())