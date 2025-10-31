
from collections import defaultdict


class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        # Map from document id to the document itself
        self._doc_map = {}
        # Nested dict: field -> value -> set of document ids
        self._indexes = defaultdict(lambda: defaultdict(set))

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError("Document must be a dict")
        doc_id = id(doc)
        # If already indexed, remove old entry first
        if doc_id in self._doc_map:
            self.remove(doc)
        self._doc_map[doc_id] = doc
        for field, value in doc.items():
            # Only index hashable values
            try:
                hash(value)
            except TypeError:
                continue
            self._indexes[field][value].add(doc_id)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        doc_id = id(doc)
        if doc_id not in self._doc_map:
            return
        # Remove from indexes
        for field, value in self._doc_map[doc_id].items():
            try:
                hash(value)
            except TypeError:
                continue
            ids_set = self._indexes[field].get(value)
            if ids_set:
                ids_set.discard(doc_id)
                if not ids_set:
                    del self._indexes[field][value]
        # Remove from doc map
        del self._doc_map[doc_id]

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
        ids = self._indexes.get(field, {}).get(value, set())
        return [self._doc_map[doc_id] for doc_id in ids]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        result_ids = set()
        field_index = self._indexes.get(field, {})
        for value in values:
            result_ids.update(field_index.get(value, set()))
        return [self._doc_map[doc_id] for doc_id in result_ids]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._doc_map.clear()
        self._indexes.clear()
