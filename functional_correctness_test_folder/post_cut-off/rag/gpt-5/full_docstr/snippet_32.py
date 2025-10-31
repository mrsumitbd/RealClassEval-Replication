from typing import Any, Dict, Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .pricing import PricingCalculator  # adjust import path if needed
    from .timezone import TimezoneHandler   # adjust import path if needed
    from .models import UsageEntry          # adjust import path if needed
    from .enums import CostMode             # adjust import path if needed


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: 'PricingCalculator', timezone_handler: 'TimezoneHandler'):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        '''Map raw data to UsageEntry - compatibility interface.'''
        mapper = globals().get('_map_to_usage_entry')
        if callable(mapper):
            try:
                return mapper(
                    data,
                    mode,
                    pricing_calculator=self.pricing_calculator,
                    timezone_handler=self.timezone_handler,
                )
            except Exception:
                return None
        return None

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict) or not tokens:
            return False

        total = tokens.get('total')
        if isinstance(total, int):
            return total > 0

        # Consider common keys and any positive int value as valid
        valid_any = False
        for v in tokens.values():
            if isinstance(v, int):
                if v < 0:
                    return False
                if v > 0:
                    valid_any = True
            else:
                # Non-int values are ignored for validity, but do not invalidate
                continue
        return valid_any

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        if not isinstance(data, dict):
            return None

        # Common timestamp keys
        candidates = [
            data.get('timestamp'),
            data.get('time'),
            data.get('created'),
            data.get('datetime'),
            data.get('date'),
        ]

        meta = data.get('meta') or data.get('metadata') or {}
        if isinstance(meta, dict):
            candidates.extend([
                meta.get('timestamp'),
                meta.get('time'),
                meta.get('created'),
            ])

        ts_value = next((c for c in candidates if c is not None), None)
        if ts_value is None:
            return None

        try:
            # Numeric epoch (seconds or milliseconds)
            if isinstance(ts_value, (int, float)):
                # Heuristic: treat large numbers as milliseconds
                if ts_value > 1e12:
                    ts_value = ts_value / 1000.0
                dt = datetime.fromtimestamp(float(ts_value), tz=timezone.utc)
                return dt

            # ISO 8601 string
            if isinstance(ts_value, str):
                iso = ts_value.strip()
                if iso.endswith('Z'):
                    iso = iso[:-1] + '+00:00'
                try:
                    dt = datetime.fromisoformat(iso)
                except ValueError:
                    return None
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
        except Exception:
            return None

        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        if not isinstance(data, dict):
            return ''

        # Direct keys
        for key in ('model', 'model_name', 'deployment', 'name'):
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

        # Nested common locations
        request = data.get('request') or {}
        response = data.get('response') or {}
        meta = data.get('meta') or data.get('metadata') or {}

        for container in (request, response, meta):
            if isinstance(container, dict):
                for key in ('model', 'model_name', 'deployment', 'name'):
                    val = container.get(key)
                    if isinstance(val, str) and val.strip():
                        return val.strip()

        return ''

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        if not isinstance(data, dict):
            return {}

        metadata: Dict[str, str] = {}

        # Flatten some commonly expected metadata fields
        candidates = {
            'project_id': data.get('project_id'),
            'project': data.get('project'),
            'user': data.get('user'),
            'organization': data.get('organization') or data.get('org'),
            'request_id': data.get('request_id') or data.get('id'),
            'source': data.get('source'),
            'endpoint': data.get('endpoint'),
            'operation': data.get('operation'),
            'provider': data.get('provider'),
        }

        # Merge nested meta/metadata dicts
        meta = data.get('meta') or data.get('metadata') or {}
        if isinstance(meta, dict):
            for k, v in meta.items():
                # Only include simple string-ish values
                if isinstance(v, (str, int, float, bool)):
                    candidates.setdefault(k, v)

        # Coerce to strings
        for k, v in candidates.items():
            if v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                metadata[k] = str(v)

        return metadata
