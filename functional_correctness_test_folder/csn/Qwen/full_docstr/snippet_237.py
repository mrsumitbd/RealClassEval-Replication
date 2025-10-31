
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
                    if len(parts) > 1:
                        seq_id, tax_string = parts[0], parts[1]
                        tax_dict[seq_id] = tax_string
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
                tax_string = self._get_taxonomy_string(leaf)
                f.write(f"{leaf.taxon.label}\t{tax_string}\n")

    def _get_taxonomy_string(self, node):
        if node.taxon and node.taxon.label in self.taxonomy:
            return self.taxonomy[node.taxon.label]
        elif node.label:
            return node.label
        return ""

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
            parts = node.label.split(':')
            if len(parts) > 1:
                node.label = f"{parts[0]}:{parts[1]}:{name}"
            else:
                node.label = f"{node.label}:{name}"
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
        self._decorate_tree(self.tree.seed_node, unique_names)
        self.tree.write(path=output_tree, schema='newick')
        self._write_consensus_strings(output_tax)

    def _decorate_tree(self, node, unique_names):
        if node.is_leaf():
            return {self._get_taxonomy_string(node)}

        child_taxonomies = [self._decorate_tree(
            child, unique_names) for child in node.child_nodes()]
        common_taxonomy = set.intersection(*child_taxonomies)

        if common_taxonomy:
            common_tax = common_taxonomy.pop()
            self._rename(node, common_tax)
        else:
            for i, child in enumerate(node.child_nodes()):
                self._rename(child, f"clade_{i}")

        if unique_names:
            self._ensure_unique_names(node)

        return set.union(*child_taxonomies)

    def _ensure_unique_names(self, node):
        name_count = defaultdict(int)
        for child in node.child_nodes():
            if child.label:
                name_count[child.label] += 1

        for child in node.child_nodes():
            if name_count[child.label] > 1:
                self._rename(child, f"{child.label}_{name_count[child.label]}")
                name_count[child.label] -= 1
