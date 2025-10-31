
class Deduplicator:
    '''Deduplicates sequences'''

    def deduplicate(self, aligned_sequence_objects):
        deduplicated_sequences = []
        seen_sequences = set()

        for sequence in aligned_sequence_objects:
            sequence_str = str(sequence)
            if sequence_str not in seen_sequences:
                seen_sequences.add(sequence_str)
                deduplicated_sequences.append([sequence])
            else:
                for group in deduplicated_sequences:
                    if str(group[0]) == sequence_str:
                        group.append(sequence)
                        break

        return deduplicated_sequences

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
        lca_taxonomies = []

        for group in deduplicated_sequences:
            taxonomies = [taxonomy_hash[str(seq)] for seq in group]
            lca = self._find_lca(taxonomies)
            lca_taxonomies.append(lca)

        return lca_taxonomies

    def _find_lca(self, taxonomies):
        if not taxonomies:
            return []

        lca = []
        for i in range(len(taxonomies[0])):
            current_level = taxonomies[0][i]
            for taxonomy in taxonomies[1:]:
                if i >= len(taxonomy) or taxonomy[i] != current_level:
                    return lca
            lca.append(current_level)

        return lca
