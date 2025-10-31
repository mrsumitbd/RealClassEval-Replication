
import csv
import collections
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
        self.taxonomy = {}
        self.taxonomy_format = None

        # Try to detect format
        if seqinfo is None:
            # Greengenes format: tab separated, first col is tip, second col is taxonomy string
            with open(taxonomy, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('\t')
                    if len(parts) < 2:
                        continue
                    tip, tax = parts[0], parts[1]
                    self.taxonomy[tip] = tax
            self.taxonomy_format = 'greengenes'
        else:
            # Taxtastic format: taxonomy is a csv with id, taxonomy string; seqinfo is a csv with tip, taxonomy id
            # Read taxonomy file
            taxid_to_tax = {}
            with open(taxonomy, 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    taxid, taxstr = row[0], row[1]
                    taxid_to_tax[taxid] = taxstr
            # Read seqinfo file
            with open(seqinfo, 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    tip, taxid = row[0], row[1]
                    if taxid in taxid_to_tax:
                        self.taxonomy[tip] = taxid_to_tax[taxid]
            self.taxonomy_format = 'taxtastic'

        # For each node, will store consensus taxonomy string (or None)
        for node in self.tree:
            node.consensus_taxonomy = None

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
                name = leaf.taxon.label if leaf.taxon else leaf.label
                tax = self.taxonomy.get(name, None)
                if tax is None:
                    # Try to get from consensus up the tree
                    node = leaf
                    while node is not None:
                        if hasattr(node, 'consensus_taxonomy') and node.consensus_taxonomy:
                            tax = node.consensus_taxonomy
                            break
                        node = node.parent_node
                if tax is None:
                    tax = ''
                f.write(f"{name}\t{tax}\n")

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
        # DendroPy nodes have label and annotations
        if node.label is not None:
            # If label is a bootstrap value (numeric), append after ":"
            try:
                float(node.label)
                node.label = f"{node.label}:{name}"
            except ValueError:
                # Not a number, append annotation
                node.label = f"{node.label}_{name}"
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
        # First, for each tip, assign its taxonomy string
        for leaf in self.tree.leaf_node_iter():
            name = leaf.taxon.label if leaf.taxon else leaf.label
            leaf.consensus_taxonomy = self.taxonomy.get(name, None)

        # For unique_names, keep a count of each group name
        group_counts = collections.defaultdict(int)
        group_seen = collections.defaultdict(int)

        def get_consensus(node):
            if node.is_leaf():
                return node.consensus_taxonomy
            child_taxa = [get_consensus(child)
                          for child in node.child_node_iter()]
            child_taxa = [t for t in child_taxa if t is not None]
            if not child_taxa:
                node.consensus_taxonomy = None
                return None
            # If all children have the same taxonomy, assign to this node
            if all(t == child_taxa[0] for t in child_taxa):
                node.consensus_taxonomy = child_taxa[0]
                return child_taxa[0]
            else:
                node.consensus_taxonomy = None
                return None

        get_consensus(self.tree.seed_node)

        # Now, for each internal node, if it has a consensus taxonomy, rename it
        def assign_names(node):
            if node.is_leaf():
                return
            if node.consensus_taxonomy:
                group_name = node.consensus_taxonomy
                if unique_names:
                    group_counts[group_name] += 1
                    group_seen[group_name] += 1
                    group_name_unique = f"{group_name}_{group_counts[group_name]}"
                    self._rename(node, group_name_unique)
                else:
                    self._rename(node, group_name)
            for child in node.child_node_iter():
                assign_names(child)

        assign_names(self.tree.seed_node)

        # Write the decorated tree
        self.tree.write(path=output_tree, schema="newick",
                        suppress_rooting=True, suppress_annotations=False)

        # Write the taxonomy strings for each tip
        self._write_consensus_strings(output_tax)
