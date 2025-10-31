import csv
import io
import os
import re
from collections import defaultdict
from typing import Dict, List, Optional

try:
    import dendropy
except ImportError as e:
    raise ImportError(
        "TreeDecorator requires the 'dendropy' package to be installed.") from e


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
        self.tree: dendropy.Tree = tree
        self.taxonomy_path: str = taxonomy
        self.seqinfo_path: Optional[str] = seqinfo

        # Map: tip label -> taxonomy string
        self.tip_to_taxonomy: Dict[str, str] = {}
        # Map: tip label -> taxonomy list (hierarchy)
        self.tip_to_taxlist: Dict[str, List[str]] = {}

        # Load taxonomy mapping
        if self.seqinfo_path:
            # Expect seqinfo as two columns: sequence, taxonomy
            self.tip_to_taxonomy = self._read_two_column_file(
                self.seqinfo_path)
        else:
            # Expect taxonomy file as two columns: sequence, taxonomy (Greengenes-like)
            self.tip_to_taxonomy = self._read_two_column_file(
                self.taxonomy_path)

        # Normalize taxonomy strings into lists
        for tip, tax in list(self.tip_to_taxonomy.items()):
            normalized = self._normalize_taxonomy_string(tax)
            self.tip_to_taxlist[tip] = normalized
            # Store back a normalized string with '; ' separators
            self.tip_to_taxonomy[tip] = '; '.join(normalized)

    def _read_two_column_file(self, path: str) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        if not os.path.exists(path):
            raise FileNotFoundError(f"Taxonomy/seqinfo file not found: {path}")

        def add_record(k, v):
            k = k.strip()
            v = v.strip()
            if k:
                mapping[k] = v

        with open(path, 'r', newline='') as fh:
            data = fh.read()

        # Try CSV/TSV with csv module first
        sniffer = csv.Sniffer()
        has_header = False
        dialect = None
        try:
            sample = data[:4096]
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)
        except Exception:
            # Fallback: try splitting lines manually
            dialect = None

        if dialect:
            reader = csv.reader(io.StringIO(data), dialect)
            first = True
            for row in reader:
                if not row:
                    continue
                if first and has_header:
                    first = False
                    continue
                first = False
                if len(row) == 1:
                    # Try to split by whitespace into two fields
                    parts = re.split(r'\s+', row[0], maxsplit=1)
                    if len(parts) == 2:
                        add_record(parts[0], parts[1])
                else:
                    add_record(row[0], row[1] if len(row) > 1 else '')
        else:
            # Manual parse: support tab, comma, or whitespace separated two columns
            for line in data.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '\t' in line:
                    parts = line.split('\t', 1)
                elif ',' in line:
                    parts = line.split(',', 1)
                else:
                    parts = re.split(r'\s+', line, maxsplit=1)
                if len(parts) == 2:
                    add_record(parts[0], parts[1])

        return mapping

    def _normalize_taxonomy_string(self, tax: str) -> List[str]:
        # Replace commas with semicolons if present, split on ';'
        if tax is None:
            return []
        s = tax.strip()
        if not s:
            return []
        s = s.replace(',', ';')
        parts = [p.strip() for p in s.split(';')]
        # Drop empty parts
        parts = [p for p in parts if p]
        return parts

    def _write_consensus_strings(self, output):
        with open(output, 'w', newline='') as fh:
            for tip, tax in sorted(self.tip_to_taxonomy.items()):
                fh.write(f"{tip}\t{tax}\n")

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
        if not name:
            return
        existing = node.label
        if existing is None or str(existing).strip() == '':
            node.label = name
            return
        existing_str = str(existing)
        # Determine if existing is numeric/bootstrap
        is_numeric = False
        try:
            float(existing_str)
            is_numeric = True
        except Exception:
            is_numeric = False
        if is_numeric:
            node.label = f"{existing_str}:{name}"
        else:
            node.label = f"{existing_str};{name}"

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
        # Write tip taxonomy table
        self._write_consensus_strings(output_tax)

        # Build a quick mapping from tip node names to taxonomy lists
        def tip_name(node):
            if node.taxon is not None and node.taxon.label:
                return node.taxon.label
            return node.label

        # Function to compute the common prefix taxonomy among a list of tax lists
        def common_prefix(lists: List[List[str]]) -> List[str]:
            if not lists:
                return []
            min_len = min(len(x) for x in lists)
            prefix = []
            for i in range(min_len):
                item = lists[0][i]
                if all((i < len(x) and x[i] == item) for x in lists):
                    prefix.append(item)
                else:
                    break
            return prefix

        used_names = defaultdict(int)

        # Postorder traversal ensures children processed before parents if needed
        for node in self.tree.postorder_node_iter():
            if node.is_leaf():
                continue
            leaves = node.leaf_nodes()
            tax_lists = []
            missing = False
            for lf in leaves:
                nm = tip_name(lf)
                if nm in self.tip_to_taxlist:
                    tax_lists.append(self.tip_to_taxlist[nm])
                else:
                    missing = True
                    break
            if missing or not tax_lists:
                continue
            prefix_list = common_prefix(tax_lists)
            if not prefix_list:
                continue
            base_name = '; '.join(prefix_list)
            final_name = base_name
            if unique_names:
                used_names[base_name] += 1
                cnt = used_names[base_name]
                if cnt > 1:
                    final_name = f"{base_name}_{cnt}"
            self._rename(node, final_name)

        # Write decorated tree
        # Ensure we write Newick labels as they are
        self.tree.write(path=output_tree, schema="newick",
                        suppress_rooting=False)
