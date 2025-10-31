class IndexManager:

    def __init__(self):
        self._docs = {}  # doc_key -> doc
        self._index = {}  # field -> value -> set(doc_key)

    def _doc_key(self, doc):
        try:
            if isinstance(doc, dict) and 'id' in doc and self._is_hashable(doc['id']):
                return ('id', doc['id'])
        except Exception:
            pass
        return ('obj', id(doc))

    def _is_hashable(self, v):
        try:
            hash(v)
            return True
        except TypeError:
            return False

    def _values_to_index(self, value):
        if isinstance(value, (list, tuple, set)):
            for v in value:
                if self._is_hashable(v):
                    yield v
        else:
            if self._is_hashable(value):
                yield value

    def _add_to_index(self, doc_key, doc):
        if not isinstance(doc, dict):
            return
        for field, value in doc.items():
            for v in self._values_to_index(value):
                self._index.setdefault(field, {}).setdefault(
                    v, set()).add(doc_key)

    def _remove_from_index(self, doc_key, doc):
        if not isinstance(doc, dict):
            return
        for field, value in doc.items():
            field_map = self._index.get(field)
            if not field_map:
                continue
            for v in self._values_to_index(value):
                docs_set = field_map.get(v)
                if not docs_set:
                    continue
                docs_set.discard(doc_key)
                if not docs_set:
                    field_map.pop(v, None)
            if not field_map:
                self._index.pop(field, None)

    def index(self, doc):
        key = self._doc_key(doc)
        existing = self._docs.get(key)
        if existing is not None:
            self._remove_from_index(key, existing)
        self._docs[key] = doc
        self._add_to_index(key, doc)

    def remove(self, doc):
        key = self._doc_key(doc)
        existing = self._docs.get(key)
        if existing is None:
            return False
        self._remove_from_index(key, existing)
        self._docs.pop(key, None)
        return True

    def reindex(self, old_doc, new_doc):
        old_key = self._doc_key(old_doc)
        if old_key in self._docs:
            self._remove_from_index(old_key, self._docs[old_key])
            self._docs.pop(old_key, None)
        self.index(new_doc)

    def query(self, field, value):
        res = []
        field_map = self._index.get(field, {})
        keys = field_map.get(value, set())
        for k in keys:
            doc = self._docs.get(k)
            if doc is not None:
                res.append(doc)
        return res

    def query_in(self, field, values):
        res_keys = set()
        field_map = self._index.get(field, {})
        for v in values:
            keys = field_map.get(v)
            if keys:
                res_keys.update(keys)
        return [self._docs[k] for k in res_keys if k in self._docs]

    def clear(self):
        self._docs.clear()
        self._index.clear()
