from typing import Any, Dict, Optional
from datetime import datetime, timezone


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
        func = globals().get('_map_to_usage_entry')
        if not callable(func):
            return None

        attempts = [
            # Keyword-first attempt (most explicit)
            {'kwargs': {'data': data, 'mode': mode, 'pricing_calculator': self.pricing_calculator,
                        'timezone_handler': self.timezone_handler}},
            # Common positional permutations
            {'args': (data, mode, self.pricing_calculator,
                      self.timezone_handler)},
            {'args': (self.pricing_calculator,
                      self.timezone_handler, data, mode)},
            {'args': (data, self.pricing_calculator,
                      self.timezone_handler, mode)},
            {'args': (self.pricing_calculator, data,
                      mode, self.timezone_handler)},
            # Fallbacks with fewer params
            {'args': (data, mode, self.pricing_calculator)},
            {'kwargs': {'data': data, 'mode': mode}},
            {'args': (data, mode)},
        ]

        for attempt in attempts:
            try:
                if 'kwargs' in attempt:
                    return func(**attempt['kwargs'])
                if 'args' in attempt:
                    return func(*attempt['args'])
            except TypeError:
                continue
            except Exception:
                return None
        return None

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not tokens or not isinstance(tokens, dict):
            return False
        for key in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
            val = tokens.get(key)
            if isinstance(val, int) and val >= 0:
                return True
        return False

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        def find_timestamp(d: Dict[str, Any]) -> Any:
            for k in ('timestamp', 'created_at', 'created', 'time', 'datetime', 'ts'):
                if k in d:
                    return d.get(k)
            # Nested common locations
            for a, b in (('usage', 'timestamp'), ('meta', 'timestamp'), ('response', 'created'), ('request', 'created')):
                if isinstance(d.get(a), dict) and b in d[a]:
                    return d[a][b]
            return None

        raw = find_timestamp(data)
        if raw is None:
            return None

        # Delegate to timezone handler if possible
        for method_name in ('to_datetime', 'parse', 'parse_datetime'):
            method = getattr(self.timezone_handler, method_name, None)
            if callable(method):
                try:
                    dt = method(raw)
                    if isinstance(dt, datetime):
                        return dt
                except Exception:
                    pass

        # Fallback parsing
        if isinstance(raw, datetime):
            if raw.tzinfo is None:
                localize = getattr(self.timezone_handler, 'localize', None)
                if callable(localize):
                    try:
                        return localize(raw)
                    except Exception:
                        pass
                return raw.replace(tzinfo=timezone.utc)
            return raw

        if isinstance(raw, (int, float)):
            try:
                return datetime.fromtimestamp(raw, tz=timezone.utc)
            except Exception:
                return None

        if isinstance(raw, str):
            s = raw.strip()
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            try:
                return datetime.fromisoformat(s)
            except Exception:
                # Try numeric string epoch
                try:
                    if '.' in s:
                        return datetime.fromtimestamp(float(s), tz=timezone.utc)
                    return datetime.fromtimestamp(int(s), tz=timezone.utc)
                except Exception:
                    return None

        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        for key in ('model', 'model_name'):
            val = data.get(key)
            if val is not None:
                return str(val)

        for a, b in (('request', 'model'), ('response', 'model'), ('metadata', 'model'), ('meta', 'model')):
            container = data.get(a)
            if isinstance(container, dict) and b in container and container[b] is not None:
                return str(container[b])

        return ''

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        result: Dict[str, str] = {}
        md = data.get('metadata') or data.get('meta')
        if isinstance(md, dict):
            for k, v in md.items():
                if v is not None:
                    result[str(k)] = str(v)

        # Promote some common fields into metadata if present
        candidates = [
            'request_id', 'id', 'user', 'user_id', 'project', 'project_id',
            'organization', 'org', 'endpoint', 'provider', 'source', 'mode',
        ]
        for k in candidates:
            if k in data and data[k] is not None and str(k) not in result:
                result[k] = str(data[k])

        # Nested common locations
        nested_candidates = [
            ('headers', 'x-request-id'),
            ('request', 'id'),
            ('response', 'id'),
        ]
        for a, b in nested_candidates:
            container = data.get(a)
            if isinstance(container, dict) and b in container and container[b] is not None:
                key = f'{a}.{b}'
                if key not in result:
                    result[key] = str(container[b])

        return result
