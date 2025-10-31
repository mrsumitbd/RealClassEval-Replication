
class SearchTableWriter:

    def _interpret_hits(self, results_list, base_list):
        interpreted_results = {}
        for result in results_list:
            for base in base_list:
                if base in result:
                    if base not in interpreted_results:
                        interpreted_results[base] = []
                    interpreted_results[base].append(result)
        return interpreted_results

    def _write_results(self, db_count, output_path):
        with open(output_path, 'w') as file:
            file.write(f"Database Count: {db_count}\n")
            for key, values in db_count.items():
                file.write(f"{key}: {', '.join(map(str, values))}\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        interpreted_results = self._interpret_hits(
            search_results_list, base_list)
        db_count = {key: len(values)
                    for key, values in interpreted_results.items()}
        self._write_results(db_count, output_path)
