class NodeFinder:

    def __init__(self, matcher, limit=0):
        self.matcher = matcher
        self.limit = int(limit) if limit is not None else 0

    def _matches(self, node):
        if node is None:
            return False
        m = self.matcher
        try:
            if hasattr(m, "match") and callable(m.match):
                return bool(m.match(node))
            if callable(m):
                return bool(m(node))
        except Exception:
            return False
        return False

    def _iter_children(self, node):
        if node is None:
            return
        # Try Python ast nodes
        try:
            import ast
            if isinstance(node, ast.AST):
                for child in ast.iter_child_nodes(node):
                    if child is not None:
                        yield child
                return
        except Exception:
            pass

        # Objects with 'children' attribute
        if hasattr(node, "children"):
            try:
                for child in getattr(node, "children"):
                    if child is not None:
                        yield child
                return
            except Exception:
                pass

        # Generic iterables (avoid strings/bytes)
        if isinstance(node, (list, tuple)):
            for child in node:
                if child is not None:
                    yield child
            return

        try:
            if hasattr(node, "__iter__") and not isinstance(node, (str, bytes, bytearray)):
                for child in node:
                    if child is not None:
                        yield child
                return
        except Exception:
            pass

    def find(self, node, list):
        if node is None:
            return
        if self.limit and len(list) >= self.limit:
            return

        if self._matches(node):
            list.append(node)
            if self.limit and len(list) >= self.limit:
                return

        for child in self._iter_children(node) or ():
            if self.limit and len(list) >= self.limit:
                return
            self.find(child, list)
