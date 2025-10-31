
from typing import List, Dict


class Sequence:
    def __init__(self, name: str, sequence: str):
        self.name = name
        self.sequence = sequence


class Deduplicator:
    '''Deduplicates sequences'''

    def deduplicate(self, aligned_sequence_objects: List[Sequence]) -> List[List[Sequence]]:
        sequence_dict = {}
        for sequence in aligned_sequence_objects:
            if sequence.sequence not in sequence_dict:
                sequence_dict[sequence.sequence] = [sequence]
            else:
                sequence_dict[sequence.sequence].append(sequence)
        return list(sequence_dict.values())

    def lca_taxonomy(self, deduplicated_sequences: List[List[Sequence]], taxonomy_hash: Dict[str, List[str]]) -> List[List[str]]:
        lcas = []
        for group in deduplicated_sequences:
            taxonomies = [taxonomy_hash[seq.name]
                          for seq in group if seq.name in taxonomy_hash]
            if taxonomies:
                lca = self._lca(taxonomies)
                lcas.append(lca)
            else:
                lcas.append([])
        return lcas

    def _lca(self, taxonomies: List[List[str]]) -> List[str]:
        if not taxonomies:
            return []

        lca = taxonomies[0]
        for taxonomy in taxonomies[1:]:
            lca = self._common_prefix(lca, taxonomy)
        return lca

    def _common_prefix(self, list1: List[str], list2: List[str]) -> List[str]:
        common_prefix = []
        for elem1, elem2 in zip(list1, list2):
            if elem1 == elem2:
                common_prefix.append(elem1)
            else:
                break
        return common_prefix


# Example usage:
if __name__ == "__main__":
    deduplicator = Deduplicator()

    # Create some example Sequence objects
    seq1 = Sequence('seq1', 'ATCG')
    seq2 = Sequence('seq2', 'ATCG')
    seq3 = Sequence('seq3', 'ATGC')
    seq4 = Sequence('seq4', 'ATGC')

    # Deduplicate sequences
    aligned_sequences = [seq1, seq2, seq3, seq4]
    deduplicated = deduplicator.deduplicate(aligned_sequences)
    print("Deduplicated sequences:")
    for i, group in enumerate(deduplicated):
        print(f"Group {i+1}: {[seq.name for seq in group]}")

    # Create a taxonomy hash
    taxonomy_hash = {
        'seq1': ['Bacteria', 'Firmicutes', 'Bacillus'],
        'seq2': ['Bacteria', 'Firmicutes', 'Bacillus'],
        'seq3': ['Bacteria', 'Proteobacteria', 'Escherichia'],
        'seq4': ['Bacteria', 'Proteobacteria', 'Escherichia']
    }

    # Calculate LCA taxonomy
    lcas = deduplicator.lca_taxonomy(deduplicated, taxonomy_hash)
    print("\nLCA Taxonomies:")
    for i, lca in enumerate(lcas):
        print(f"Group {i+1}: {lca}")
