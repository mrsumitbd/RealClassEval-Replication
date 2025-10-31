
class SearchTableWriter:

    def _interpret_hits(self, results_list, base_list):

        hits_dict = {}
        for result in results_list:
            if result['query'] in hits_dict:
                hits_dict[result['query']].append(result['target'])
            else:
                hits_dict[result['query']] = [result['target']]
        return hits_dict

    def _write_results(self, db_count, output_path):

        with open(output_path, 'w') as f:
            for query, targets in db_count.items():
                f.write(f"{query}\t{','.join(targets)}\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):

        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
