
import collections
from Bio import Phylo
from io import StringIO


class TreeDecorator:
    """
    Decorate a phylogenetic tree with taxonomy information.

    Parameters
    ----------
    tree : Bio.Phylo.BaseTree.Tree
        The tree to decorate.
    taxonomy : dict
        Mapping from tip names to taxonomy strings.
    seqinfo : dict, optional
        Optional mapping from tip names to additional information (unused
        in this implementation but kept for compatibility).
    """

    def __init__(self, tree, taxonomy, seqinfo=None):
        self.tree = tree
        self.taxonomy = taxonomy
        self.seqinfo = seqinfo or {}
        # Counter for unique names
        self.name_counts = collections.Counter()

    def _write_consensus_strings(self, output):
        """
        Write taxonomy strings for each tip in the tree to the given file-like
        object.

        Parameters
        ----------
        output : file-like
            File object opened for writing.
        """
        for tip in self.tree.get_terminals():
            tax = self.taxonomy.get(tip.name, "")
            output.write(f"{tip.name}\t{tax}\n")

    def _rename(self, node, name):
        """
        Rename a node in the tree.

        Parameters
        ----------
        node : Bio.Phylo.BaseTree.Clade
            The node to rename.
        name : str
            The new name for the node.
        """
        node.name = name

    def _consensus_taxonomy(self, clade):
        """
        Recursively compute the consensus taxonomy for a clade.

        Returns
        -------
        tax : str or None
            The consensus taxonomy string if all descendant tips share the
            same taxonomy; otherwise None.
        """
        if clade.is_terminal():
            return self.taxonomy.get(clade.name, None)

        child_taxes = [self._consensus_taxonomy(
            child) for child in clade.clades]
        # If any child returned None, propagate None
        if any(t is None for t in child_taxes):
            return None

        # All child taxes are strings; check if they are identical
        if all(t == child_taxes[0] for t in child_taxes):
            return child_taxes[0]
        return None

    def _decorate_node(self, clade, unique_names):
        """
        Decorate a node with taxonomy information.

        Parameters
        ----------
        clade : Bio.Phylo.BaseTree.Clade
            The node to decorate.
        unique_names : bool
            If True, append a unique counter to duplicate names.
        """
        if clade.is_terminal():
            # Terminal nodes keep their original names
            return

        # Decorate children first
        for child in clade.clades:
            self._decorate_node(child, unique_names)

        # Compute consensus taxonomy for this clade
        tax = self._consensus_taxonomy(clade)

        if tax is not None:
            # Use taxonomy as node name
            name = tax
            if unique_names:
                count = self.name_counts[name]
                if count > 0:
                    name = f"{tax}_{count}"
                self.name_counts[tax] += 1
            self._rename(clade, name)
        else:
            # If no consensus, leave node unnamed (or set to None)
            self._rename(clade, None)

    def decorate(self, output_tree, output_tax, unique_names):
        """
        Decorate a tree with taxonomy. This code does not allow inconsistent
        taxonomy within a clade. If one sequence in a clade has a different
        annotation to the rest, it will split the clade. Paraphyletic group
        names are distinguished if unique_names = True using a simple tally of
        each group (see unique_names below).

        Parameters
        ----------
        output_tree : str
            File to which the decorated tree will be written.
        output_tax : str
            File to which the taxonomy strings for each tip in the tree will be
            written.
        unique_names : bool
            True indicating that a unique number will be appended to the end of
            a taxonomic rank if it is found more than once in the tree
            (i.e. it is paraphyletic in the tree). If false, multiple clades
            may be assigned with the same name.
        """
        # Decorate the tree
        self._decorate_node(self.tree.root, unique_names)

        # Write decorated tree to file
        with open(output_tree, "w") as f:
            Phylo.write(self.tree, f, "newick")

        # Write taxonomy strings for each tip
        with open(output_tax, "w") as f:
            self._write_consensus_strings(f)
