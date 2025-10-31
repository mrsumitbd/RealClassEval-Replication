from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional, Set, Union
from datetime import datetime


def _safe_get(obj: Any, *keys: str, default: Any = None) -> Any:
    for k in keys:
        if isinstance(obj, dict):
            if k in obj:
                return obj[k]
        else:
            if hasattr(obj, k):
                return getattr(obj, k)
    return default


def _ensure_iterable(value: Any) -> Iterable[str]:
    if value is None:
        return []
    if isinstance(value, (list, set, tuple)):
        return [str(v) for v in value if v is not None]
    return [str(value)]


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_requests: int = 0
    total_duration_ms: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    success_count: int = 0
    error_count: int = 0
    models: Set[str] = field(default_factory=set)
    tools: Set[str] = field(default_factory=set)
    providers: Set[str] = field(default_factory=set)
    first_timestamp: Optional[datetime] = None
    last_timestamp: Optional[datetime] = None

    def add_entry(self, entry: 'UsageEntry') -> None:
        self.total_requests += 1

        # Duration (ms)
        duration_ms = None
        duration_ms = (
            _safe_get(entry, 'duration_ms', 'latency_ms', default=None)
        )
        if duration_ms is None:
            duration = _safe_get(entry, 'duration', 'elapsed', default=None)
            if isinstance(duration, (int, float)):
                # Assume seconds if reasonably small, convert to ms
                duration_ms = duration * 1000.0
        if duration_ms is None:
            # Try timestamps
            start_ts = _safe_get(entry, 'start_time',
                                 'started_at', default=None)
            end_ts = _safe_get(entry, 'end_time', 'ended_at',
                               'finished_at', default=None)
            if start_ts and end_ts:
                try:
                    if isinstance(start_ts, (int, float)) and isinstance(end_ts, (int, float)):
                        duration_ms = max(
                            0.0, (float(end_ts) - float(start_ts)) * 1000.0)
                    else:
                        # Attempt to parse datetimes
                        st = start_ts if isinstance(
                            start_ts, datetime) else datetime.fromisoformat(str(start_ts))
                        et = end_ts if isinstance(
                            end_ts, datetime) else datetime.fromisoformat(str(end_ts))
                        duration_ms = max(
                            0.0, (et - st).total_seconds() * 1000.0)
                except Exception:
                    pass
        if isinstance(duration_ms, (int, float)):
            self.total_duration_ms += float(duration_ms)

        # Tokens
        in_tokens = _safe_get(entry, 'input_tokens',
                              'prompt_tokens', 'request_tokens', default=0) or 0
        out_tokens = _safe_get(
            entry, 'output_tokens', 'completion_tokens', 'response_tokens', default=0) or 0
        total_tokens = _safe_get(entry, 'total_tokens', default=None)
        if isinstance(total_tokens, (int, float)) and not (isinstance(in_tokens, (int, float)) and isinstance(out_tokens, (int, float))):
            # if only total provided, split unknowns as 0 in/out but keep totals
            pass
        if isinstance(in_tokens, (int, float)):
            self.total_input_tokens += int(in_tokens)
        if isinstance(out_tokens, (int, float)):
            self.total_output_tokens += int(out_tokens)
        if isinstance(total_tokens, (int, float)) and not (isinstance(in_tokens, (int, float)) or isinstance(out_tokens, (int, float))):
            # If only total_tokens given, count toward input (conservative)
            self.total_input_tokens += int(total_tokens)

        # Cost
        cost = _safe_get(entry, 'cost', 'price', 'total_cost',
                         'usd_cost', default=0.0) or 0.0
        try:
            self.total_cost += float(cost)
        except Exception:
            pass

        # Success / error
        success = _safe_get(entry, 'success', default=None)
        status = _safe_get(entry, 'status', 'status_code', default=None)
        error = _safe_get(entry, 'error', 'exception', default=None)
        determined_success: Optional[bool] = None
        if isinstance(success, bool):
            determined_success = success
        elif isinstance(status, int):
            determined_success = 200 <= status < 300
        elif error is not None:
            determined_success = False
        if determined_success is True:
            self.success_count += 1
        elif determined_success is False:
            self.error_count += 1

        # Model(s)
        model_values = []
        model_values.extend(_ensure_iterable(
            _safe_get(entry, 'model', default=None)))
        model_values.extend(_ensure_iterable(
            _safe_get(entry, 'models', default=None)))
        for m in model_values:
            if m:
                self.models.add(m)

        # Tool(s)
        tool_values = []
        tool_values.extend(_ensure_iterable(
            _safe_get(entry, 'tool', 'tool_name', default=None)))
        tool_values.extend(_ensure_iterable(
            _safe_get(entry, 'tools', 'tool_names', default=None)))
        for t in tool_values:
            if t:
                self.tools.add(t)

        # Provider(s)
        provider_values = []
        provider_values.extend(_ensure_iterable(
            _safe_get(entry, 'provider', 'service', 'vendor', default=None)))
        providers = _safe_get(entry, 'providers', default=None)
        provider_values.extend(_ensure_iterable(providers))
        for p in provider_values:
            if p:
                self.providers.add(p)

        # Timestamps
        ts_candidates: Iterable[Union[datetime, str, float, int]] = [
            _safe_get(entry, 'timestamp', 'time', 'created_at',
                      'start_time', 'started_at', default=None)
        ]
        for ts in ts_candidates:
            if not ts:
                continue
            try:
                if isinstance(ts, datetime):
                    dt = ts
                elif isinstance(ts, (int, float)):
                    dt = datetime.fromtimestamp(float(ts))
                else:
                    dt = datetime.fromisoformat(str(ts))
                if self.first_timestamp is None or dt < self.first_timestamp:
                    self.first_timestamp = dt
                if self.last_timestamp is None or dt > self.last_timestamp:
                    self.last_timestamp = dt
            except Exception:
                pass

    def to_dict(self) -> Dict[str, Any]:
        total_tokens = self.total_input_tokens + self.total_output_tokens
        return {
            'total_requests': self.total_requests,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'total_duration_ms': self.total_duration_ms,
            'avg_duration_ms': (self.total_duration_ms / self.total_requests) if self.total_requests else 0.0,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': total_tokens,
            'avg_input_tokens': (self.total_input_tokens / self.total_requests) if self.total_requests else 0.0,
            'avg_output_tokens': (self.total_output_tokens / self.total_requests) if self.total_requests else 0.0,
            'avg_total_tokens': (total_tokens / self.total_requests) if self.total_requests else 0.0,
            'total_cost': self.total_cost,
            'avg_cost': (self.total_cost / self.total_requests) if self.total_requests else 0.0,
            'models': sorted(self.models),
            'tools': sorted(self.tools),
            'providers': sorted(self.providers),
            'window_start': self.first_timestamp.isoformat() if self.first_timestamp else None,
            'window_end': self.last_timestamp.isoformat() if self.last_timestamp else None,
        }
