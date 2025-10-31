class KNNModel:
    def __init__(self, items, k=3):
        self.k = int(k) if k is not None else 3
        self._items = []
        # Normalize input formats:
        # - Mapping[id] -> embedding
        # - Sequence[(id, embedding)]
        # - Sequence[embedding] -> ids are indices

        def is_mapping(obj):
            try:
                return hasattr(obj, "items")
            except Exception:
                return False

        if is_mapping(items):
            iterable = items.items()
        else:
            # Determine if items look like (id, emb) pairs
            iterable = []
            as_pairs = False
            try:
                if len(items) > 0:
                    first = items[0]
                    if isinstance(first, (list, tuple)) and len(first) == 2 and not all(
                        isinstance(x, (int, float)) for x in first
                    ):
                        as_pairs = True
            except Exception:
                pass
            if as_pairs:
                iterable = items
            else:
                iterable = [(idx, emb) for idx, emb in enumerate(items)]

        # Build normalized vectors; skip zero-norm or invalid embeddings
        def normalize(vec):
            s = 0.0
            for v in vec:
                s += float(v) * float(v)
            if s <= 0.0:
                return None
            inv = s ** -0.5
            return [float(v) * inv for v in vec]

        dims = None
        for item_id, emb in iterable:
            try:
                norm = normalize(emb)
            except Exception:
                continue
            if norm is None:
                continue
            if dims is None:
                dims = len(norm)
            if len(norm) != dims:
                continue
            self._items.append((item_id, norm))

    def neighbors(self, target_emb, k=None):
        '''
        Retrieve k nearest neighbors by cosine distance.
        :param target_emb: Query embedding vector.
        :type target_emb: Sequence[float]
        :param k: Override number of neighbors (defaults to self.k).
        :type k: int
        :return: List of (item_id, distance) pairs ordered by proximity.
        :rtype: List[Tuple[Any, float]]
        '''
        if not self._items:
            return []
        # Normalize target
        s = 0.0
        try:
            for v in target_emb:
                s += float(v) * float(v)
        except Exception:
            return []
        if s <= 0.0:
            return []
        inv = s ** -0.5
        target = [float(v) * inv for v in target_emb]
        dims = len(self._items[0][1])
        if len(target) != dims:
            return []

        # Compute cosine distance = 1 - dot(normalized)
        def dot(a, b):
            return sum(x * y for x, y in zip(a, b))

        n = len(self._items)
        kk = n if k is None else max(0, min(int(k), n))
        if kk == 0:
            kk = min(self.k if isinstance(self.k, int)
                     and self.k > 0 else 1, n)

        dists = []
        for item_id, vec in self._items:
            sim = dot(target, vec)
            if sim > 1.0:
                sim = 1.0
            elif sim < -1.0:
                sim = -1.0
            dist = 1.0 - sim
            dists.append((item_id, dist))

        # Select k smallest distances
        if kk >= len(dists):
            dists.sort(key=lambda x: x[1])
            return dists
        else:
            import heapq
            smallest = heapq.nsmallest(kk, dists, key=lambda x: x[1])
            smallest.sort(key=lambda x: x[1])
            return smallest
