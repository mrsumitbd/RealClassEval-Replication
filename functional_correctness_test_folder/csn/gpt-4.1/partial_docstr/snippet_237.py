
import csv
from collections import defaultdict, Counter
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
        self.taxonomy_ranks = []
        self.seqinfo = {}
        self.tip_taxonomy = {}
        self.tip_names = set(
            [leaf.taxon.label for leaf in self.tree.leaf_node_iter()])
        self._parse_taxonomy(taxonomy, seqinfo)

    def _parse_taxonomy(self, taxonomy, seqinfo):
        # Try to detect format: Greengenes or taxtastic
        # Greengenes: tab-delimited, first column is tip name, second is taxonomy string
        # Taxtastic: taxonomy is a .csv with id, name, parent_id, rank, etc. seqinfo is required
        if taxonomy.endswith('.csv') and seqinfo is not None:
            # Taxtastic format
            # Parse taxonomy file
            id_to_name = {}
            id_to_parent = {}
            id_to_rank = {}
            with open(taxonomy, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id_to_name[row['id']] = row['name']
                    id_to_parent[row['id']] = row['parent_id']
                    id_to_rank[row['id']] = row['rank']
            # Parse seqinfo file
            with open(seqinfo, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or len(row) < 2:
                        continue
                    seqname, taxid = row[0], row[1]
                    # Build taxonomy string for this tip
                    lineage = []
                    current = taxid
                    while current and current in id_to_name:
                        lineage.append(id_to_name[current])
                        current = id_to_parent[current]
                    lineage = lineage[::-1]
                    self.taxonomy[seqname] = ";".join(lineage)
                    self.seqinfo[seqname] = taxid
            # Set ranks
            self.taxonomy_ranks = []
            # Try to get ranks from one lineage
            for seqname in self.taxonomy:
                taxid = self.seqinfo[seqname]
                ranks = []
                current = taxid
                while current and current in id_to_rank:
                    ranks.append(id_to_rank[current])
                    current = id_to_parent[current]
                self.taxonomy_ranks = ranks[::-1]
                break
        else:
            # Greengenes format
            with open(taxonomy) as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split('\t')
                    if len(parts) < 2:
                        continue
                    seqname, taxstr = parts[0], parts[1]
                    self.taxonomy[seqname] = taxstr
            # Try to infer ranks from first taxonomy string
            for seqname in self.taxonomy:
                taxstr = self.taxonomy[seqname]
                if taxstr:
                    self.taxonomy_ranks = ["rank%d" %
                                           (i+1) for i in taxstr.split(";")]
                break
        # Map tip names to taxonomy
        for tip in self.tip_names:
            if tip in self.taxonomy:
                self.tip_taxonomy[tip] = self.taxonomy[tip]
            else:
                self.tip_taxonomy[tip] = ""

    def _write_consensus_strings(self, output):
        with open(output, 'w') as f:
            for tip in self.tree.leaf_node_iter():
                name = tip.taxon.label
                taxstr = self.tip_taxonomy.get(name, "")
                f.write(f"{name}\t{taxstr}\n")

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
        # DendroPy: node.label is the node name
        if node.label:
            if name not in node.label:
                node.label = f"{node.label}|{name}"
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
        # First, collect all tip taxonomy strings
        for tip in self.tree.leaf_node_iter():
            name = tip.taxon.label
            if name in self.taxonomy:
                self.tip_taxonomy[name] = self.taxonomy[name]
            else:
                self.tip_taxonomy[name] = ""

        # For unique_names, keep a counter for each group name
        name_counter = defaultdict(int)
        assigned_names = {}

        def get_consensus_taxonomy(node):
            # For a node, get the set of taxonomy strings for all descendant tips
            tips = [leaf.taxon.label for leaf in node.leaf_iter()]
            taxonomies = [self.tip_taxonomy.get(tip, "") for tip in tips]
            # Split taxonomy strings into lists
            split_tax = [tax.split(";") for tax in taxonomies if tax]
            if not split_tax:
                return None
            # Find consensus at each rank
            consensus = []
            for i in range(max(len(x) for x in split_tax)):
                ith = [x[i] for x in split_tax if len(x) > i]
                if ith and all(t == ith[0] for t in ith):
                    consensus.append(ith[0])
                else:
                    break
            if consensus:
                return ";".join(consensus)
            else:
                return None

        def assign_names(node):
            if node.is_leaf():
                return
            consensus = get_consensus_taxonomy(node)
            if consensus:
                # If unique_names, append a number if this name is used more than once
                if unique_names:
                    name_counter[consensus] += 1
                    if name_counter[consensus] > 1:
                        name = f"{consensus}_{name_counter[consensus]}"
                    else:
                        name = consensus
                else:
                    name = consensus
                self._rename(node, name)
                assigned_names[node] = name
            for child in node.child_node_iter():
                assign_names(child)

        assign_names(self.tree.seed_node)

        # Write decorated tree
        self.tree.write(path=output_tree, schema="newick",
                        suppress_rooting=True)
        # Write taxonomy strings for each tip
        self._write_consensus_strings(output_tax)
