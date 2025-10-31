
class TreeDecorator:

    def __init__(self, tree, taxonomy, seqinfo=None):
        self.tree = tree
        self.taxonomy = taxonomy
        self.seqinfo = seqinfo if seqinfo is not None else {}
        self.name_counter = {}

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for node in self.tree.get_terminals():
                f.write(f"{node.name}\t{self.seqinfo.get(node.name, '')}\n")

    def _rename(self, node, name):
        if name in self.name_counter:
            self.name_counter[name] += 1
        else:
            self.name_counter[name] = 1
        if self.name_counter[name] > 1:
            node.name = f"{name}_{self.name_counter[name]}"
        else:
            node.name = name

    def decorate(self, output_tree, output_tax, unique_names):
        def assign_taxonomy(node):
            if node.is_terminal():
                tax = self.taxonomy.get(node.name, '')
                if unique_names:
                    self._rename(node, tax)
                else:
                    node.name = tax
            else:
                child_taxes = [assign_taxonomy(child) for child in node.clades]
                if child_taxes:
                    consensus_tax = self._consensus_taxonomy(child_taxes)
                    if unique_names:
                        self._rename(node, consensus_tax)
                    else:
                        node.name = consensus_tax
                else:
                    node.name = ''
            return node.name

        def _consensus_taxonomy(taxonomies):
            from collections import Counter
            tax_counter = Counter(taxonomies)
            most_common_tax, count = tax_counter.most_common(1)[0]
            if count == len(taxonomies):
                return most_common_tax
            else:
                return 'mixed'

        assign_taxonomy(self.tree)
        self.tree.write(output_tree)
        self._write_consensus_strings(output_tax)
