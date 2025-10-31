class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._indexes = {}          # field -> { value -> set(doc_ids) }
        self._doc_map = {}          # doc_id -> doc
        self._identity_map = {}     # id(doc) -> doc_id
        # doc_id -> { field -> set(values) } (what we indexed)
        self._doc_fields = {}
        self._next_id = 1

    def _is_hashable(self, v):
        try:
            hash(v)
            return True
        except TypeError:
            return False

    def _normalize_field_values(self, value):
        # Returns a set of hashable values for indexing
        values = set()
        if isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                if self._is_hashable(item):
                    values.add(item)
        elif isinstance(value, dict):
            # Skip dicts by default; not hashable and ambiguous for indexing
            pass
        else:
            if self._is_hashable(value):
                values.add(value)
        return values

    def _compute_index_values(self, doc):
        # Returns a dict: field -> set(values) to index for the given doc
        mapping = {}
        for field, value in doc.items():
            vals = self._normalize_field_values(value)
            if vals:
                mapping[field] = vals
        return mapping

    def _add_index_values(self, doc_id, values_map):
        for field, values in values_map.items():
            field_index = self._indexes.setdefault(field, {})
            for val in values:
                field_index.setdefault(val, set()).add(doc_id)

    def _remove_index_values(self, doc_id, values_map):
        for field, values in values_map.items():
            field_index = self._indexes.get(field)
            if not field_index:
                continue
            for val in values:
                doc_set = field_index.get(val)
                if not doc_set:
                    continue
                doc_set.discard(doc_id)
                if not doc_set:
                    field_index.pop(val, None)
            if not field_index:
                self._indexes.pop(field, None)

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError('doc must be a dictionary')

        identity = id(doc)
        doc_id = self._identity_map.get(identity)

        if doc_id is None:
            doc_id = self._next_id
            self._next_id += 1
            self._doc_map[doc_id] = doc
            self._identity_map[identity] = doc_id
            values_map = self._compute_index_values(doc)
            self._doc_fields[doc_id] = values_map
            self._add_index_values(doc_id, values_map)
        else:
            # Update existing document's index values (document may have mutated)
            old_values_map = self._doc_fields.get(doc_id, {})
            self._remove_index_values(doc_id, old_values_map)
            self._doc_map[doc_id] = doc
            new_values_map = self._compute_index_values(doc)
            self._doc_fields[doc_id] = new_values_map
            self._add_index_values(doc_id, new_values_map)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError('doc must be a dictionary')

        targets = []
        identity = id(doc)
        doc_id = self._identity_map.get(identity)
        if doc_id is not None:
            targets.append(doc_id)
        else:
            # Fallback: remove any documents equal to the provided one
            for did, stored in list(self._doc_map.items()):
                if stored == doc:
                    targets.append(did)

        for did in targets:
            stored = self._doc_map.pop(did, None)
            if stored is None:
                continue
            self._identity_map.pop(id(stored), None)
            values_map = self._doc_fields.pop(did, {})
            self._remove_index_values(did, values_map)

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
        results = []
        # Fast path for hashable values using indexes
        if self._is_hashable(value):
            doc_ids = self._indexes.get(field, {}).get(value, set())
            for did in sorted(doc_ids):
                results.append(self._doc_map[did])
            return results

        # Fallback: linear scan if value is not hashable or complex
        for did, doc in self._doc_map.items():
            if field in doc and doc[field] == value:
                results.append(doc)
        return results

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        if values is None:
            return []

        result_ids = set()
        non_hashable_values = []

        for v in values:
            if self._is_hashable(v):
                doc_ids = self._indexes.get(field, {}).get(v, set())
                result_ids.update(doc_ids)
            else:
                non_hashable_values.append(v)

        # Fallback scan for non-hashable values
        if non_hashable_values:
            for did, doc in self._doc_map.items():
                if field not in doc:
                    continue
                dv = doc[field]
                for v in non_hashable_values:
                    try:
                        matched = False
                        if isinstance(dv, (list, tuple, set, frozenset)):
                            matched = v in dv
                        else:
                            matched = dv == v
                        if matched:
                            result_ids.add(did)
                            break
                    except Exception:
                        continue

        return [self._doc_map[did] for did in sorted(result_ids)]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._indexes.clear()
        self._doc_map.clear()
        self._identity_map.clear()
        self._doc_fields.clear()
        self._next_id = 1
