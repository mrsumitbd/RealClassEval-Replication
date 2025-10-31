
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
        from collections import defaultdict
        seq_groups = defaultdict(list)
        for seq_obj in aligned_sequence_objects:
            seq_groups[seq_obj.sequence].append(seq_obj)
        return list(seq_groups.values())

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
        def lca(taxa_lists):
            if not taxa_lists:
                return []
            min_len = min(len(t) for t in taxa_lists)
            lca_result = []
            for i in range(min_len):
                ith_level = [t[i] for t in taxa_lists]
                if all(x == ith_level[0] for x in ith_level):
                    lca_result.append(ith_level[0])
                else:
                    break
            return lca_result

        lca_list = []
        for group in deduplicated_sequences:
            taxa_lists = []
            for seq_obj in group:
                name = seq_obj.name
                if name in taxonomy_hash:
                    taxa_lists.append(taxonomy_hash[name])
            lca_list.append(lca(taxa_lists))
        return lca_list
