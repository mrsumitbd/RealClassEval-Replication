class PlainName:
    def __init__(self, multi_metamodel_support=True):
        self.multi_metamodel_support = bool(multi_metamodel_support)

    def __call__(self, obj, attr, obj_ref):
        def _inner_resolve_link_rule_ref(cls_name, obj_name):
            return _resolve_by_name(root, obj_name, type_name=cls_name)

        if obj_ref is None:
            return None

        if not hasattr(obj, "__dict__") and not isinstance(obj, (list, tuple, dict, set)):
            return None

        if not isinstance(attr, str):
            attr = str(attr)

        if not isinstance(obj_ref, str):
            # Already an object; return as-is
            return obj_ref

        # Determine root container by following parent-like links
        root = obj
        visited_ids = set()
        while True:
            parent = None
            for parent_attr in ("parent", "__parent__", "_parent"):
                if hasattr(root, parent_attr):
                    parent = getattr(root, parent_attr)
                    break
            if parent is None or id(parent) in visited_ids:
                break
            visited_ids.add(id(parent))
            root = parent

        # Parse possible "ClassName:name" or "ClassName#name" notation
        cls_name = None
        name_token = obj_ref
        if self.multi_metamodel_support and isinstance(obj_ref, str):
            if ":" in obj_ref:
                parts = obj_ref.split(":", 1)
                if parts[0] and parts[1]:
                    cls_name, name_token = parts[0].strip(), parts[1].strip()
            elif "#" in obj_ref:
                parts = obj_ref.split("#", 1)
                if parts[0] and parts[1]:
                    cls_name, name_token = parts[0].strip(), parts[1].strip()

        # Attempt dotted path resolution: a.b.c
        if "." in name_token:
            current = root
            for segment in name_token.split("."):
                current = _resolve_by_name(
                    current, segment, type_name=cls_name)
                if current is None:
                    break
                # After first segment, do not constrain by class name further
                cls_name = None
            return current

        # Plain name or with class constraint
        if cls_name:
            return _inner_resolve_link_rule_ref(cls_name, name_token)
        return _resolve_by_name(root, name_token)


def _is_primitive(x):
    return isinstance(x, (str, bytes, int, float, bool, complex))


def _iter_children(obj):
    seen = set()
    stack = [obj]
    while stack:
        cur = stack.pop()
        cid = id(cur)
        if cid in seen:
            continue
        seen.add(cid)

        if _is_primitive(cur):
            continue

        # Yield children depending on container type
        if isinstance(cur, dict):
            values = list(cur.values())
            for v in values:
                if not _is_primitive(v):
                    yield v
                    stack.append(v)
            continue

        if isinstance(cur, (list, tuple, set)):
            for v in cur:
                if not _is_primitive(v):
                    yield v
                    stack.append(v)
            continue

        # For objects with attributes
        if hasattr(cur, "__dict__"):
            for k, v in list(cur.__dict__.items()):
                if k.startswith("_"):
                    continue
                if callable(v):
                    continue
                if _is_primitive(v):
                    continue
                if isinstance(v, (list, tuple, set)):
                    for item in v:
                        if not _is_primitive(item):
                            yield item
                            stack.append(item)
                    continue
                if isinstance(v, dict):
                    for item in v.values():
                        if not _is_primitive(item):
                            yield item
                            stack.append(item)
                    continue
                yield v
                stack.append(v)


def _type_name(o):
    try:
        return type(o).__name__
    except Exception:
        return None


def _get_name(o):
    for attr in ("name", "id", "identifier"):
        if hasattr(o, attr):
            val = getattr(o, attr)
            if isinstance(val, str):
                return val
    return None


def _resolve_by_name(scope, name, type_name=None):
    # Breadth-first search for stability
    from collections import deque

    if scope is None:
        return None

    # Direct match if scope itself matches
    if not _is_primitive(scope) and hasattr(scope, "__dict__"):
        sname = _get_name(scope)
        if sname == name and (type_name is None or _type_name(scope) == type_name):
            return scope

    q = deque()
    seen = set()

    def enqueue(x):
        ix = id(x)
        if ix not in seen and not _is_primitive(x):
            seen.add(ix)
            q.append(x)

    enqueue(scope)

    while q:
        cur = q.popleft()

        # Iterate children
        for child in _iter_children(cur):
            # Check match
            cname = _get_name(child)
            if cname == name and (type_name is None or _type_name(child) == type_name):
                return child
            enqueue(child)

    return None
