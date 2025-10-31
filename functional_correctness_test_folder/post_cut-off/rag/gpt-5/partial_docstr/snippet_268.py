class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self.indexes = {}  # field -> {value -> set(doc_ids)}
        self._doc_map = {}  # doc_id -> doc
        self._indexed_pairs = {}  # doc_id -> set of (field, value)

    def _iter_index_values(self, value):
        if isinstance(value, (list, tuple, set)):
            for v in value:
                # Only index hashable values
                if isinstance(v, (str, int, float, bool, type(None), tuple)):
                    yield v
        else:
            if isinstance(value, (str, int, float, bool, type(None), tuple)):
                yield value

    def _build_pairs(self, doc):
        pairs = set()
        if isinstance(doc, dict):
            for field, value in doc.items():
                for v in self._iter_index_values(value):
                    pairs.add((field, v))
        return pairs

    def _unindex_id(self, doc_id):
        pairs = self._indexed_pairs.get(doc_id, set())
        for field, value in pairs:
            field_map = self.indexes.get(field)
            if not field_map:
                continue
            id_set = field_map.get(value)
            if not id_set:
                continue
            id_set.discard(doc_id)
            if not id_set:
                field_map.pop(value, None)
            if not field_map:
                self.indexes.pop(field, None)
        self._indexed_pairs.pop(doc_id, None)

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        doc_id = id(doc)
        # If already indexed (possibly mutated), unindex previous pairs
        if doc_id in self._doc_map:
            self._unindex_id(doc_id)
        pairs = self._build_pairs(doc)
        for field, value in pairs:
            field_map = self.indexes.setdefault(field, {})
            id_set = field_map.setdefault(value, set())
            id_set.add(doc_id)
        self._doc_map[doc_id] = doc
        self._indexed_pairs[doc_id] = pairs

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        doc_id = id(doc)
        if doc_id not in self._doc_map:
            return
        self._unindex_id(doc_id)
        self._doc_map.pop(doc_id, None)

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
        field_map = self.indexes.get(field)
        if not field_map:
            return []
        ids = field_map.get(value, set())
        return [self._doc_map[i] for i in ids if i in self._doc_map]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        field_map = self.indexes.get(field)
        if not field_map or not values:
            return []
        result_ids = set()
        for v in values:
            ids = field_map.get(v)
            if ids:
                result_ids.update(ids)
        return [self._doc_map[i] for i in result_ids if i in self._doc_map]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self.indexes.clear()
        self._doc_map.clear()
        self._indexed_pairs.clear()
