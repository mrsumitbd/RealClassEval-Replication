
class Deduplicator:

    def deduplicate(self, aligned_sequence_objects):
        unique_sequences = {}
        for seq_obj in aligned_sequence_objects:
            seq = seq_obj.sequence
            if seq not in unique_sequences:
                unique_sequences[seq] = seq_obj
        return list(unique_sequences.values())

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        lca_taxonomies = {}
        for seq_obj in deduplicated_sequences:
            tax_ids = seq_obj.taxonomy_ids
            common_ancestors = set(taxonomy_hash[tax_ids[0]])
            for tax_id in tax_ids[1:]:
                common_ancestors.intersection_update(taxonomy_hash[tax_id])
            lca_taxonomies[seq_obj] = common_ancestors
        return lca_taxonomies
