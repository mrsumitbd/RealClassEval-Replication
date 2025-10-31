
class Deduplicator:
    '''Deduplicates sequences'''

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
        # Use a dictionary to group by sequence string
        groups = {}
        for seq_obj in aligned_sequence_objects:
            # Try common attribute names for the sequence string
            seq_str = getattr(seq_obj, 'sequence', None)
            if seq_str is None:
                seq_str = getattr(seq_obj, 'seq', None)
            if seq_str is None:
                raise AttributeError(
                    f"Sequence object {seq_obj} has no 'sequence' or 'seq' attribute"
                )
            groups.setdefault(seq_str, []).append(seq_obj)
        # Return the grouped sequences as a list of lists
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
        lca_list = []
        for group in deduplicated_sequences:
            # Collect taxonomy arrays for each sequence in the group
            taxonomies = []
            for seq_obj in group:
                # Try common attribute names for the sequence name
                name = getattr(seq_obj, 'name', None)
                if name is None:
                    name = getattr(seq_obj, 'id', None)
                if name is None:
                    raise AttributeError(
                        f"Sequence object {seq_obj} has no 'name' or 'id' attribute"
                    )
                tax = taxonomy_hash.get(name, [])
                if not isinstance(tax, list):
                    # Ensure taxonomy is a list
                    tax = list(tax)
                taxonomies.append(tax)

            # Compute lowest common ancestor (common prefix)
            if not taxonomies:
                lca_list.append([])
                continue

            # Find the shortest taxonomy length
            min_len = min(len(t) for t in taxonomies)
            lca = []
            for i in range(min_len):
                # Check if all taxonomies have the same element at position i
                elem = taxonomies[0][i]
                if all(t[i] == elem for t in taxonomies):
                    lca.append(elem)
                else:
                    break
            lca_list.append(lca)
        return lca_list
