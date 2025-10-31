
class TreeDecorator:

    def __init__(self, tree, taxonomy, seqinfo=None):
        self.tree = tree
        self.taxonomy = taxonomy  # dict: tip_name -> taxonomy string or list
        self.seqinfo = seqinfo if seqinfo is not None else {}
        self.tip_tax = {}  # tip_name -> taxonomy string
        self.tip_nodes = {}  # tip_name -> node
        self._collect_tips(self.tree)

    def _collect_tips(self, node):
        if not hasattr(node, 'clades') or not node.clades:
            self.tip_nodes[node.name] = node
            if node.name in self.taxonomy:
                self.tip_tax[node.name] = self.taxonomy[node.name]
        else:
            for clade in node.clades:
                self._collect_tips(clade)

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for tip, tax in self.tip_tax.items():
                f.write(f"{tip}\t{tax}\n")

    def _rename(self, node, name):
        node.name = name

    def decorate(self, output_tree, output_tax, unique_names):
        from collections import defaultdict
        import copy

        def get_tip_names(node):
            if not hasattr(node, 'clades') or not node.clades:
                return [node.name]
            names = []
            for clade in node.clades:
                names.extend(get_tip_names(clade))
            return names

        def get_tax_list(tip_names):
            # Return list of taxonomy lists for the tips
            tax_list = []
            for tip in tip_names:
                tax = self.taxonomy.get(tip)
                if tax is None:
                    continue
                if isinstance(tax, str):
                    tax = tax.split(';')
                tax_list.append([t.strip() for t in tax])
            return tax_list

        def consensus_tax(tax_list):
            if not tax_list:
                return []
            minlen = min(len(t) for t in tax_list)
            consensus = []
            for i in range(minlen):
                vals = set(t[i] for t in tax_list)
                if len(vals) == 1:
                    consensus.append(list(vals)[0])
                else:
                    break
            return consensus

        # For unique_names, keep a tally of group names at each rank
        name_tally = defaultdict(int)
        used_names = set()

        def decorate_node(node):
            tip_names = get_tip_names(node)
            tax_list = get_tax_list(tip_names)
            cons = consensus_tax(tax_list)
            if not cons:
                return
            name = cons[-1]
            if unique_names:
                key = ';'.join(cons)
                name_tally[key] += 1
                if name_tally[key] > 1:
                    name = f"{name}_{name_tally[key]}"
            # Only rename if not a tip
            if hasattr(node, 'clades') and node.clades:
                self._rename(node, name)
            # Recurse
            for clade in getattr(node, 'clades', []):
                decorate_node(clade)

        # Work on a copy of the tree to avoid modifying the original
        import copy
        tree_copy = copy.deepcopy(self.tree)
        decorate_node(tree_copy)
        # Write the decorated tree
        try:
            from Bio import Phylo
            Phylo.write(tree_copy, output_tree, "newick")
        except ImportError:
            # Fallback: write as Newick manually
            def to_newick(node):
                if not hasattr(node, 'clades') or not node.clades:
                    return node.name
                else:
                    return "(" + ",".join(to_newick(c) for c in node.clades) + ")" + (node.name if node.name else "")
            with open(output_tree, 'w') as f:
                f.write(to_newick(tree_copy) + ";\n")
        # Write taxonomy strings for each tip
        self._write_consensus_strings(output_tax)
