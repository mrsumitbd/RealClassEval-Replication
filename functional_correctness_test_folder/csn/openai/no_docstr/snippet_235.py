
class Deduplicator:
    """
    A simple deduplication and taxonomy LCA utility.

    The class expects objects that expose at least two attributes:
        - `id`   : a unique identifier for the sequence
        - `seq`  : the sequence string

    The `deduplicate` method removes duplicate sequences (by sequence string)
    while preserving the original order of first occurrences.

    The `lca_taxonomy` method computes the lowest common ancestor (LCA) of
    taxonomy paths for a list of deduplicated sequences.  The taxonomy
    paths are supplied via a dictionary mapping sequence IDs to a list of
    taxonomy ranks (e.g. ['k__Bacteria', 'p__Proteobacteria', ...]).
    The method returns the longest common prefix of these taxonomy lists.
    """

    def deduplicate(self, aligned_sequence_objects):
        """
        Remove duplicate sequences from a list of sequence objects.

        Parameters
        ----------
        aligned_sequence_objects : list
            List of objects that have at least the attributes `id` and `seq`.

        Returns
        -------
        list
            A list of unique sequence objects, preserving the order of first
            appearance.
        """
        seen = set()
        unique = []
        for obj in aligned_sequence_objects:
            seq = getattr(obj, "seq", None)
            if seq is None:
                # If the object does not have a `seq` attribute, skip it.
                continue
            if seq not in seen:
                seen.add(seq)
                unique.append(obj)
        return unique

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        """
        Compute the lowest common ancestor (LCA) taxonomy for a set of
        deduplicated sequences.

        Parameters
        ----------
        deduplicated_sequences : list
            List of sequence objects that have an `id` attribute.
        taxonomy_hash : dict
            Mapping from sequence ID to a list of taxonomy ranks.

        Returns
        -------
        list
            The longest common prefix of the taxonomy lists for all
            provided sequences.  If no common prefix exists, an empty list
            is returned.
        """
        # Gather taxonomy lists for all sequences
        tax_lists = []
        for seq_obj in deduplicated_sequences:
            seq_id = getattr(seq_obj, "id", None)
            if seq_id is None:
                continue
            tax = taxonomy_hash.get(seq_id)
            if tax is None:
                continue
            tax_lists.append(tax)

        if not tax_lists:
            return []

        # Compute common prefix
        lca = []
        for ranks in zip(*tax_lists):
            if all(rank == ranks[0] for rank in ranks):
                lca.append(ranks[0])
            else:
                break
        return lca
