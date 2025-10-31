
class SearchTableWriter:

    def _interpret_hits(self, results_list, base_list):
        interpreted_hits = []
        for result in results_list:
            hit_dict = {}
            for hit in result:
                if hit in base_list:
                    hit_dict[hit] = hit_dict.get(hit, 0) + 1
            interpreted_hits.append(hit_dict)
        return interpreted_hits

    def _write_results(self, db_count, output_path):
        with open(output_path, 'w') as f:
            headers = sorted(db_count[0].keys())
            f.write("\t".join(["OTU"] + headers) + "\n")
            for i, otu_counts in enumerate(db_count):
                row = [f"OTU_{i+1}"]
                for header in headers:
                    row.append(str(otu_counts.get(header, 0)))
                f.write("\t".join(row) + "\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        interpreted_hits = self._interpret_hits(search_results_list, base_list)
        self._write_results(interpreted_hits, output_path)
