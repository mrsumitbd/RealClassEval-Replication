from collections import OrderedDict


class Deduplicator:
    '''Deduplicates sequences'''

    def _get_sequence_str(self, obj):
        # Try common attributes/methods to fetch aligned sequence string
        for attr in ('aligned_sequence', 'sequence', 'seq', 'sequence_string'):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        pass
                if isinstance(val, str):
                    return val
        # Fallback to str(obj)
        return str(obj)

    def _get_name(self, obj):
        for attr in ('name', 'id', 'identifier', 'header', 'label'):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        pass
                if isinstance(val, str):
                    return val
        return str(obj)

    def deduplicate(self, aligned_sequence_objects):
        '''Sort the given aligned_sequence objects into an array of arrays,
        where input sequences are grouped iff they have the same sequence
        Parameters
        ----------
        aligned_sequence_objects: array of Sequence objects
            input sequences
        Returns
        -------
        Array of arrays of Sequence objects'''
        groups = OrderedDict()
        for obj in aligned_sequence_objects or []:
            key = self._get_sequence_str(obj)
            groups.setdefault(key, []).append(obj)
        return list(groups.values())

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        '''Given a set of deduplicated sequences and a taxonomy hash,
        return the respective LCAs of taxonomy
        Parameters
        ----------
        deduplicated_sequences: Array of arrays of Sequence objects
            as output from deduplicate()
        taxonomy_hash: dictionary 
            of sequence names to taxonomy array (i.e. array of str)
        Returns
        -------
        Array of taxonomy LCAs'''
        if not deduplicated_sequences:
            return []

        def lca_of_arrays(arrays):
            if not arrays:
                return []
            # Start with the first taxonomy, then reduce by common prefix
            lca = list(arrays[0])
            for arr in arrays[1:]:
                max_len = min(len(lca), len(arr))
                i = 0
                while i < max_len and lca[i] == arr[i]:
                    i += 1
                lca = lca[:i]
                if not lca:
                    break
            return lca

        results = []
        for group in deduplicated_sequences:
            tax_arrays = []
            for obj in group:
                name = self._get_name(obj)
                if name in taxonomy_hash:
                    tx = taxonomy_hash.get(name)
                    if isinstance(tx, (list, tuple)):
                        tax_arrays.append(list(tx))
            results.append(lca_of_arrays(tax_arrays))
        return results
