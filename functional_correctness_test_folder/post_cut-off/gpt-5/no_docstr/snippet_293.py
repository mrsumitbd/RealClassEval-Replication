class KNNModel:

    def __init__(self, items, k=3):
        self.k = int(k) if k is not None else 3
        self.keys = []
        self.embs = []
        self.dim = None

        if isinstance(items, dict):
            iterator = items.items()
        else:
            iterator = items

        for idx, item in enumerate(iterator):
            if isinstance(items, dict):
                key, emb = item
            else:
                # item could be (key, emb) or just emb
                if isinstance(item, (list, tuple)) and len(item) == 2 and hasattr(item[1], "__iter__"):
                    key, emb = item
                else:
                    key, emb = idx, item

            emb_tuple = tuple(float(x) for x in emb)
            if self.dim is None:
                if len(emb_tuple) == 0:
                    raise ValueError("Embeddings must be non-empty sequences.")
                self.dim = len(emb_tuple)
            elif len(emb_tuple) != self.dim:
                raise ValueError(
                    "All embeddings must have the same dimension.")
            self.keys.append(key)
            self.embs.append(emb_tuple)

        if not self.embs:
            raise ValueError("Items must contain at least one embedding.")

    def neighbors(self, target_emb, k=None):
        if k is None:
            k = self.k
        k = max(0, int(k))
        if k == 0:
            return []

        target = tuple(float(x) for x in target_emb)
        if len(target) != self.dim:
            raise ValueError(
                f"Target embedding dimension {len(target)} does not match model dimension {self.dim}.")

        # Compute squared Euclidean distances
        def sq_dist(a, b):
            return sum((ai - bi) ** 2 for ai, bi in zip(a, b))

        distances = []
        for key, emb in zip(self.keys, self.embs):
            d2 = sq_dist(target, emb)
            distances.append((key, d2))

        # Select k smallest distances
        if k >= len(distances):
            selected = sorted(distances, key=lambda x: x[1])
        else:
            import heapq
            selected = heapq.nsmallest(k, distances, key=lambda x: x[1])

        # Return with actual Euclidean distances
        result = [(key, d2 ** 0.5) for key, d2 in selected]
        return result
