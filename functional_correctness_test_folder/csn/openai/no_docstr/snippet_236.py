
import csv
import os
from collections import defaultdict


class SearchTableWriter:
    """
    Utility class to build an OTU table from search results.
    """

    def _interpret_hits(self, results_list, base_list):
        """
        Convert a list of search results into a nested dictionary mapping
        base IDs to search IDs and their corresponding scores.

        Parameters
        ----------
        results_list : list
            Each element is expected to be a mapping with at least the keys
            'search_id' and 'hits'.  The 'hits' value should be an iterable
            of mappings containing 'base_id' and 'score'.
        base_list : list
            List of all base IDs that should appear as rows in the table.

        Returns
        -------
        dict
            A dictionary where keys are base IDs and values are dictionaries
            mapping search IDs to scores.  Missing scores are omitted.
        """
        # Ensure base_list is a set for quick membership checks
        base_set = set(base_list)

        # Nested dict: base_id -> {search_id: score}
        table = defaultdict(dict)

        for result in results_list:
            search_id = result.get("search_id")
            if search_id is None:
                continue
            hits = result.get("hits", [])
            for hit in hits:
                base_id = hit.get("base_id")
                if base_id is None or base_id not in base_set:
                    continue
                score = hit.get("score", 0)
                table[base_id][search_id] = score

        # Ensure all base IDs are present in the table
        for base_id in base_set:
            table.setdefault(base_id, {})

        return dict(table)

    def _write_results(self, db_count, output_path):
        """
        Write the OTU table to a CSV file.

        Parameters
        ----------
        db_count : int
            Number of base entries (used only for validation).
        output_path : str
            Path to the output CSV file.
        """
        # The actual data to write is stored in self._table and self._search_ids
        if not hasattr(self, "_table") or not hasattr(self, "_search_ids"):
            raise RuntimeError(
                "No table data available. Call build_search_otu_table first.")

        # Validate db_count matches number of base rows
        if db_count != len(self._table):
            raise ValueError(
                f"db_count ({db_count}) does not match number of base rows ({len(self._table)}).")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            header = ["BaseID"] + self._search_ids
            writer.writerow(header)

            for base_id in sorted(self._table):
                row = [base_id]
                scores = self._table[base_id]
                for search_id in self._search_ids:
                    row.append(scores.get(search_id, 0))
                writer.writerow(row)

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        """
        Build an OTU table from search results and write it to a CSV file.

        Parameters
        ----------
        search_results_list : list
            List of search result mappings.
        base_list : list
            List of base IDs.
        output_path : str
            Path to the output CSV file.

        Returns
        -------
        None
        """
        # Interpret hits into a nested dictionary
        self._table = self._interpret_hits(search_results_list, base_list)

        # Determine the set of search IDs from the results
        search_ids = set()
        for result in search_results_list:
            search_id = result.get("search_id")
            if search_id is not None:
                search_ids.add(search_id)
        self._search_ids = sorted(search_ids)

        # Write the table to CSV
        self._write_results(len(base_list), output_path)
