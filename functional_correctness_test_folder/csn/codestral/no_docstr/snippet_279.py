
class SearchDumperExt:

    def dump(self, record, data):

        data['id'] = record.id
        data['name'] = record.name
        data['description'] = record.description
        data['created_at'] = record.created_at.isoformat()
        data['updated_at'] = record.updated_at.isoformat()

    def load(self, data, record_cls):

        record = record_cls()
        record.id = data['id']
        record.name = data['name']
        record.description = data['description']
        record.created_at = datetime.fromisoformat(data['created_at'])
        record.updated_at = datetime.fromisoformat(data['updated_at'])
        return record
