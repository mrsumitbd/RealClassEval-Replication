
import dendropy
import csv
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
        self.taxonomy = taxonomy
        self.seqinfo = seqinfo
        self.tax_dict = {}
        self._load_taxonomy()

    def _load_taxonomy(self):
        if self.seqinfo is None:
            # Assume Greengenes format
            with open(self.taxonomy, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        seq_id = parts[0]
                        tax_string = parts[1]
                        self.tax_dict[seq_id] = tax_string
        else:
            # Assume taxtastic format with seqinfo
            seqinfo_dict = {}
            with open(self.seqinfo, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:
                        seq_id = row[0]
                        tax_rank = row[1]
                        seqinfo_dict[seq_id] = tax_rank

            with open(self.taxonomy, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        tax_id = parts[0]
                        tax_string = parts[1]
                        if tax_id in seqinfo_dict:
                            seq_id = seqinfo_dict[tax_id]
                            self.tax_dict[seq_id] = tax_string

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for seq_id, tax_string in self.tax_dict.items():
                f.write(f"{seq_id}\t{tax_string}\n")

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
            if ':' in node.label:
                parts = node.label.split(':')
                node.label = f"{parts[0]}:{name}"
            else:
                node.label = f"{node.label}:{name}"

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
        name_counts = defaultdict(int)

        def _decorate_node(node):
            if node.is_leaf():
                return {self.tax_dict.get(node.taxon.label, '')}

            child_taxa = set()
            for child in node.child_nodes():
                child_taxa.update(_decorate_node(child))

            if len(child_taxa) == 1:
                tax = next(iter(child_taxa))
                if tax:
                    if unique_names:
                        name_counts[tax] += 1
                        unique_tax = f"{tax}_{name_counts[tax]}"
                        self._rename(node, unique_tax)
                    else:
                        self._rename(node, tax)
                return child_taxa
            else:
                return set()

        _decorate_node(self.tree.seed_node)
        self.tree.write(path=output_tree, schema='newick')
        self._write_consensus_strings(output_tax)
