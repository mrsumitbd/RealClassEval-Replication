
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
            with open(self.taxonomy, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        seq_id = parts[0]
                        tax_str = parts[1]
                        self.tax_dict[seq_id] = tax_str
        else:
            seq_to_taxid = {}
            with open(self.seqinfo, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        seq_id = row[0]
                        taxid = row[1]
                        seq_to_taxid[seq_id] = taxid

            taxid_to_tax = {}
            with open(self.taxonomy, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    if len(row) >= 2:
                        taxid = row[0]
                        tax_str = row[1]
                        taxid_to_tax[taxid] = tax_str

            for seq_id, taxid in seq_to_taxid.items():
                if taxid in taxid_to_tax:
                    self.tax_dict[seq_id] = taxid_to_tax[taxid]

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
        with open(output, 'w') as f:
            for leaf in self.tree.leaf_node_iter():
                tax_str = self._get_tax_string(leaf)
                f.write(f"{leaf.taxon.label}\t{tax_str}\n")

    def _get_tax_string(self, node):
        if node.is_leaf():
            return self.tax_dict.get(node.taxon.label, "")
        else:
            for child in node.child_node_iter():
                if not child.label or ";" not in child.label:
                    return ""
            return node.label.split(";")[-1].strip()

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
            if ":" in node.label:
                parts = node.label.split(":")
                node.label = f"{parts[0]}:{name}"
            else:
                node.label = f"{node.label}; {name}"

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
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                continue
            tax_set = set()
            for leaf in node.leaf_iter():
                tax_str = self.tax_dict.get(leaf.taxon.label, "")
                tax_set.add(tax_str)
            if len(tax_set) == 1:
                tax_str = tax_set.pop()
                if tax_str:
                    if unique_names:
                        name_counts[tax_str] += 1
                        unique_name = f"{tax_str}_{name_counts[tax_str]}"
                        self._rename(node, unique_name)
                    else:
                        self._rename(node, tax_str)
        self.tree.write_to_path(output_tree, schema="newick")
        self._write_consensus_strings(output_tax)
