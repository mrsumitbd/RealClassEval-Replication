class Deduplicator:
    '''Deduplicates sequences'''

    def _get_sequence_string(self, obj):
        # Try common attribute names for aligned sequence strings
        for attr in (
            'aligned_sequence',
            'aligned_seq',
            'alignment',
            'sequence',
            'seq',
            'sequence_string',
        ):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        pass
                if isinstance(val, (str, bytes)):
                    return val.decode() if isinstance(val, bytes) else val
        # Fallback to str
        return str(obj)

    def _get_name(self, obj):
        # Try common attribute names for identifiers
        for attr in ('name', 'id', 'header', 'label', 'identifier'):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        val = val()
                    except TypeError:
                        pass
                if isinstance(val, (str, bytes)):
                    return val.decode() if isinstance(val, bytes) else val
        # Fallback: try to avoid using the sequence string as name; use repr
        return repr(obj)

    def deduplicate(self, aligned_sequence_objects):
        from collections import OrderedDict

        groups = OrderedDict()
        for obj in aligned_sequence_objects:
            key = self._get_sequence_string(obj)
            if key not in groups:
                groups[key] = []
            groups[key].append(obj)
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
        def lca(list_of_taxa_lists):
            if not list_of_taxa_lists:
                return []
            # Filter out empty taxonomies
            taxa = [t for t in list_of_taxa_lists if t]
            if not taxa:
                return []
            # Compute longest common prefix
            lcp = []
            for level_items in zip(*taxa):
                first = level_items[0]
                if all(item == first for item in level_items[1:]):
                    lcp.append(first)
                else:
                    break
            return lcp

        lcas = []
        for group in deduplicated_sequences:
            taxa_lists = []
            for obj in group:
                name = self._get_name(obj)
                if name in taxonomy_hash:
                    taxa = taxonomy_hash[name]
                    # Ensure list-like of strings
                    if taxa is None:
                        continue
                    if isinstance(taxa, (list, tuple)):
                        taxa_lists.append(list(taxa))
                    else:
                        # If given as string, convert to single-element taxonomy
                        taxa_lists.append([str(taxa)])
            lcas.append(lca(taxa_lists))
        return lcas
