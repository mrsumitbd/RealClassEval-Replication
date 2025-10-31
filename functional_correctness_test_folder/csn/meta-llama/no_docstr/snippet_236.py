
import pandas as pd


class SearchTableWriter:

    def _interpret_hits(self, results_list, base_list):
        """Interpret search results and create a dictionary with the results."""
        results_dict = {}
        for i, result in enumerate(results_list):
            base_name = base_list[i]
            results_dict[base_name] = {}
            for hit in result:
                results_dict[base_name][hit['id']] = hit['count']
        return results_dict

    def _write_results(self, db_count, output_path):
        """Write the search results to a tab-delimited file."""
        db_count.to_csv(output_path, sep='\t', index=True)

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        """Build a search OTU table from search results."""
        results_dict = self._interpret_hits(search_results_list, base_list)
        db_count = pd.DataFrame(results_dict).fillna(0).astype(int)
        self._write_results(db_count, output_path)
