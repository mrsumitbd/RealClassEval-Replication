class ExpObject:

    def __init__(self, **kwargs):
        self.lsid = kwargs.pop('lsid', None)
        self.name = kwargs.pop('name', None)
        self.id = kwargs.pop('id', None)
        self.row_id = self.id
        self.comment = kwargs.pop('comment', None)
        self.created = kwargs.pop('created', None)
        self.modified = kwargs.pop('modified', None)
        self.created_by = kwargs.pop('created_by', kwargs.pop('createdBy', None))
        self.modified_by = kwargs.pop('modified_by', kwargs.pop('modifiedBy', None))
        self.properties = kwargs.pop('properties', {})

    def to_json(self):
        data = {'comment': self.comment, 'name': self.name, 'created': self.created, 'createdBy': self.created_by, 'modified': self.modified, 'modifiedBy': self.modified_by, 'properties': self.properties}
        if self.id is not None:
            data.update({'id': self.id})
        if self.lsid is not None:
            data.update({'lsid': self.lsid})
        return data