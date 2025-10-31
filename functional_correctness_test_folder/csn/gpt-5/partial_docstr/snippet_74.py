class PlainName:

    def __init__(self, multi_metamodel_support=True):
        '''
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        '''
        self.multi_metamodel_support = multi_metamodel_support

    def __call__(self, obj, attr, obj_ref):
        '''
        the default scope provider
        Args:
            obj: unused (used for multi_metamodel_support)
            attr: unused
            obj_ref: the cross reference to be resolved
        Returns:
            the resolved reference or None
        '''
        def extract_name(ref):
            if ref is None:
                return None
            # textX style Reference has obj_name
            n = getattr(ref, 'obj_name', None)
            if n is not None:
                return n
            # direct string reference
            if isinstance(ref, str):
                return ref
            # fallbacks
            n = getattr(ref, 'name', None)
            if isinstance(n, str):
                return n
            return None

        def get_root(node):
            cur = node
            # textX sets _tx_parent on contained objects
            while True:
                parent = getattr(cur, '_tx_parent', None)
                if parent is None:
                    break
                cur = parent
            return cur

        def is_primitive(v):
            return isinstance(v, (str, bytes, int, float, bool))

        def iter_children(node):
            if node is None:
                return
            # Iterate over attributes except private/textX meta ones
            for k, v in vars(node).items():
                if k.startswith('_tx_'):
                    continue
                if is_primitive(v) or v is None:
                    continue
                if isinstance(v, (list, tuple)):
                    for it in v:
                        if not is_primitive(it) and hasattr(it, '__dict__'):
                            yield it
                else:
                    if hasattr(v, '__dict__'):
                        yield v

        def get_name(o):
            for candidate in ('name', 'id'):
                if hasattr(o, candidate):
                    n = getattr(o, candidate)
                    if isinstance(n, str):
                        return n
            return None

        def find_by_name(root_obj, target_name):
            # Simple DFS search by name
            visited = set()
            stack = [root_obj]
            while stack:
                cur = stack.pop()
                oid = id(cur)
                if oid in visited:
                    continue
                visited.add(oid)
                n = get_name(cur)
                if n == target_name:
                    return cur
                # push children
                for ch in iter_children(cur):
                    stack.append(ch)
            return None

        def find_qualified(root_obj, parts):
            # Resolve a qualified name like A.B.C by descending containment
            # Start with all candidates matching first part anywhere, then descend.
            first = parts[0]
            visited = set()
            # Gather all with name == first
            candidates = []
            stack = [root_obj]
            while stack:
                cur = stack.pop()
                oid = id(cur)
                if oid in visited:
                    continue
                visited.add(oid)
                if get_name(cur) == first:
                    candidates.append(cur)
                for ch in iter_children(cur):
                    stack.append(ch)
            if not candidates:
                return None
            # Descend for remaining parts
            for p in parts[1:]:
                next_candidates = []
                for c in candidates:
                    for ch in iter_children(c):
                        if get_name(ch) == p:
                            next_candidates.append(ch)
                if not next_candidates:
                    return None
                candidates = next_candidates
            return candidates[0] if candidates else None

        def search_using_instances(model_like, target_name):
            # model_like may expose parser._instances as {rule: [objs]}
            try:
                parser = getattr(model_like, 'parser', None)
                if parser is None:
                    return None
                instances = getattr(parser, '_instances', None)
                if not instances:
                    return None
                # Flatten and search
                for coll in instances.values():
                    for inst in coll:
                        if get_name(inst) == target_name:
                            return inst
                return None
            except Exception:
                return None

        def _inner_resolve_link_rule_ref(cls, obj_name):
            '''
            Depth-first resolving of link rule reference.
            '''
            if not obj_name:
                return None
            parts = obj_name.split('.')
            if not parts:
                return None
            # If cls is provided as a root to start from, use it directly.
            # Otherwise, fall back to searching from the overall root.
            start = cls if cls is not None else get_root(obj)
            if len(parts) == 1:
                return find_by_name(start, parts[0])
            return find_qualified(start, parts)

        name = extract_name(obj_ref)
        if not name:
            return None

        # Resolve qualified names via inner link-rule resolver
        if '.' in name:
            return _inner_resolve_link_rule_ref(obj, name)

        # Try fast path using instances when multi_metamodel_support is False
        if not self.multi_metamodel_support:
            # Attempt to locate model's parser instances
            tx_model = getattr(obj, '_tx_model', None)
            resolved = None
            if tx_model is not None:
                resolved = search_using_instances(tx_model, name)
            if resolved is not None:
                return resolved
            # Fallback to root search
            return find_by_name(get_root(obj), name)

        # multi_metamodel_support: AST-based search from root
        root = get_root(obj)
        return find_by_name(root, name)
