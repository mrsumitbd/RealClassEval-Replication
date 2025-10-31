
import csv


class SearchTableWriter:

    def _interpret_hits(self, results_list, base_list):
        """
        Given a list of search results (list of sets or lists of hits per query)
        and a base_list (list of all possible OTUs), return a list of dicts
        mapping OTU to 1 (hit) or 0 (no hit) for each result in results_list.
        """
        interpreted = []
        for hits in results_list:
            # Convert hits to set for fast lookup
            hit_set = set(hits)
            row = {otu: (1 if otu in hit_set else 0) for otu in base_list}
            interpreted.append(row)
        return interpreted

    def _write_results(self, db_count, output_path):
        """
        Write the db_count (list of dicts) to a CSV file at output_path.
        The first row is the header (OTU names).
        Each subsequent row is a sample/query.
        """
        if not db_count:
            # Nothing to write
            return
        fieldnames = list(db_count[0].keys())
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in db_count:
                writer.writerow(row)

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        """
        Given search_results_list (list of lists/sets of hits per query),
        base_list (all possible OTUs), and output_path (CSV file),
        build and write the OTU table.
        """
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
