
class SearchDumperExt:

    def dump(self, record, data):
        data['record_id'] = record.id
        data['record_name'] = record.name
        data['record_value'] = record.value

    def load(self, data, record_cls):
        return record_cls(
            id=data['record_id'],
            name=data['record_name'],
            value=data['record_value']
        )
