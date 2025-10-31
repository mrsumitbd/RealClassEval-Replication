
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
        groups = {}
        for seq_obj in aligned_sequence_objects:
            seq = str(seq_obj)
            if seq not in groups:
                groups[seq] = []
            groups[seq].append(seq_obj)
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
        lca_results = []
        for group in deduplicated_sequences:
            if not group:
                continue
            taxonomies = []
            for seq_obj in group:
                seq_name = seq_obj.name
                if seq_name in taxonomy_hash:
                    taxonomies.append(taxonomy_hash[seq_name])
            if not taxonomies:
                lca_results.append([])
                continue
            min_length = min(len(tax) for tax in taxonomies)
            lca = []
            for i in range(min_length):
                level_taxa = set(tax[i] for tax in taxonomies)
                if len(level_taxa) == 1:
                    lca.append(level_taxa.pop())
                else:
                    break
            lca_results.append(lca)
        return lca_results
