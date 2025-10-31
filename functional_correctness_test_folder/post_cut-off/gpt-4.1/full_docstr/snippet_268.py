
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
        self._next_id = 1   # unique doc id generator

    def _get_doc_id(self, doc):
        # Use id() for uniqueness, but to allow for doc copies, use a hidden _im_id
        if '_im_id' in doc:
            return doc['_im_id']
        else:
            doc_id = self._next_id
            self._next_id += 1
            doc['_im_id'] = doc_id
            return doc_id

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        doc_id = self._get_doc_id(doc)
        if doc_id in self._doc_map:
            return  # Already indexed
        self._doc_map[doc_id] = doc
        for field, value in doc.items():
            if field == '_im_id':
                continue
            if field not in self._indexes:
                self._indexes[field] = {}
            if value not in self._indexes[field]:
                self._indexes[field][value] = set()
            self._indexes[field][value].add(doc_id)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        doc_id = doc.get('_im_id')
        if doc_id is None or doc_id not in self._doc_map:
            return
        old_doc = self._doc_map[doc_id]
        for field, value in old_doc.items():
            if field == '_im_id':
                continue
            if field in self._indexes and value in self._indexes[field]:
                self._indexes[field][value].discard(doc_id)
                if not self._indexes[field][value]:
                    del self._indexes[field][value]
                if not self._indexes[field]:
                    del self._indexes[field]
        del self._doc_map[doc_id]
        # Optionally, remove _im_id from doc
        # doc.pop('_im_id', None)

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
        if field in self._indexes and value in self._indexes[field]:
            doc_ids = self._indexes[field][value]
            return [self._doc_map[doc_id] for doc_id in doc_ids]
        return []

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        result_ids = set()
        if field in self._indexes:
            for value in values:
                if value in self._indexes[field]:
                    result_ids.update(self._indexes[field][value])
        return [self._doc_map[doc_id] for doc_id in result_ids]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._doc_map.clear()
        self._indexes.clear()
        self._next_id = 1
