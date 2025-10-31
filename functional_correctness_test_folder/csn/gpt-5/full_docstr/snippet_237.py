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
        self.seqinfo_path = seqinfo
        self.taxonomy_path = taxonomy
        self.taxonomy_map = self._load_taxonomy_file(taxonomy)

    def _load_taxonomy_file(self, path):
        tx = {}
        if path is None:
            return tx
        import csv
        # Try TSV first, then CSV
        with open(path, "r", newline="") as fh:
            sample = fh.read(4096)
            fh.seek(0)
            dialect = None
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters="\t,;")
            except Exception:
                pass
            if dialect is not None:
                reader = csv.reader(fh, dialect)
            else:
                reader = (line.rstrip("\n") for line in fh)
                reader = (l.split("\t") if "\t" in l else l.split(",")
                          for l in reader)
            for row in reader:
                if not row:
                    continue
                if isinstance(row, str):
                    row = [r for r in row.split("\t") if r] or [
                        r for r in row.split(",") if r]
                # Expect at least two columns: id and taxonomy string
                if len(row) == 1:
                    # Try to split on whitespace between id and taxonomy
                    parts = row[0].strip().split(None, 1)
                    if len(parts) == 2:
                        key, val = parts
                    else:
                        # Skip malformed lines
                        continue
                else:
                    key = row[0].strip()
                    val = row[1].strip()
                if not key:
                    continue
                # Normalize taxonomy separators to "; " and strip parts
                parts = [p.strip() for p in self._split_tax_string(val)]
                if parts:
                    tx[key] = parts
        return tx

    def _split_tax_string(self, s):
        if s is None:
            return []
        # Accept separators like ';', '; ', '|', or ',' (but avoid splitting on commas within names if quoted)
        raw = [seg for seg in s.replace("|", ";").split(";")]
        cleaned = []
        for seg in raw:
            seg = seg.strip()
            if not seg:
                continue
            cleaned.append(seg)
        return cleaned

    def _tip_name(self, node):
        # Try common dendropy attributes to get the tip name
        name = None
        try:
            if getattr(node, "taxon", None) is not None:
                name = getattr(node.taxon, "label", None)
        except Exception:
            name = None
        if not name:
            name = getattr(node, "label", None)
        if not name:
            name = getattr(node, "leaf_label", None)
        return name

    def _is_leaf(self, node):
        try:
            return node.is_leaf()
        except Exception:
            # Fallback: no children means leaf
            ch = getattr(node, "child_nodes", None)
            if callable(ch):
                return len(ch()) == 0
            children = getattr(node, "child_nodes", []) or getattr(
                node, "children", [])
            try:
                return len(children) == 0
            except Exception:
                return False

    def _iter_leaves(self):
        # DendroPy provides leaf_node_iter
        try:
            yield from self.tree.leaf_node_iter()
            return
        except Exception:
            pass
        try:
            for n in self.tree.leaf_nodes():
                yield n
            return
        except Exception:
            pass
        # Fallback: traverse all nodes and yield leaves
        yield from (n for n in self._postorder_nodes() if self._is_leaf(n))

    def _postorder_nodes(self):
        try:
            yield from self.tree.postorder_node_iter()
            return
        except Exception:
            pass
        # Fallback: recursive traversal from seed/root
        root = getattr(self.tree, "seed_node", None) or getattr(
            self.tree, "root", None)
        if root is None:
            return
        yield from self._postorder_from(root)

    def _children(self, node):
        ch_meth = getattr(node, "child_nodes", None)
        if callable(ch_meth):
            return list(ch_meth())
        children = getattr(node, "child_nodes", None)
        if children is None:
            children = getattr(node, "children", [])
        return list(children) if children is not None else []

    def _parent(self, node):
        return getattr(node, "parent_node", None) or getattr(node, "parent", None)

    def _postorder_from(self, node):
        for c in self._children(node):
            yield from self._postorder_from(c)
        yield node

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
        with open(output, "w") as out:
            for leaf in self._iter_leaves():
                name = self._tip_name(leaf) or ""
                tparts = self.taxonomy_map.get(name, None)
                if not tparts:
                    # Build from ancestor annotations
                    tparts = self._taxonomy_from_ancestors(leaf)
                tx_str = "; ".join(tparts) if tparts else ""
                out.write(f"{name}\t{tx_str}\n")

    def _taxonomy_from_ancestors(self, leaf):
        # Walk from root towards leaf collecting annotation labels
        parts = []
        seen = set()
        # Build path to root
        chain = []
        n = self._parent(leaf)
        while n is not None:
            chain.append(n)
            n = self._parent(n)
        for node in reversed(chain):
            lbl = getattr(node, "label", None)
            if not lbl:
                continue
            ann = self._extract_annotation_from_label(lbl)
            if not ann:
                continue
            if ann not in seen:
                parts.append(ann)
                seen.add(ann)
        return parts

    def _extract_annotation_from_label(self, label):
        # If bootstrap-like numeric with annotation after ":", take the suffix
        if ":" in label:
            # assume everything after the first ":" is annotation; trim spaces
            candidate = label.split(":", 1)[1].strip()
            if candidate:
                return candidate
        # Otherwise, if label contains semicolons, take last segment as annotation name
        if ";" in label:
            segs = [s.strip() for s in label.split(";") if s.strip()]
            if segs:
                return segs[-1]
        # If the label is purely numeric, treat as bootstrap only
        import re
        if re.fullmatch(r"\s*-?\d+(\.\d+)?\s*", label):
            return ""
        return label.strip()

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
        current = getattr(node, "label", None)
        if not current:
            node.label = name
            return
        import re
        if re.fullmatch(r"\s*-?\d+(\.\d+)?\s*", current):
            node.label = f"{current}:{name}"
            return
        # If already has "bootstrap:annotation" form, append "; name" to annotation part
        if ":" in current:
            left, right = current.split(":", 1)
            right = right.strip()
            if right:
                node.label = f"{left}:{right}; {name}"
            else:
                node.label = f"{left}:{name}"
            return
        # Otherwise append with semicolon
        node.label = f"{current}; {name}"

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
        # Preload leaf taxonomy lists
        leaf_tax_lists = {}
        for leaf in self._iter_leaves():
            nm = self._tip_name(leaf)
            parts = self.taxonomy_map.get(nm, [])
            leaf_tax_lists[leaf] = parts

        # Helper to get descendant leaf taxonomy lists for a node
        def descendant_tax_lists(node):
            # collect leaves below node
            stack = [node]
            lists = []
            while stack:
                cur = stack.pop()
                if self._is_leaf(cur):
                    lists.append(leaf_tax_lists.get(cur, []))
                else:
                    stack.extend(self._children(cur))
            return lists

        def common_prefix(list_of_lists):
            if not list_of_lists:
                return []
            # Filter out empty lists
            nonempty = [lst for lst in list_of_lists if lst]
            if not nonempty:
                return []
            # Compute shared prefix across all lists
            prefix = []
            idx = 0
            while True:
                # Check that all lists have idx and equal element
                try:
                    cand = nonempty[0][idx]
                except IndexError:
                    break
                ok = True
                for lst in nonempty[1:]:
                    if len(lst) <= idx or lst[idx] != cand:
                        ok = False
                        break
                if not ok:
                    break
                prefix.append(cand)
                idx += 1
            return prefix

        name_counts = {}
        # Postorder so children evaluated before parents
        for node in self._postorder_nodes():
            if self._is_leaf(node):
                continue
            lists = descendant_tax_lists(node)
            prefix = common_prefix(lists)
            if not prefix:
                continue
            base = prefix[-1]
            if unique_names:
                cnt = name_counts.get(base, 0) + 1
                name_counts[base] = cnt
                name = f"{base}" if cnt == 1 else f"{base}_{cnt}"
            else:
                name = base
            self._rename(node, name)

        # Write outputs
        # Tree
        wrote = False
        try:
            # DendroPy-style
            self.tree.write(path=output_tree, schema="newick")
            wrote = True
        except Exception:
            try:
                with open(output_tree, "w") as fh:
                    fh.write(str(self.tree))
                wrote = True
            except Exception:
                wrote = False
        # Taxonomy strings per leaf
        self._write_consensus_strings(output_tax)
        return wrote
