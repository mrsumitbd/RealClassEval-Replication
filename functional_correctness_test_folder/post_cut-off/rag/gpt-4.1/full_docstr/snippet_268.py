class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._doc_map = {}  # doc_id -> doc
        self._indexes = {}  # field -> {value -> set(doc_id)}
        self._next_id = 1   # simple auto-increment doc id

    def _get_doc_id(self, doc):
        # Use id() as fallback if not present, but prefer a stable hash if possible
        return doc.get('_id', None)

    def _assign_doc_id(self, doc):
        if '_id' not in doc:
            doc['_id'] = self._next_id
            self._next_id += 1
        return doc['_id']

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        doc_id = self._assign_doc_id(doc)
        self._doc_map[doc_id] = doc
        for field, value in doc.items():
            if field == '_id':
                continue
            if field not in self._indexes:
                self._indexes[field] = {}
            if isinstance(value, list):
                for v in value:
                    self._indexes[field].setdefault(v, set()).add(doc_id)
            else:
                self._indexes[field].setdefault(value, set()).add(doc_id)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        doc_id = self._get_doc_id(doc)
        if doc_id is None or doc_id not in self._doc_map:
            return
        old_doc = self._doc_map[doc_id]
        for field, value in old_doc.items():
            if field == '_id':
                continue
            if field in self._indexes:
                if isinstance(value, list):
                    for v in value:
                        ids = self._indexes[field].get(v)
                        if ids:
                            ids.discard(doc_id)
                            if not ids:
                                del self._indexes[field][v]
                else:
                    ids = self._indexes[field].get(value)
                    if ids:
                        ids.discard(doc_id)
                        if not ids:
                            del self._indexes[field][value]
                if not self._indexes[field]:
                    del self._indexes[field]
        del self._doc_map[doc_id]

    def reindex(self, old_doc, new_doc):
        '''
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        '''
        old_id = self._get_doc_id(old_doc)
        if old_id is not None:
            self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        '''
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        '''
        if field not in self._indexes:
            return []
        doc_ids = self._indexes[field].get(value, set())
        return [self._doc_map[doc_id] for doc_id in doc_ids]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        if field not in self._indexes:
            return []
        result_ids = set()
        for v in values:
            ids = self._indexes[field].get(v)
            if ids:
                result_ids.update(ids)
        return [self._doc_map[doc_id] for doc_id in result_ids]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._doc_map.clear()
        self._indexes.clear()
        self._next_id = 1
