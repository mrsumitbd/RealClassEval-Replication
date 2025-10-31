class TreeDecorator:

    class _Node:
        __slots__ = ("name", "children", "parent")

        def __init__(self, name=None, children=None, parent=None):
            self.name = name
            self.children = children if children is not None else []
            self.parent = parent

        def is_leaf(self):
            return not self.children

    def __init__(self, tree, taxonomy, seqinfo=None):
        # tree: Newick string or already-parsed _Node
        # taxonomy: dict {tip_name: "rank1;rank2;..."}
        self.seqinfo = seqinfo
        self.taxonomy = taxonomy if taxonomy is not None else {}
        if isinstance(tree, str):
            self.root = self._parse_newick(tree)
        elif isinstance(tree, TreeDecorator._Node):
            self.root = tree
        else:
            raise TypeError(
                "tree must be a Newick string or TreeDecorator._Node")

        # cache of leaves
        self._leaves = None

    def _write_consensus_strings(self, output):
        with open(output, "w", encoding="utf-8") as fh:
            for leaf in self._get_leaves():
                tax = self.taxonomy.get(leaf.name, "")
                fh.write(f"{leaf.name}\t{tax}\n")

    def _rename(self, node, name):
        node.name = name

    def decorate(self, output_tree, output_tax, unique_names):
        # Compute consensus taxonomy for internal nodes
        consensus_map = {}
        self._compute_consensus_for_all(self.root, consensus_map)

        # Assign names to internal nodes based on consensus
        name_counts = {}
        for node, consensus in consensus_map.items():
            if not node.is_leaf():
                # choose the deepest rank in consensus as the node label
                label = consensus.split(";")[-1] if consensus else ""
                if label:
                    if unique_names:
                        c = name_counts.get(label, 0) + 1
                        name_counts[label] = c
                        if c > 1:
                            label = f"{label}_{c}"
                    self._rename(node, label)

        # Write tree
        with open(output_tree, "w", encoding="utf-8") as fh:
            fh.write(self._to_newick(self.root) + ";\n")

        # Write tip taxonomy
        self._write_consensus_strings(output_tax)

    # --------- Internal helpers ----------

    def _get_leaves(self):
        if self._leaves is None:
            self._leaves = []
            self._collect_leaves(self.root, self._leaves)
        return self._leaves

    def _collect_leaves(self, node, acc):
        if node.is_leaf():
            acc.append(node)
        else:
            for ch in node.children:
                self._collect_leaves(ch, acc)

    def _compute_consensus_for_all(self, node, consensus_map):
        if node.is_leaf():
            tax = self.taxonomy.get(node.name, "")
            consensus_map[node] = tax
            return tax

        child_cons = [self._compute_consensus_for_all(
            ch, consensus_map) for ch in node.children]
        consensus = self._common_prefix(child_cons)
        consensus_map[node] = consensus
        return consensus

    def _common_prefix(self, tax_strings):
        # tax_strings: list of semicolon-separated strings
        if not tax_strings:
            return ""
        split_lists = [s.split(";") if s else [] for s in tax_strings]
        # find the longest prefix where all are equal and non-empty
        min_len = min((len(l) for l in split_lists), default=0)
        prefix = []
        for i in range(min_len):
            vals = {l[i] for l in split_lists}
            if len(vals) == 1 and list(vals)[0] != "":
                prefix.append(list(vals)[0])
            else:
                break
        return ";".join(prefix)

    def _to_newick(self, node):
        if node.is_leaf():
            return self._escape_name(node.name or "")
        else:
            kids = ",".join(self._to_newick(ch) for ch in node.children)
            label = self._escape_name(node.name) if node.name else ""
            return f"({kids}){label}"

    def _escape_name(self, name):
        if name is None:
            return ""
        # Minimal escaping: replace spaces with underscores
        return str(name).replace(" ", "_")

    def _parse_newick(self, newick):
        s = newick.strip()
        if not s.endswith(";"):
            # allow missing semicolon
            s = s + ";"
        idx = 0

        def parse_subtree():
            nonlocal idx
            if s[idx] == "(":
                idx += 1  # skip '('
                children = []
                while True:
                    child = parse_subtree()
                    children.append(child)
                    if s[idx] == ",":
                        idx += 1
                        continue
                    elif s[idx] == ")":
                        idx += 1
                        break
                    else:
                        raise ValueError("Invalid Newick: expected ',' or ')'")
                # optional name after ')'
                name = parse_name()
                node = TreeDecorator._Node(name=name, children=children)
                for ch in children:
                    ch.parent = node
                # optional branch length ':...' ignored
                if idx < len(s) and s[idx] == ":":
                    skip_branch_length()
                return node
            else:
                # leaf name
                name = parse_name(mandatory=True)
                node = TreeDecorator._Node(name=name)
                # optional branch length ':...' ignored
                if idx < len(s) and s[idx] == ":":
                    skip_branch_length()
                return node

        def parse_name(mandatory=False):
            nonlocal idx
            start = idx
            # read until comma, parenthesis, colon, or semicolon
            while idx < len(s) and s[idx] not in [",", ")", "(", ":", ";"]:
                idx += 1
            name = s[start:idx].strip()
            if mandatory and name == "":
                raise ValueError("Invalid Newick: missing leaf name")
            return name if name != "" else None

        def skip_branch_length():
            nonlocal idx
            if idx < len(s) and s[idx] == ":":
                idx += 1
                while idx < len(s) and s[idx] not in [",", ")", ";"]:
                    idx += 1

        root = parse_subtree()
        # skip following semicolon
        while idx < len(s) and s[idx] != ";":
            # allow trailing spaces/comments ignored
            idx += 1
        if idx < len(s) and s[idx] == ";":
            idx += 1
        return root
