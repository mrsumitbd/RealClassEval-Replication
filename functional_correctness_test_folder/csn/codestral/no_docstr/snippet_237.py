
class TreeDecorator:

    def __init__(self, tree, taxonomy, seqinfo=None):

        self.tree = tree
        self.taxonomy = taxonomy
        self.seqinfo = seqinfo

    def _write_consensus_strings(self, output):

        with open(output, 'w') as f:
            for node in self.tree.get_terminals():
                tax_string = self.taxonomy.get(node.name, '')
                f.write(f"{node.name}\t{tax_string}\n")

    def _rename(self, node, name):

        if name in node.name:
            return
        if not node.is_terminal():
            node.name = name
        else:
            node.name = f"{name}_{node.name}"

    def decorate(self, output_tree, output_tax, unique_names):

        self._write_consensus_strings(output_tax)
        for node in self.tree.get_nonterminals(order='postorder'):
            tax_dict = {}
            for child in node.clades:
                if child.is_terminal():
                    tax_string = self.taxonomy.get(child.name, '')
                    tax_dict[tax_string] = tax_dict.get(tax_string, 0) + 1
                else:
                    tax_string = child.name
                    tax_dict[tax_string] = tax_dict.get(tax_string, 0) + 1
            if len(tax_dict) == 1:
                tax_string = list(tax_dict.keys())[0]
                if unique_names and tax_dict[tax_string] > 1:
                    tax_string = f"{tax_string}_{tax_dict[tax_string]}"
                self._rename(node, tax_string)
        self.tree.write(format=1, outfile=output_tree)
