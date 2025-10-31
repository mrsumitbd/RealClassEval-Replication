
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
        sequence_dict = {}
        for seq in aligned_sequence_objects:
            sequence = seq.sequence
            if sequence not in sequence_dict:
                sequence_dict[sequence] = []
            sequence_dict[sequence].append(seq)
        return list(sequence_dict.values())

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
        for seq_group in deduplicated_sequences:
            taxonomies = [taxonomy_hash[seq.name] for seq in seq_group]
            lca = self._find_lca(taxonomies)
            lca_taxonomies.append(lca)
        return lca_taxonomies

    def _find_lca(self, taxonomies):
        '''Find the lowest common ancestor (LCA) of a list of taxonomies'''
        if not taxonomies:
            return []
        lca = taxonomies[0]
        for taxonomy in taxonomies[1:]:
            lca = [taxon for i, taxon in enumerate(
                lca) if i < len(taxonomy) and taxon == taxonomy[i]]
        return lca
