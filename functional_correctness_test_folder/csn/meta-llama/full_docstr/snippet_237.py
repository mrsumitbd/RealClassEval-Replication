
import dendropy
import csv


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
                seq_dict = {row[0]: row[1] for row in reader}
            with open(taxonomy, 'r') as f:
                for line in f:
                    tax_id, taxonomy_str = line.strip().split('\t', 1)
                    tax_dict[seq_dict[tax_id]] = taxonomy_str.split(';')
        else:
            # Greengenes format
            with open(taxonomy, 'r') as f:
                for line in f:
                    tax_id, taxonomy_str = line.strip().split('\t', 1)
                    tax_dict[tax_id] = taxonomy_str.split(';')
        return tax_dict

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
                taxonomy_str = self._get_taxonomy_str(leaf)
                f.write(f'{leaf.taxon.label}\t{taxonomy_str}\n')

    def _get_taxonomy_str(self, node):
        taxonomy = []
        while node:
            if hasattr(node, 'taxonomy'):
                taxonomy.append(node.taxonomy)
            node = node.parent_node
        taxonomy = list(reversed(taxonomy))
        taxonomy_str = ';'.join(taxonomy)
        return taxonomy_str

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
                node.label = f'{label}_{name}:{bootstrap}'
            else:
                node.label = f'{node.label}_{name}'
        else:
            node.label = name
        node.taxonomy = name

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
        name_count = {}
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                node.taxonomy = self.taxonomy.get(node.taxon.label, '')
            else:
                child_taxonomies = [
                    child.taxonomy for child in node.child_nodes()]
                if len(set(child_taxonomies)) == 1:
                    node.taxonomy = child_taxonomies[0]
                    if unique_names and node.taxonomy:
                        name_count[node.taxonomy] = name_count.get(
                            node.taxonomy, 0) + 1
                        if name_count[node.taxonomy] > 1:
                            self._rename(
                                node, f'{node.taxonomy}_{name_count[node.taxonomy]}')
                        else:
                            self._rename(node, node.taxonomy)
                else:
                    node.taxonomy = ''
        self.tree.write_to_path(output_tree, 'newick')
        self._write_consensus_strings(output_tax)
