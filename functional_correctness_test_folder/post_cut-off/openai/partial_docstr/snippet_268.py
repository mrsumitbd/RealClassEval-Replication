
class IndexManager:
    def __init__(self):
        # Mapping from document id to the document itself
        self._docs = {}
        # Inverted index: field -> value -> set of document ids
        self._index = {}

    def index(self, doc):
        """Add a document to the index."""
        doc_id = id(doc)
        if doc_id in self._docs:
            return  # already indexed
        self._docs[doc_id] = doc
        for field, value in doc.items():
            self._index.setdefault(field, {}).setdefault(
                value, set()).add(doc_id)

    def remove(self, doc):
        """Remove a document from the index."""
        doc_id = id(doc)
        if doc_id not in self._docs:
            return
        # Remove from inverted index
        for field, value in self._docs[doc_id].items():
            ids = self._index.get(field, {}).get(value)
            if ids:
                ids.discard(doc_id)
                if not ids:
                    del self._index[field][value]
                    if not self._index[field]:
                        del self._index[field]
        # Remove from docs
        del self._docs[doc_id]

    def reindex(self, old_doc, new_doc):
        """
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        """
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        """
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        """
        ids = self._index.get(field, {}).get(value, set())
        return [self._docs[doc_id] for doc_id in ids]

    def query_in(self, field, values):
        """Return documents where the field's value is in the provided iterable."""
        result_ids = set()
        field_index = self._index.get(field, {})
        for val in values:
            ids = field_index.get(val)
            if ids:
                result_ids.update(ids)
        return [self._docs[doc_id] for doc_id in result_ids]

    def clear(self):
        """Clear the entire index."""
        self._docs.clear()
        self._index.clear()
