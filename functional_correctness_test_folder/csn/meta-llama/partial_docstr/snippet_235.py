
from collections import Counter


class Deduplicator:
    '''Deduplicates sequences'''

    def deduplicate(self, aligned_sequence_objects):
        """Deduplicate a list of aligned sequence objects.

        Parameters
        ----------
        aligned_sequence_objects: list of Sequence objects

        Returns
        -------
        list of lists of Sequence objects
            where each sublist contains Sequence objects with identical sequences
        """
        sequence_dict = {}
        for sequence in aligned_sequence_objects:
            sequence_str = str(sequence)
            if sequence_str not in sequence_dict:
                sequence_dict[sequence_str] = []
            sequence_dict[sequence_str].append(sequence)
        return list(sequence_dict.values())

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        '''Given a set of deduplicated sequences and a taxonomy hash,
        return the respective LCAs of taxonomy

        Parameters
        ----------
        deduplicated_sequences: list of lists of Sequence objects
            as output from deduplicate()
        taxonomy_hash: dictionary 
            of sequence names to taxonomy array (i.e. array of str)

        Returns
        -------
        list of taxonomy LCAs
        '''
        lcas = []
        for sequences in deduplicated_sequences:
            taxonomies = [taxonomy_hash.get(seq.name, []) for seq in sequences]
            lca = self._lca(taxonomies)
            lcas.append(lca)
        return lcas

    @staticmethod
    def _lca(taxonomies):
        """Compute the LCA of a list of taxonomies.

        Parameters
        ----------
        taxonomies: list of lists of str

        Returns
        -------
        list of str
            the LCA taxonomy
        """
        if not taxonomies:
            return []

        lca = []
        for ranks in zip(*taxonomies):
            counter = Counter(ranks)
            most_common = counter.most_common(1)[0]
            if most_common[1] == len(taxonomies):
                lca.append(most_common[0])
            else:
                break
        return lca
