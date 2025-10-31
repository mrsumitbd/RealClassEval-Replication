
import dendropy
from collections import defaultdict


class TreeDecorator:
    '''
    A class that conservatively decorates trees with taxonomy, or any other
    hierarchical annotation. If all tips descending from a node within the
    provided tree have consistent taxonomy, it will be decorated with that
    taxonomy (or annotation of any type).
    '''

    def __init__(self, tree, taxonomy, seqinfo=None):
        '''
        Parameters
        ----------
        tree        : dendropy.Tree
            dendropy.Tree object
        taxonomy    : string
            Path to a file containing taxonomy information about the tree,
            either in Greengenes or taxtastic format (seqinfo file must also
            be provided if taxonomy is in taxtastic format).
        seqinfo     : string
            Path to a seqinfo file. This is a .csv file with the first column
            denoting the sequence name, and the second column, its most resolved
            taxonomic rank.
        '''
        self.tree = tree
        self.taxonomy_map = {}
        self.seqinfo_map = {}
        # read taxonomy file
        with open(taxonomy, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                seqname, tax = parts[0], parts[1]
                self.taxonomy_map[seqname] = tax
        # read seqinfo file if provided
        if seqinfo:
            with open(seqinfo, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split(',')
                    if len(parts) < 2:
                        continue
                    seqname, tax = parts[0], parts[1]
                    self.seqinfo_map[seqname] = tax

    def _write_consensus_strings(self, output):
        '''
        Write taxonomy strings for each tip to the output file.
        '''
        with open(output, 'w') as out:
            for leaf in self.tree.leaf_nodes():
                name = leaf.taxon.label if leaf.taxon else leaf.label
                tax = self.taxonomy_map.get(name, '')
                out.write(f'{name}\t{tax}\n')

    def _rename(self, node, name):
        '''
        Rename an internal node of the tree. If an annotation is already
        present, append the new annotation to the end of it. If a bootstrap
        value is present, add annotations are added after a ":" as per standard
        newick format.
        Parameters
        ----------
        node: dendropy.Node
            dendropy.Node object
        name    : string
            Annotation to rename the node with.
        '''
        if node.label is None:
            node.label = name
        else:
            # if node already has a label, append with a separator
            node.label = f'{node.label}|{name}'

    def decorate(self, output_tree, output_tax, unique_names):
        '''
        Decorate a tree with taxonomy. This code does not allow inconsistent
        taxonomy within a clade. If one sequence in a clade has a different
        annotation to the rest, it will split the clade. Paraphyletic group
        names are distinguished if unique_names = True using a simple tally of
        each group (see unique_names below).
        Parameters
        ----------
        output_tree        : string
            File to which the decorated tree will be written.
        output_tax         : string
            File to which the taxonomy strings for each tip in the tree will be
            written.
        unique_names       : boolean
            True indicating that a unique number will be appended to the end of
            a taxonomic rank if it is found more than once in the tree
            (i.e. it is paraphyletic in the tree). If false, multiple clades
            may be assigned with the same name.
        '''
        # Count occurrences for unique naming
        tax_counts = defaultdict(int)

        # Helper to get taxonomy for a leaf
        def leaf_tax(leaf):
            name = leaf.taxon.label if leaf.taxon else leaf.label
            return self.taxonomy_map.get(name, '')

        # Postorder traversal to annotate internal nodes
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                continue
            # gather taxonomy strings of descendant tips
            taxa = set()
            for leaf in node.leaf_nodes():
                taxa.add(leaf_tax(leaf))
            if len(taxa) == 1:
                tax = taxa.pop()
                if unique_names:
                    tax_counts[tax] += 1
                    if tax_counts[tax] > 1:
                        tax = f'{tax}_{tax_counts[tax]}'
                self._rename(node, tax)

        # Write taxonomy strings for each tip
        self._write_consensus_strings(output_tax)

        # Write decorated tree
        self.tree.write(path=output_tree, schema='newick', suppress_rooting=False,
                        unquoted_underscores=True)
