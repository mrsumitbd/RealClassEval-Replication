
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
        self.taxonomy = self._read_taxonomy(taxonomy, seqinfo)

    def _read_taxonomy(self, taxonomy, seqinfo):
        tax_dict = {}
        if seqinfo:
            # taxtastic format
            with open(seqinfo, 'r') as f:
                reader = csv.reader(f)
                seq_to_tax_id = {row[0]: row[1] for row in reader}
            with open(taxonomy, 'r') as f:
                for line in f:
                    tax_id, tax_string = line.strip().split('\t', 1)
                    tax_dict[seq_to_tax_id[tax_id]] = tax_string.split(';')
        else:
            # Greengenes format
            with open(taxonomy, 'r') as f:
                for line in f:
                    tax_id, tax_string = line.strip().split('\t', 1)
                    tax_dict[tax_id] = tax_string.split(';')
        return tax_dict

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for tip in self.tree.taxon_namespace:
                tip_name = tip.label
                if tip_name in self.taxonomy:
                    f.write('%s\t%s\n' %
                            (tip_name, ';'.join(self.taxonomy[tip_name])))
                else:
                    f.write('%s\t\n' % tip_name)

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
                label, bootstrap = node.label.split(':')
                node.label = '%s_%s:%s' % (label, name, bootstrap)
            else:
                node.label = '%s_%s' % (node.label, name)
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
        self._write_consensus_strings(output_tax)
        name_counts = defaultdict(int)
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                node_taxonomy = self.taxonomy.get(node.taxon.label, [])
                node.annotations['taxonomy'] = node_taxonomy
            else:
                child_taxonomies = [child.annotations['taxonomy']
                                    for child in node.child_nodes()]
                consensus_taxonomy = self._consensus(child_taxonomies)
                node.annotations['taxonomy'] = consensus_taxonomy
                if consensus_taxonomy and unique_names:
                    for i, rank in enumerate(consensus_taxonomy):
                        name_counts[rank] += 1
                        if name_counts[rank] > 1:
                            consensus_taxonomy[i] = '%s_%d' % (
                                rank, name_counts[rank])
                if consensus_taxonomy:
                    self._rename(node, '_'.join(consensus_taxonomy))
        self.tree.write_to_path(output_tree, 'newick')

    def _consensus(self, taxonomies):
        if not taxonomies:
            return []
        consensus = []
        for ranks in zip(*taxonomies):
            if len(set(ranks)) == 1:
                consensus.append(ranks[0])
            else:
                break
        return consensus
