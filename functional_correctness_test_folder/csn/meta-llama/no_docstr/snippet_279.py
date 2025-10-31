
import json


class SearchDumperExt:

    def dump(self, record, data):
        """Dumps the given record into a JSON string."""
        record_data = {
            'id': record.id,
            'data': data
        }
        return json.dumps(record_data)

    def load(self, data, record_cls):
        """Loads a record from the given JSON data."""
        try:
            record_data = json.loads(data)
            record = record_cls(id=record_data['id'])
            return record, record_data['data']
        except (json.JSONDecodeError, KeyError, TypeError):
            return None, None
