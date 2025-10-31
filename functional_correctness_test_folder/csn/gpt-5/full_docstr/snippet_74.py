class PlainName:
    '''
    plain name scope provider
    '''

    def __init__(self, multi_metamodel_support=True):
        '''
        the default scope provider constructor
        Args:
            multi_metamodel_support: enable a AST based search, instead
            of using the parser._instances
        '''
        self.multi_metamodel_support = bool(multi_metamodel_support)

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
        # Helper getters
        def _get_name(o):
            for n in ("obj_name", "name", "id"):
                if hasattr(o, n):
                    return getattr(o, n)
            if isinstance(o, str):
                return o
            return None

        def _get_expected_classes():
            candidates = []
            for holder in (obj_ref, attr):
                if holder is None:
                    continue
                for n in ("cls", "type", "expected_cls", "expected_type"):
                    if hasattr(holder, n):
                        c = getattr(holder, n)
                        if c is not None:
                            candidates.append(c)
                # Some frameworks store multiple acceptable classes
                for n in ("classes", "types", "expected_classes", "expected_types"):
                    if hasattr(holder, n):
                        cs = getattr(holder, n)
                        if cs:
                            candidates.extend(cs if isinstance(
                                cs, (list, tuple, set)) else [cs])
            # Deduplicate while preserving order
            seen = set()
            result = []
            for c in candidates:
                if isinstance(c, type) and c not in seen:
                    seen.add(c)
                    result.append(c)
            return tuple(result)

        def _root_of(o):
            # Try textX-like ancestry first
            visited = set()
            cur = o
            while True:
                if cur is None:
                    break
                obj_id = id(cur)
                if obj_id in visited:
                    break
                visited.add(obj_id)
                parent = getattr(cur, "_tx_parent", None)
                if parent is None:
                    break
                cur = parent
            # Prefer model root if available
            model = getattr(cur, "_tx_model", None) or getattr(
                o, "_tx_model", None)
            return model or cur

        def _iter_elements(root):
            # Generic DFS over Python object graphs while avoiding cycles
            stack = [root]
            seen = set()
            while stack:
                cur = stack.pop()
                oid = id(cur)
                if oid in seen:
                    continue
                seen.add(oid)
                # Yield only "element-like" objects (instances with dict)
                if hasattr(cur, "__dict__"):
                    yield cur
                    # Explore attributes
                    for k, v in vars(cur).items():
                        if k.startswith("_tx_"):
                            # Still dive into some known textX graph links
                            if k in ("_tx_children", "_tx_model_repository"):
                                pass
                            else:
                                # Skip common internal attributes
                                continue
                        _push_value(v, stack)
                elif isinstance(cur, (list, tuple, set, frozenset)):
                    for v in cur:
                        _push_value(v, stack)
                elif isinstance(cur, dict):
                    for v in cur.values():
                        _push_value(v, stack)

        def _push_value(v, stack):
            if v is None:
                return
            if isinstance(v, (str, bytes, int, float, bool)):
                return
            stack.append(v)

        def _match_expected(o, expected_types):
            if not expected_types:
                return True
            return any(isinstance(o, t) for t in expected_types)

        def _resolve_dotted_from_scope(scope_root, expected_types, dotted_name):
            parts = [p for p in str(dotted_name).split(".") if p]
            if not parts:
                return None
            # Find candidates for the first part in the entire scope
            first = parts[0]

            def _children_of(node):
                # Iterate over direct children of a node
                for k, v in vars(node).items() if hasattr(node, "__dict__") else []:
                    if k.startswith("_tx_"):
                        continue
                    if isinstance(v, (list, tuple, set, frozenset)):
                        for it in v:
                            if hasattr(it, "__dict__"):
                                yield it
                    elif hasattr(v, "__dict__"):
                        yield v

            def _find_all_named(root, name):
                for e in _iter_elements(root):
                    if _get_name(e) == name:
                        yield e

            def _resolve_from(node, idx):
                if idx >= len(parts):
                    return node
                target_name = parts[idx]
                # Search among node's children for next name
                for child in _children_of(node):
                    if _get_name(child) == target_name:
                        if idx == len(parts) - 1:
                            return child if _match_expected(child, expected_types) else None
                        found = _resolve_from(child, idx + 1)
                        if found is not None:
                            return found
                return None

            for candidate in _find_all_named(scope_root, first):
                if len(parts) == 1:
                    if _match_expected(candidate, expected_types):
                        return candidate
                    continue
                res = _resolve_from(candidate, 1)
                if res is not None and _match_expected(res, expected_types):
                    return res
            return None

        def _resolve_via_parser_instances(parser, expected_types, name):
            instances = getattr(parser, "_instances", None)
            if not instances:
                return None
            # instances can be dict[type] -> set/list of instances
            # Prefer expected types if provided, else search all
            if expected_types:
                search_types = [t for t in expected_types if t in instances]
            else:
                search_types = list(instances.keys())
            for t in search_types:
                try:
                    for inst in instances.get(t, []):
                        if _get_name(inst) == name:
                            return inst
                except Exception:
                    continue
            # Fallback: scan all instances if nothing found
            if not expected_types:
                for bucket in instances.values():
                    try:
                        for inst in bucket:
                            if _get_name(inst) == name:
                                return inst
                    except Exception:
                        continue
            return None

        # Actual resolution
        obj_name = _get_name(obj_ref)
        if not obj_name:
            return None

        expected_types = _get_expected_classes()

        # Dotted names first using AST when enabled
        if self.multi_metamodel_support:
            root = _root_of(obj)
            if "." in str(obj_name):
                found = _resolve_dotted_from_scope(
                    root, expected_types, obj_name)
                if found is not None:
                    return found
            # Plain name search across AST
            for element in _iter_elements(root):
                if _get_name(element) == obj_name and _match_expected(element, expected_types):
                    return element
            return None

        # Parser instances based resolution
        parser = None
        model = getattr(obj, "_tx_model", None)
        if model is not None:
            parser = getattr(model, "_tx_parser", None)
        if parser is not None:
            if "." in str(obj_name):
                # Try dotted name by stepwise filtering via instances/AST hybrid:
                # fall back to AST if dotted and instances are insufficient
                root = _root_of(obj)
                found = _resolve_dotted_from_scope(
                    root, expected_types, obj_name)
                if found is not None:
                    return found
            # Plain via instances
            found = _resolve_via_parser_instances(
                parser, expected_types, obj_name)
            if found is not None:
                return found

        # Final fallback: AST scan even if multi_metamodel_support is False
        root = _root_of(obj)
        if "." in str(obj_name):
            found = _resolve_dotted_from_scope(root, expected_types, obj_name)
            if found is not None:
                return found
        for element in _iter_elements(root):
            if _get_name(element) == obj_name and _match_expected(element, expected_types):
                return element
        return None

        def _inner_resolve_link_rule_ref(cls, obj_name):
            '''
            Depth-first resolving of link rule reference.
            '''
            # Kept for backward-compatibility; not used due to the more general resolver above.
            root = _root_of(obj)
            if "." in str(obj_name):
                return _resolve_dotted_from_scope(root, (cls,) if isinstance(cls, type) else tuple(cls or []), obj_name)
            # Plain name
            for element in _iter_elements(root):
                if _get_name(element) == obj_name and (cls is None or isinstance(element, cls)):
                    return element
            return None
