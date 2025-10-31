class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._indexes = {}  # field -> { frozen_value -> set(doc_id) }
        self._docs = {}  # doc_id -> doc
        self._doc_field_keys = {}  # doc_id -> { field -> frozen_value }

    @staticmethod
    def _freeze(value):
        try:
            hash(value)
            return value
        except TypeError:
            pass

        if isinstance(value, dict):
            items = tuple(sorted(((IndexManager._freeze(k), IndexManager._freeze(
                v)) for k, v in value.items()), key=repr))
            return ('__dict__', items)
        if isinstance(value, (list, tuple)):
            items = tuple(IndexManager._freeze(v) for v in value)
            tag = '__list__' if isinstance(value, list) else '__tuple__'
            return (tag, items)
        if isinstance(value, set):
            items = tuple(sorted((IndexManager._freeze(v)
                          for v in value), key=repr))
            return ('__set__', items)
        return ('__repr__', repr(value))

    def _prune_empty(self, field, frozen_value):
        value_map = self._indexes.get(field)
        if not value_map:
            return
        value_set = value_map.get(frozen_value)
        if value_set is not None and not value_set:
            del value_map[frozen_value]
        if not value_map:
            del self._indexes[field]

    def _purge_docid(self, doc_id):
        for field, value_map in list(self._indexes.items()):
            for frozen_value, id_set in list(value_map.items()):
                if doc_id in id_set:
                    id_set.discard(doc_id)
                    if not id_set:
                        del value_map[frozen_value]
            if not value_map:
                del self._indexes[field]

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError('Document must be a dictionary')
        doc_id = id(doc)
        # If already indexed, remove first to reindex
        if doc_id in self._docs:
            self.remove(doc)
        self._docs[doc_id] = doc
        field_keys = {}
        for field, value in doc.items():
            frozen_value = self._freeze(value)
            field_keys[field] = frozen_value
            field_index = self._indexes.setdefault(field, {})
            id_set = field_index.setdefault(frozen_value, set())
            id_set.add(doc_id)
        self._doc_field_keys[doc_id] = field_keys

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError('Document must be a dictionary')
        doc_id = id(doc)
        if doc_id not in self._docs:
            return
        field_keys = self._doc_field_keys.pop(doc_id, None)
        if field_keys is None:
            self._purge_docid(doc_id)
        else:
            for field, frozen_value in field_keys.items():
                value_map = self._indexes.get(field)
                if not value_map:
                    continue
                id_set = value_map.get(frozen_value)
                if id_set:
                    id_set.discard(doc_id)
                    if not id_set:
                        del value_map[frozen_value]
                if not value_map:
                    del self._indexes[field]
        del self._docs[doc_id]

    def reindex(self, old_doc, new_doc):
        '''
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        '''
        self.remove(old_doc)
        self.index(new_doc)

    def _iter_docs_by_order(self, doc_ids):
        for did in self._docs:
            if did in doc_ids:
                yield self._docs[did]

    def query(self, field, value):
        '''
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        '''
        frozen_value = self._freeze(value)
        id_set = self._indexes.get(field, {}).get(frozen_value, set())
        return list(self._iter_docs_by_order(id_set))

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        result_ids = set()
        field_map = self._indexes.get(field, {})
        for value in values:
            frozen_value = self._freeze(value)
            result_ids |= field_map.get(frozen_value, set())
        return list(self._iter_docs_by_order(result_ids))

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._indexes.clear()
        self._docs.clear()
        self._doc_field_keys.clear()
