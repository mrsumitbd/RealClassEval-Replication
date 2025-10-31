
class Deduplicator:
    '''Deduplicates sequences'''

    def deduplicate(self, aligned_sequence_objects):
        deduplicated = {}
        for seq_obj in aligned_sequence_objects:
            sequence = seq_obj.sequence
            if sequence not in deduplicated:
                deduplicated[sequence] = []
            deduplicated[sequence].append(seq_obj)
        return list(deduplicated.values())

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
        def find_lca(taxonomies):
            if not taxonomies:
                return []
            min_length = min(len(tax) for tax in taxonomies)
            for i in range(min_length):
                current_taxon = taxonomies[0][i]
                if not all(tax[i] == current_taxon for tax in taxonomies):
                    return taxonomies[0][:i]
            return taxonomies[0][:min_length]

        lcas = []
        for seq_group in deduplicated_sequences:
            taxonomies = [taxonomy_hash[seq_obj.name] for seq_obj in seq_group]
            lca = find_lca(taxonomies)
            lcas.append(lca)
        return lcas
