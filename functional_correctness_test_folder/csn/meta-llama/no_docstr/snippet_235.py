
class Deduplicator:

    def deduplicate(self, aligned_sequence_objects):
        """
        Removes duplicate sequences from the given list of aligned sequence objects.

        Args:
            aligned_sequence_objects (list): A list of aligned sequence objects.

        Returns:
            list: A list of deduplicated sequence objects.
        """
        seen = set()
        deduplicated_sequences = []
        for sequence in aligned_sequence_objects:
            sequence_str = str(sequence)
            if sequence_str not in seen:
                seen.add(sequence_str)
                deduplicated_sequences.append(sequence)
        return deduplicated_sequences

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        """
        Assigns the lowest common ancestor (LCA) taxonomy to the given deduplicated sequences.

        Args:
            deduplicated_sequences (list): A list of deduplicated sequence objects.
            taxonomy_hash (dict): A dictionary mapping sequence IDs to their corresponding taxonomies.

        Returns:
            dict: A dictionary mapping deduplicated sequence IDs to their corresponding LCA taxonomies.
        """
        lca_taxonomies = {}
        for sequence in deduplicated_sequences:
            sequence_id = sequence.id  # Assuming sequence objects have an 'id' attribute
            taxonomy = taxonomy_hash.get(sequence_id)
            if taxonomy:
                lca_taxonomies[sequence_id] = taxonomy
        return lca_taxonomies
