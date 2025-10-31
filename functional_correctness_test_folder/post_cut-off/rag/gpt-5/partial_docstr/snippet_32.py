from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING
from datetime import datetime, timezone
import importlib

if TYPE_CHECKING:
    # These are only for type-checking; actual implementations are provided elsewhere.
    from .pricing import PricingCalculator  # type: ignore
    from .timezone import TimezoneHandler  # type: ignore
    from .types import UsageEntry, CostMode  # type: ignore


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        '''Map raw data to UsageEntry - compatibility interface.'''
        # Attempt to resolve the new functional mapper dynamically.
        func = None
        func = globals().get('_map_to_usage_entry')

        if func is None:
            # Try common module locations without failing hard.
            for mod_name in (
                __name__,  # current module
                'usage_entry_mapper',
                'usage.mapper',
                'mapper',
            ):
                try:
                    mod = importlib.import_module(mod_name)
                    func = getattr(mod, '_map_to_usage_entry', None)
                    if func:
                        break
                except Exception:
                    continue

        if func is None:
            return None

        # Try positional call signature first, then keyword-based as fallback.
        try:
            return func(data, mode, self.pricing_calculator, self.timezone_handler)
        except TypeError:
            try:
                return func(
                    data=data,
                    mode=mode,
                    pricing_calculator=self.pricing_calculator,
                    timezone_handler=self.timezone_handler,
                )
            except Exception:
                return None
        except Exception:
            return None

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict) or not tokens:
            return False
        total = 0
        for v in tokens.values():
            if not isinstance(v, int) or v < 0:
                return False
            total += v
        return total > 0

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        ts = None
        for key in ('timestamp', 'created', 'time', 'ts'):
            if key in data:
                ts = data.get(key)
                break

        if ts is None:
            return None

        # Delegate to timezone handler if it exposes a suitable method.
        try:
            if hasattr(self.timezone_handler, 'to_aware_datetime'):
                # type: ignore[attr-defined]
                return self.timezone_handler.to_aware_datetime(ts)
            if hasattr(self.timezone_handler, 'parse'):
                # type: ignore[attr-defined]
                return self.timezone_handler.parse(ts)
        except Exception:
            pass

        # Fallback parsing.
        if isinstance(ts, (int, float)):
            try:
                return datetime.fromtimestamp(float(ts), tz=timezone.utc)
            except Exception:
                return None

        if isinstance(ts, str):
            try:
                iso = ts.strip()
                if iso.endswith('Z'):
                    iso = iso[:-1] + '+00:00'
                return datetime.fromisoformat(iso)
            except Exception:
                return None

        if isinstance(ts, datetime):
            return ts

        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        # Direct keys
        for key in ('model', 'model_name'):
            if key in data and data[key]:
                return str(data[key])

        # Nested known structures
        for container_key in ('request', 'response', 'metadata', 'config'):
            container = data.get(container_key)
            if isinstance(container, dict):
                for key in ('model', 'model_name'):
                    if key in container and container[key]:
                        return str(container[key])

        # Some providers embed it within usage or params
        for container_key in ('usage', 'params', 'settings'):
            container = data.get(container_key)
            if isinstance(container, dict):
                for key in ('model', 'model_name'):
                    if key in container and container[key]:
                        return str(container[key])

        return ''

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        meta: Dict[str, str] = {}

        # Include explicit metadata dict if present
        if isinstance(data.get('metadata'), dict):
            for k, v in data['metadata'].items():
                meta[str(k)] = '' if v is None else str(v)

        # Common top-level identifiers and context
        for key in (
            'id',
            'request_id',
            'response_id',
            'organization_id',
            'org_id',
            'project_id',
            'user_id',
            'endpoint',
            'provider',
            'type',
            'source',
        ):
            if key in data and data[key] is not None and str(key) not in meta:
                meta[str(key)] = str(data[key])

        # Nested containers that might carry identifiers
        for container_key in ('request', 'response', 'context'):
            container = data.get(container_key)
            if isinstance(container, dict):
                for key in ('id', 'request_id', 'trace_id', 'session_id'):
                    if key in container and container[key] is not None and str(key) not in meta:
                        meta[str(key)] = str(container[key])

        return meta
