
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
        self._parse_taxonomy()

    def _parse_taxonomy(self):
        if self.seqinfo:
            with open(self.seqinfo, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.tax_dict[row[0]] = row[1]
        else:
            with open(self.taxonomy, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    self.tax_dict[parts[0]] = parts[1]

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for leaf in self.tree.leaf_nodes():
                f.write(
                    f"{leaf.taxon.label}\t{self.tax_dict.get(leaf.taxon.label, '')}\n")

    def _rename(self, node, name):
        if node.label:
            if ':' in node.label:
                parts = node.label.split(':')
                node.label = f"{parts[0]}{name}:{parts[1]}"
            else:
                node.label = f"{node.label}{name}"
        else:
            node.label = name

    def decorate(self, output_tree, output_tax, unique_names):
        self._write_consensus_strings(output_tax)
        tax_counts = defaultdict(int)
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                node.tax = self.tax_dict.get(node.taxon.label, '')
            else:
                child_tax = [child.tax for child in node.child_nodes()]
                if len(set(child_tax)) == 1:
                    node.tax = child_tax[0]
                    if unique_names:
                        tax_counts[node.tax] += 1
                        if tax_counts[node.tax] > 1:
                            self._rename(node, f"_{tax_counts[node.tax]}")
                    else:
                        self._rename(node, node.tax)
                else:
                    node.tax = ''
        self.tree.write(path=output_tree, schema='newick')
