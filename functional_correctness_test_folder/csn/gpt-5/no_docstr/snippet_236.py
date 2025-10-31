class SearchTableWriter:
    def __init__(self):
        self._counts_per_base = None
        self._base_list = None

    def _extract_id(self, item):
        if item is None:
            return None
        # Direct types
        if isinstance(item, (str, int)):
            return str(item)
        # Dict-like
        if isinstance(item, dict):
            for key in ("id", "otu", "name", "identifier", "taxon", "tax_id", "taxid"):
                if key in item and item[key] is not None:
                    return str(item[key])
            # Fallback: first non-null value
            for v in item.values():
                if v is not None:
                    return str(v)
            return None
        # Tuple/list-like
        if isinstance(item, (list, tuple)):
            for v in item:
                if v is not None:
                    return str(v)
            return None
        # Fallback to string repr
        try:
            return str(item)
        except Exception:
            return None

    def _interpret_hits(self, results_list, base_list):
        if base_list is None:
            raise ValueError("base_list is required")
        if results_list is None:
            raise ValueError("results_list is required")
        base_str_list = [str(b) for b in base_list]
        base_set = set(base_str_list)
        num_dbs = len(results_list)
        counts_per_base = {b: [0] * num_dbs for b in base_str_list}

        for col_idx, db_results in enumerate(results_list):
            if db_results is None:
                continue
            # Normalize to iterable
            try:
                iterator = iter(db_results)
            except TypeError:
                iterator = iter([db_results])

            local_counts = {}
            for item in iterator:
                hit_id = self._extract_id(item)
                if hit_id is None:
                    continue
                if hit_id in base_set:
                    local_counts[hit_id] = local_counts.get(hit_id, 0) + 1

            for b in base_str_list:
                if b in local_counts:
                    counts_per_base[b][col_idx] = local_counts[b]

        self._counts_per_base = counts_per_base
        self._base_list = base_str_list
        return counts_per_base

    def _write_results(self, db_count, output_path):
        if self._counts_per_base is None or self._base_list is None:
            raise RuntimeError(
                "No interpreted results to write. Call _interpret_hits first.")
        if not output_path:
            raise ValueError("output_path is required")

        # Support gzip transparently
        opener = None
        if str(output_path).endswith(".gz"):
            import gzip
            def opener(p, m): return gzip.open(p, m, compresslevel=5)
        else:
            opener = open

        header = ["ID"] + [f"DB_{i+1}" for i in range(db_count)]
        newline = "\n"

        with opener(output_path, "wt") as fh:
            fh.write("\t".join(header) + newline)
            for base_id in self._base_list:
                counts = self._counts_per_base.get(base_id, [0] * db_count)
                row = [base_id] + [str(c) for c in counts]
                fh.write("\t".join(row) + newline)

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        counts = self._interpret_hits(search_results_list, base_list)
        self._write_results(len(search_results_list), output_path)
        return counts
