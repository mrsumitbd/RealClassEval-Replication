class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._docs = {}            # doc_id -> doc
        self._indexes = {}         # field -> { value -> set(doc_id) }

    def _doc_id(self, doc):
        return id(doc)

    def _add_to_index(self, doc_id, doc):
        for field, value in doc.items():
            try:
                hash(field)
                hash(value)
            except TypeError:
                continue
            by_value = self._indexes.setdefault(field, {})
            doc_set = by_value.setdefault(value, set())
            doc_set.add(doc_id)

    def _remove_from_index(self, doc_id, doc):
        for field, value in doc.items():
            try:
                hash(field)
                hash(value)
            except TypeError:
                continue
            by_value = self._indexes.get(field)
            if not by_value:
                continue
            doc_set = by_value.get(value)
            if not doc_set:
                continue
            doc_set.discard(doc_id)
            if not doc_set:
                by_value.pop(value, None)
            if by_value and not by_value:
                self._indexes.pop(field, None)
        # Clean up empty field dicts
        empty_fields = [f for f, m in self._indexes.items() if not m]
        for f in empty_fields:
            self._indexes.pop(f, None)

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        doc_id = self._doc_id(doc)
        if doc_id in self._docs:
            self._remove_from_index(doc_id, self._docs[doc_id])
        self._docs[doc_id] = doc
        self._add_to_index(doc_id, doc)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        doc_id = self._doc_id(doc)
        existing = self._docs.get(doc_id)
        if existing is None:
            return
        self._remove_from_index(doc_id, existing)
        self._docs.pop(doc_id, None)

    def reindex(self, old_doc, new_doc):
        '''
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        '''
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        '''
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        '''
        try:
            hash(field)
            hash(value)
        except TypeError:
            return []
        by_value = self._indexes.get(field)
        if not by_value:
            return []
        ids = by_value.get(value)
        if not ids:
            return []
        return [self._docs[i] for i in ids if i in self._docs]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        try:
            hash(field)
        except TypeError:
            return []
        by_value = self._indexes.get(field)
        if not by_value:
            return []
        result_ids = set()
        for v in values:
            try:
                hash(v)
            except TypeError:
                continue
            ids = by_value.get(v)
            if ids:
                result_ids.update(ids)
        return [self._docs[i] for i in result_ids if i in self._docs]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._docs.clear()
        self._indexes.clear()
