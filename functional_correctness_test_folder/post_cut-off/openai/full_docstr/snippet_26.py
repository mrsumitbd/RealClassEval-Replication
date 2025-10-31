
from __future__ import annotations

import base64
import datetime
import json
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Tuple, Union


class DataConverter:
    '''Unified data conversion utilities.'''

    @staticmethod
    def flatten_nested_dict(
        data: Dict[str, Any], prefix: str = ''
    ) -> Dict[str, Any]:
        '''Flatten nested dictionary structure.

        Args:
            data: Nested dictionary
            prefix: Prefix for flattened keys

        Returns:
            Flattened dictionary
        '''
        flat: Dict[str, Any] = {}

        def _flatten(current: Any, current_prefix: str) -> None:
            if isinstance(current, dict):
                for k, v in current.items():
                    new_prefix = f'{current_prefix}.{k}' if current_prefix else k
                    _flatten(v, new_prefix)
            elif isinstance(current, (list, tuple)):
                for idx, item in enumerate(current):
                    new_prefix = f'{current_prefix}[{idx}]'
                    _flatten(item, new_prefix)
            else:
                flat[current_prefix] = current

        _flatten(data, prefix)
        return flat

    @staticmethod
    def extract_model_name(
        data: Dict[str, Any], default: str = 'claude-3-5-sonnet'
    ) -> str:
        '''Extract model name from various data sources.

        Args:
            data: Data containing model information
            default: Default model name if not found

        Returns:
            Extracted model name
        '''
        # Common keys that might hold the model name
        candidate_keys = [
            'model',
            'model_name',
            'name',
            'modelId',
            'model_id',
            'modelName',
            'model_name',
            'modelId',
            'model_id',
            'model',
        ]

        def _search(d: Any) -> Union[str, None]:
            if isinstance(d, dict):
                for key, value in d.items():
                    if key.lower() in candidate_keys:
                        if isinstance(value, str):
                            return value
                    # Recurse into nested structures
                    result = _search(value)
                    if result:
                        return result
            elif isinstance(d, (list, tuple)):
                for item in d:
                    result = _search(item)
                    if result:
                        return result
            return None

        name = _search(data)
        return name if name else default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.

        Args:
            obj: Object to convert

        Returns:
            JSON-serializable representation
        '''
        def _convert(o: Any) -> Any:
            if isinstance(o, (str, int, float, bool)) or o is None:
                return o
            if isinstance(o, (datetime.datetime, datetime.date, datetime.time)):
                return o.isoformat()
            if isinstance(o, Decimal):
                return float(o)
            if isinstance(o, bytes):
                return base64.b64encode(o).decode('ascii')
            if isinstance(o, (list, tuple)):
                return [_convert(item) for item in o]
            if isinstance(o, set):
                return [_convert(item) for item in o]
            if isinstance(o, dict):
                return {str(k): _convert(v) for k, v in o.items()}
            # Fallback: try JSON serialization
            try:
                json.dumps(o)
                return o
            except Exception:
                return str(o)

        return _convert(obj)
