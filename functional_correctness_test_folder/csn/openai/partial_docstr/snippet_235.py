
class Deduplicator:
    '''Deduplicates sequences'''

    def deduplicate(self, aligned_sequence_objects):
        """
        Group Sequence objects by identical sequence strings.

        Parameters
        ----------
        aligned_sequence_objects : list
            List of Sequence objects. Each object must have a `sequence` attribute.

        Returns
        -------
        list
            List of lists, where each sublist contains Sequence objects that share the same
            sequence string.
        """
        groups = {}
        for seq_obj in aligned_sequence_objects:
            seq_key = getattr(seq_obj, 'sequence', None)
            if seq_key is None:
                # If no sequence attribute, treat each object as unique
                seq_key = id(seq_obj)
            groups.setdefault(seq_key, []).append(seq_obj)
        return list(groups.values())

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        """
        Given a set of deduplicated sequences and a taxonomy hash,
        return the respective LCAs of taxonomy.

        Parameters
        ----------
        deduplicated_sequences : list of lists
            Output from deduplicate(): each sublist contains Sequence objects that are identical.
        taxonomy_hash : dict
            Mapping from sequence names to taxonomy arrays (list of str).

        Returns
        -------
        list
            List of taxonomy LCAs (each LCA is a list of str) corresponding to each group.
        """
        lca_list = []

        for group in deduplicated_sequences:
            # Collect taxonomy arrays for all sequences in the group
            taxonomies = []
            for seq_obj in group:
                name = getattr(seq_obj, 'name', None)
                if name is None:
                    continue
                tax = taxonomy_hash.get(name)
                if tax is not None:
                    taxonomies.append(tax)

            if not taxonomies:
                # No taxonomy information available for this group
                lca_list.append([])
                continue

            # Compute common prefix (LCA) across all taxonomies
            lca = taxonomies[0]
            for tax in taxonomies[1:]:
                # Find common prefix length
                min_len = min(len(lca), len(tax))
                i = 0
                while i < min_len and lca[i] == tax[i]:
                    i += 1
                lca = lca[:i]
                if not lca:
                    break
            lca_list.append(lca)

        return lca_list
