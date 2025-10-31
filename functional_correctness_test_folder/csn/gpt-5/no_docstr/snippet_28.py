class DistanceData:

    def __init__(self, names, result):
        if not isinstance(names, (list, tuple)):
            raise TypeError("names must be a list or tuple")
        self.names = list(names)
        self._name_to_index = {name: i for i, name in enumerate(self.names)}
        n = len(self.names)
        # Initialize matrix
        self._matrix = [[0.0 if i == j else float(
            'inf') for j in range(n)] for i in range(n)]
        if result is None:
            return
        # Helper to resolve index from name or index

        def idx(x):
            if isinstance(x, int):
                if 0 <= x < n:
                    return x
                raise IndexError("index out of range")
            try:
                return self._name_to_index[x]
            except KeyError as e:
                raise KeyError(f"unknown name: {x}") from e
        # Load from 2D sequence
        if isinstance(result, (list, tuple)):
            if len(result) != n:
                raise ValueError("result size does not match names length")
            for i, row in enumerate(result):
                if not isinstance(row, (list, tuple)) or len(row) != n:
                    raise ValueError(
                        "result must be a square 2D sequence matching names length")
                for j, v in enumerate(row):
                    self._matrix[i][j] = float(v)
            return
        # Load from dict-of-dicts
        if isinstance(result, dict):
            # dict with tuple keys or nested dicts
            tuple_keyed = any(isinstance(k, tuple) and len(k)
                              == 2 for k in result.keys())
            if tuple_keyed:
                for (a, b), v in result.items():
                    i, j = idx(a), idx(b)
                    self._matrix[i][j] = float(v)
            else:
                for a, inner in result.items():
                    ia = idx(a)
                    if not isinstance(inner, dict):
                        raise ValueError(
                            "dict values must be dicts when not using tuple keys")
                    for b, v in inner.items():
                        ib = idx(b)
                        self._matrix[ia][ib] = float(v)
            return
        raise TypeError("Unsupported result type")

    @property
    def distance(self):
        def _d(a, b):
            i = self.index(a) if not isinstance(a, int) else a
            j = self.index(b) if not isinstance(b, int) else b
            if not (0 <= i < len(self.names) and 0 <= j < len(self.names)):
                raise IndexError("index out of range")
            return self._matrix[i][j]
        return _d

    def index(self, name):
        if isinstance(name, int):
            if 0 <= name < len(self.names):
                return name
            raise IndexError("index out of range")
        try:
            return self._name_to_index[name]
        except KeyError as e:
            raise KeyError(f"unknown name: {name}") from e

    def point(self, name):
        i = self.index(name)
        return list(self._matrix[i])
