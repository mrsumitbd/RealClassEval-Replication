
class IndexManager:
    def __init__(self):
        # Mapping from field -> value -> set of doc ids
        self._index = {}
        # Mapping from doc id -> doc object
        self._docs = {}

    def index(self, doc):
        """Add a document to the index."""
        doc_id = id(doc)
        if doc_id in self._docs:
            # Already indexed; ignore or update?
            return
        self._docs[doc_id] = doc
        # Assume doc is a mapping (dict-like)
        for field, value in doc.items():
            self._index.setdefault(field, {}).setdefault(
                value, set()).add(doc_id)

    def remove(self, doc):
        """Remove a document from the index."""
        doc_id = id(doc)
        if doc_id not in self._docs:
            return
        # Remove from field/value index
        for field, value in self._docs[doc_id].items():
            val_map = self._index.get(field)
            if val_map:
                id_set = val_map.get(value)
                if id_set:
                    id_set.discard(doc_id)
                    if not id_set:
                        del val_map[value]
                if not val_map:
                    del self._index[field]
        # Remove from docs
        del self._docs[doc_id]

    def reindex(self, old_doc, new_doc):
        """Replace old_doc with new_doc in the index."""
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        """Return a list of documents where doc[field] == value."""
        result = []
        val_map = self._index.get(field, {})
        id_set = val_map.get(value, set())
        for doc_id in id_set:
            result.append(self._docs[doc_id])
        return result

    def query_in(self, field, values):
        """Return a list of documents where doc[field] is in values."""
        result_set = set()
        val_map = self._index.get(field, {})
        for value in values:
            id_set = val_map.get(value)
            if id_set:
                result_set.update(id_set)
        return [self._docs[doc_id] for doc_id in result_set]

    def clear(self):
        """Clear the entire index."""
        self._index.clear()
        self._docs.clear()
