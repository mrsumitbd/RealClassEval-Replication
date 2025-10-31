from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Union
from collections import Counter
import numbers

# Assume UsageEntry is defined elsewhere
# from .models import UsageEntry


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    count: int = 0
    totals: Dict[str, float] = field(default_factory=dict)
    by_model: Counter = field(default_factory=Counter)
    by_provider: Counter = field(default_factory=Counter)
    by_endpoint: Counter = field(default_factory=Counter)

    def _iter_fields(self, entry: Union["UsageEntry", Mapping[str, Any]]) -> Dict[str, Any]:
        if isinstance(entry, Mapping):
            return dict(entry)
        # Fallback to vars for objects (e.g., dataclasses)
        try:
            return dict(vars(entry))
        except TypeError:
            # As a last resort, inspect __dict__ if available
            d = getattr(entry, "__dict__", None)
            return dict(d) if isinstance(d, dict) else {}

    def add_entry(self, entry: "UsageEntry") -> None:
        '''Add an entry's statistics to this aggregate.'''
        self.count += 1
        data = self._iter_fields(entry)

        for key, value in data.items():
            # Aggregate numeric fields (exclude booleans)
            if isinstance(value, numbers.Number) and not isinstance(value, bool):
                # Sum into totals
                prev = self.totals.get(key, 0.0)
                self.totals[key] = float(prev) + float(value)

        # Tally common categorical dimensions if present
        model = data.get("model")
        if isinstance(model, str) and model:
            self.by_model[model] += 1

        provider = data.get("provider")
        if isinstance(provider, str) and provider:
            self.by_provider[provider] += 1

        endpoint = data.get("endpoint")
        if isinstance(endpoint, str) and endpoint:
            self.by_endpoint[endpoint] += 1

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format.'''
        out: Dict[str, Any] = {
            "count": self.count,
            "totals": dict(self.totals),
        }
        if self.by_model:
            out["by_model"] = dict(self.by_model)
        if self.by_provider:
            out["by_provider"] = dict(self.by_provider)
        if self.by_endpoint:
            out["by_endpoint"] = dict(self.by_endpoint)
        return out
