
from typing import Any, Dict


class DataConverter:
    '''Unified data conversion utilities.'''

    @staticmethod
    def flatten_nested_dict(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        def _flatten(d, parent_key):
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(_flatten(v, new_key))
                else:
                    items[new_key] = v
            return items
        return _flatten(data, prefix)

    @staticmethod
    def extract_model_name(data: Dict[str, Any], default: str = 'claude-3-5-sonnet') -> str:
        '''Extract model name from various data sources.'''
        # Common possible keys for model name
        keys = [
            'model', 'model_name', 'modelName', 'model_id', 'modelId',
            'name', 'engine', 'engine_id', 'engineId'
        ]
        for key in keys:
            if key in data and isinstance(data[key], str):
                return data[key]
        # Try nested dicts
        for v in data.values():
            if isinstance(v, dict):
                name = DataConverter.extract_model_name(v, default=None)
                if name:
                    return name
        return default

    @staticmethod
    def to_serializable(obj: Any) -> Any:
        '''Convert object to JSON-serializable format.'''
        import datetime
        import decimal

        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, dict):
            return {DataConverter.to_serializable(k): DataConverter.to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [DataConverter.to_serializable(i) for i in obj]
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif hasattr(obj, '__dict__'):
            return DataConverter.to_serializable(obj.__dict__)
        elif hasattr(obj, '__slots__'):
            return {slot: DataConverter.to_serializable(getattr(obj, slot)) for slot in obj.__slots__}
        else:
            return str(obj)
