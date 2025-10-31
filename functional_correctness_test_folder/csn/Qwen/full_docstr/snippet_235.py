
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
        for seq_obj in aligned_sequence_objects:
            sequence = seq_obj.sequence
            if sequence not in sequence_dict:
                sequence_dict[sequence] = []
            sequence_dict[sequence].append(seq_obj)
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
        def find_lca(taxonomies):
            min_length = min(len(tax) for tax in taxonomies)
            for i in range(min_length):
                current_taxon = taxonomies[0][i]
                if all(tax[i] == current_taxon for tax in taxonomies):
                    continue
                return taxonomies[0][:i]
            return taxonomies[0][:min_length]

        lcas = []
        for group in deduplicated_sequences:
            taxonomies = [taxonomy_hash[seq_obj.name] for seq_obj in group]
            lca = find_lca(taxonomies)
            lcas.append(lca)
        return lcas
