class IndexManager:

    def __init__(self):
        self._next_id = 1
        self._docs_by_id = {}
        self._ids_by_key = {}
        self._index = {}

    def _is_iterable_non_string(self, v):
        return isinstance(v, (list, tuple, set))

    def _freeze(self, v):
        if isinstance(v, dict):
            return tuple(sorted((k, self._freeze(val)) for k, val in v.items()))
        if self._is_iterable_non_string(v):
            return tuple(self._freeze(x) for x in v)
        return v

    def _iter_field_values(self, v):
        if self._is_iterable_non_string(v):
            for x in v:
                yield x
        else:
            yield v

    def _add_to_index(self, doc_id, doc):
        for field, value in doc.items():
            for v in self._iter_field_values(value):
                fv = self._freeze(v)
                self._index.setdefault(field, {}).setdefault(
                    fv, set()).add(doc_id)

    def _remove_from_index(self, doc_id, doc):
        for field, value in doc.items():
            fmap = self._index.get(field)
            if not fmap:
                continue
            for v in self._iter_field_values(value):
                fv = self._freeze(v)
                idset = fmap.get(fv)
                if not idset:
                    continue
                idset.discard(doc_id)
                if not idset:
                    fmap.pop(fv, None)
            if not fmap:
                self._index.pop(field, None)

    def index(self, doc):
        key = self._freeze(doc)
        doc_id = self._next_id
        self._next_id += 1
        self._docs_by_id[doc_id] = doc
        self._ids_by_key.setdefault(key, set()).add(doc_id)
        self._add_to_index(doc_id, doc)
        return doc_id

    def remove(self, doc):
        key = self._freeze(doc)
        ids = self._ids_by_key.get(key)
        if not ids:
            return False
        doc_id = ids.pop()
        if not ids:
            self._ids_by_key.pop(key, None)
        stored = self._docs_by_id.pop(doc_id, None)
        if stored is not None:
            self._remove_from_index(doc_id, stored)
        return True

    def reindex(self, old_doc, new_doc):
        '''
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        '''
        self.remove(old_doc)
        return self.index(new_doc)

    def query(self, field, value):
        '''
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        '''
        fv = self._freeze(value)
        ids = self._index.get(field, {}).get(fv, set())
        return [self._docs_by_id[i] for i in ids]

    def query_in(self, field, values):
        result_ids = set()
        fmap = self._index.get(field, {})
        for v in values:
            fv = self._freeze(v)
            result_ids |= fmap.get(fv, set())
        return [self._docs_by_id[i] for i in result_ids]

    def clear(self):
        self._next_id = 1
        self._docs_by_id.clear()
        self._ids_by_key.clear()
        self._index.clear()
