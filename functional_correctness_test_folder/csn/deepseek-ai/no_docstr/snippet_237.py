
import json
from collections import defaultdict


class TreeDecorator:

    def __init__(self, tree, taxonomy, seqinfo=None):
        self.tree = tree
        self.taxonomy = taxonomy
        self.seqinfo = seqinfo if seqinfo is not None else {}

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for tip in self.tree.get_terminals():
                tax_str = self.taxonomy.get(tip.name, "")
                f.write(f"{tip.name}\t{tax_str}\n")

    def _rename(self, node, name):
        node.name = name

    def decorate(self, output_tree, output_tax, unique_names):
        name_counter = defaultdict(int)
        name_map = {}

        for clade in self.tree.find_clades():
            if clade.is_terminal():
                tax_str = self.taxonomy.get(clade.name, "")
                if tax_str:
                    clade.name = f"{clade.name}_{tax_str}"
            else:
                children_tax = []
                for child in clade:
                    if child.is_terminal():
                        tax = self.taxonomy.get(child.name, "")
                    else:
                        tax = child.name.split(
                            '|')[-1] if '|' in child.name else ""
                    if tax:
                        children_tax.append(tax)

                if children_tax:
                    consensus_tax = max(set(children_tax),
                                        key=children_tax.count)
                    if unique_names:
                        name_counter[consensus_tax] += 1
                        unique_name = f"{consensus_tax}_{name_counter[consensus_tax]}"
                        self._rename(clade, unique_name)
                        name_map[clade.name] = unique_name
                    else:
                        self._rename(clade, consensus_tax)
                        name_map[clade.name] = consensus_tax

        with open(output_tree, 'w') as f:
            f.write(str(self.tree))

        self._write_consensus_strings(output_tax)
