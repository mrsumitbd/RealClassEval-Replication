
class Deduplicator:

    def deduplicate(self, aligned_sequence_objects):
        """
        Deduplicate aligned_sequence_objects by their 'sequence' field.
        Returns a list of unique sequence objects (first occurrence kept).
        """
        seen = set()
        deduped = []
        for obj in aligned_sequence_objects:
            seq = obj.get('sequence')
            if seq not in seen:
                seen.add(seq)
                deduped.append(obj)
        return deduped

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        """
        For each deduplicated sequence, find the LCA (Lowest Common Ancestor) taxonomy
        from the taxonomy_hash, which maps sequence to taxonomy (as a list of ranks).
        Returns a list of dicts with 'sequence' and 'lca_taxonomy' keys.
        """
        def lca(taxa_list):
            if not taxa_list:
                return []
            min_len = min(len(t) for t in taxa_list)
            lca_result = []
            for i in range(min_len):
                current = taxa_list[0][i]
                if all(t[i] == current for t in taxa_list):
                    lca_result.append(current)
                else:
                    break
            return lca_result

        result = []
        for obj in deduplicated_sequences:
            seq = obj.get('sequence')
            taxonomies = taxonomy_hash.get(seq, [])
            # If taxonomy_hash[seq] is a list of lists, find LCA among them
            if taxonomies and isinstance(taxonomies[0], list):
                lca_tax = lca(taxonomies)
            else:
                lca_tax = taxonomies if taxonomies else []
            result.append({'sequence': seq, 'lca_taxonomy': lca_tax})
        return result
