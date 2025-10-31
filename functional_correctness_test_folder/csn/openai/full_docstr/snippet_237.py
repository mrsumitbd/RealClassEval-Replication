
import csv
import os
from collections import defaultdict

import dendropy


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
        self.taxonomy_file = taxonomy
        self.seqinfo_file = seqinfo

        # mapping from seqname -> taxonomy string
        self.seq_tax = {}
        self._load_taxonomy()

        # mapping from seqname -> tax rank (if seqinfo provided)
        self.seq_rank = {}
        if self.seqinfo_file:
            self._load_seqinfo()

        # store taxonomy annotation for each node
        self.node_tax = {}

    def _load_taxonomy(self):
        """Load taxonomy mapping from file."""
        if not os.path.exists(self.taxonomy_file):
            raise FileNotFoundError(
                f"Taxonomy file {self.taxonomy_file} not found")

        with open(self.taxonomy_file, "r") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                # Greengenes format: seqname; taxonomy
                if ";" in line:
                    parts = line.split(";")
                    seqname = parts[0].strip()
                    tax = ";".join(p.strip() for p in parts[1:])
                else:
                    # fallback: tab separated
                    parts = line.split("\t")
                    seqname = parts[0].strip()
                    tax = parts[1].strip()
                self.seq_tax[seqname] = tax

    def _load_seqinfo(self):
        """Load seqinfo mapping from file."""
        if not os.path.exists(self.seqinfo_file):
            raise FileNotFoundError(
                f"Seqinfo file {self.seqinfo_file} not found")

        with open(self.seqinfo_file, "r") as fh:
            reader = csv.reader(fh)
            for row in reader:
                if len(row) < 2:
                    continue
                seqname = row[0].strip()
                rank = row[1].strip()
                self.seq_rank[seqname] = rank

    def _write_consensus_strings(self, output):
        '''
        Writes the taxonomy of each leaf to a file. If the leaf has no
        taxonomy, a taxonomy string will be created using the annotations
        provided to the ancestor nodes of that leaf (meaning, it will be
        decorated).
        Parameters
        ----------
        output    : string
            File to which the taxonomy strings for each leaf in the tree will
            be written in Greengenes format, e.g.
                637960147    mcrA; Euryarchaeota_mcrA; Methanomicrobia
                637699780    mcrA; Euryarchaeota_mcrA; Methanomicrobia
        '''
        with open(output, "w") as fh:
            for leaf in self.tree.leaf_node_iter():
                seqname = leaf.taxon.label if leaf.taxon else leaf.label
                tax = self.node_tax.get(leaf)
                if not tax:
                    # walk up to find nearest annotated ancestor
                    node = leaf
                    while node.parent_node:
                        node = node.parent_node
                        tax = self.node_tax.get(node)
                        if tax:
                            break
                if not tax:
                    tax = ""
                fh.write(f"{seqname}\t{tax}\n")

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
        # existing label
        existing = node.label or ""
        # if bootstrap present, keep it after colon
        if node.edge and node.edge.support is not None:
            # support is numeric
            support = node.edge.support
            # remove existing support from label if present
            if ":" in existing:
                existing = existing.split(":")[0]
            new_label = f"{existing};{name}:{support}"
        else:
            new_label = f"{existing};{name}" if existing else name
        node.label = new_label

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
        # First, assign taxonomy to leaves
        for leaf in self.tree.leaf_node_iter():
            seqname = leaf.taxon.label if leaf.taxon else leaf.label
            tax = self.seq_tax.get(seqname)
            if tax:
                self.node_tax[leaf] = tax

        # Count occurrences for unique naming
        tax_counts = defaultdict(int)

        # Post-order traversal to annotate internal nodes
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                continue
            # gather taxonomy of descendant leaves
            descendant_taxes = set()
            for leaf in node.leaf_iter():
                tax = self.node_tax.get(leaf)
                if tax:
                    descendant_taxes.add(tax)
            if len(descendant_taxes) == 1:
                tax = descendant_taxes.pop()
                # unique naming
                if unique_names:
                    tax_counts[tax] += 1
                    if tax_counts[tax] > 1:
                        tax = f"{tax}_{tax_counts[tax]}"
