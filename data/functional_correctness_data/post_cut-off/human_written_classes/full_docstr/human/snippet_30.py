from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from claude_monitor.core.models import SessionBlock, UsageEntry, normalize_model_name

@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0
    cost: float = 0.0
    count: int = 0

    def add_entry(self, entry: UsageEntry) -> None:
        """Add an entry's statistics to this aggregate."""
        self.input_tokens += entry.input_tokens
        self.output_tokens += entry.output_tokens
        self.cache_creation_tokens += entry.cache_creation_tokens
        self.cache_read_tokens += entry.cache_read_tokens
        self.cost += entry.cost_usd
        self.count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {'input_tokens': self.input_tokens, 'output_tokens': self.output_tokens, 'cache_creation_tokens': self.cache_creation_tokens, 'cache_read_tokens': self.cache_read_tokens, 'cost': self.cost, 'count': self.count}