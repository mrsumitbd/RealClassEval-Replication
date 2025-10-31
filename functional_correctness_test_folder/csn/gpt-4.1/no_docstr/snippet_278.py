
import json


class Dumper:

    def dump(self, record, data):
        """
        Serializes the record and data into a JSON string.
        The record is expected to be an object with a __dict__ attribute.
        The data can be any JSON-serializable object.
        """
        payload = {
            'record': record.__dict__,
            'data': data
        }
        return json.dumps(payload)

    def load(self, data, record_cls):
        """
        Deserializes the JSON string back into a tuple (record, data).
        The record is reconstructed as an instance of record_cls.
        """
        payload = json.loads(data)
        record_data = payload['record']
        data_part = payload['data']
        record = record_cls.__new__(record_cls)
        record.__dict__.update(record_data)
        return record, data_part
