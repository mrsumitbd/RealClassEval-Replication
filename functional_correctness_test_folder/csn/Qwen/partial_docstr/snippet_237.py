
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
        self.taxonomy = self._parse_taxonomy(taxonomy, seqinfo)

    def _parse_taxonomy(self, taxonomy, seqinfo):
        tax_dict = {}
        if seqinfo:
            with open(seqinfo, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    tax_dict[row[0]] = row[1]
        else:
            with open(taxonomy, mode='r') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    tax_dict[parts[0]] = parts[1]
        return tax_dict

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for node in self.tree.leaf_nodes():
                f.write(
                    f"{node.taxon.label}: {node.annotations.get_value('taxonomy')}\n")

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
        current_label = node.label if node.label else ""
        if ':' in current_label:
            parts = current_label.split(':')
            node.label = f"{parts[0]}:{parts[1]}{name}"
        else:
            node.label = f"{current_label}{name}"

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
        def traverse(node):
            if node.is_leaf():
                node.annotations.add_new(
                    'taxonomy', self.taxonomy[node.taxon.label])
                return {self.taxonomy[node.taxon.label]: 1}
            else:
                tax_counts = defaultdict(int)
                for child in node.child_nodes():
                    child_tax_counts = traverse(child)
                    for tax, count in child_tax_counts.items():
                        tax_counts[tax] += count
                consistent_tax = [tax for tax, count in tax_counts.items(
                ) if count == len(node.child_nodes())]
                if len(consistent_tax) == 1:
                    self._rename(node, f"_{consistent_tax[0]}")
                    return {consistent_tax[0]: len(node.child_nodes())}
                else:
                    if unique_names:
                        for tax, count in tax_counts.items():
                            if count > 1:
                                self._rename(node, f"_{tax}_{count}")
                    return tax_counts

        traverse(self.tree.seed_node)
        self.tree.write(path=output_tree, schema='newick')
        self._write_consensus_strings(output_tax)
