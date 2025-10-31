
class Deduplicator:

    def deduplicate(self, aligned_sequence_objects):
        seen_sequences = set()
        deduplicated_sequences = []
        for sequence in aligned_sequence_objects:
            if sequence not in seen_sequences:
                seen_sequences.add(sequence)
                deduplicated_sequences.append(sequence)
        return deduplicated_sequences

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        from collections import defaultdict

        taxonomy_counts = defaultdict(int)
        for sequence in deduplicated_sequences:
            if sequence in taxonomy_hash:
                taxonomy = taxonomy_hash[sequence]
                taxonomy_counts[taxonomy] += 1

        if not taxonomy_counts:
            return None

        lca_taxonomy = max(taxonomy_counts, key=taxonomy_counts.get)
        return lca_taxonomy
