
class Deduplicator:

    def deduplicate(self, aligned_sequence_objects):
        unique_sequences = {}
        for seq_obj in aligned_sequence_objects:
            seq = str(seq_obj.seq)
            if seq not in unique_sequences:
                unique_sequences[seq] = seq_obj
        return list(unique_sequences.values())

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        from collections import defaultdict

        tax_counts = defaultdict(int)
        for seq_obj in deduplicated_sequences:
            seq = str(seq_obj.seq)
            if seq in taxonomy_hash:
                tax_counts[taxonomy_hash[seq]] += 1

        if not tax_counts:
            return None

        max_count = max(tax_counts.values())
        most_common_tax = [tax for tax,
                           count in tax_counts.items() if count == max_count]

        if len(most_common_tax) == 1:
            return most_common_tax[0]

        # Find LCA if multiple taxa have the same max count
        from ete3 import NCBITaxa
        ncbi = NCBITaxa()

        def get_lineage(taxid):
            try:
                lineage = ncbi.get_lineage(taxid)
                return set(lineage)
            except:
                return set()

        lineages = [get_lineage(taxid) for taxid in most_common_tax]
        common_ancestors = set.intersection(*lineages) if lineages else set()

        if not common_ancestors:
            return None

        # Get the lowest (most specific) common ancestor
        lca = None
        for taxid in most_common_tax:
            if taxid in common_ancestors:
                lca = taxid
                break

        if lca is None:
            # Find the deepest common ancestor
            max_depth = -1
            for ancestor in common_ancestors:
                depth = len(ncbi.get_lineage(ancestor))
                if depth > max_depth:
                    max_depth = depth
                    lca = ancestor

        return lca
