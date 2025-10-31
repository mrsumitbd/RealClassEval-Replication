
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
        self.tax_dict = defaultdict(list)

        if seqinfo:
            with open(seqinfo, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.tax_dict[row[0]].append(row[1])

        with open(taxonomy, 'r') as f:
            for line in f:
                if seqinfo:
                    seq_id = line.split('\t')[0]
                    tax_str = line.split('\t')[1].strip()
                    self.tax_dict[seq_id].append(tax_str)
                else:
                    seq_id = line.split(';')[0].strip()
                    tax_str = line.split(';')[1].strip()
                    self.tax_dict[seq_id].append(tax_str)

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
            for leaf in self.tree.leaf_nodes():
                tax_str = '; '.join(self.tax_dict[leaf.taxon.label])
                f.write(f"{leaf.taxon.label}\t{tax_str}\n")

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
        if node.label:
            if ':' in node.label:
                bootstrap, label = node.label.split(':')
                node.label = f"{bootstrap}:{label};{name}"
            else:
                node.label = f"{node.label};{name}"
        else:
            node.label = name

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
        tax_counts = defaultdict(int)

        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                node.taxonomy = self.tax_dict[node.taxon.label]
            else:
                child_taxonomies = [
                    child.taxonomy for child in node.child_nodes()]
                if all(tax == child_taxonomies[0] for tax in child_taxonomies):
                    node.taxonomy = child_taxonomies[0]
                else:
                    node.taxonomy = None

        for node in self.tree.postorder_node_iter():
            if node.taxonomy:
                tax_str = '; '.join(node.taxonomy)
                if unique_names:
                    tax_counts[tax_str] += 1
                    if tax_counts[tax_str] > 1:
                        tax_str = f"{tax_str}_{tax_counts[tax_str]}"
                self._rename(node, tax_str)

        self.tree.write(path=output_tree, schema='newick')
        self._write_consensus_strings(output_tax)
