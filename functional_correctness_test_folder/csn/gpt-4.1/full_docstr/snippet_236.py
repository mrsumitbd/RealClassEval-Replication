
class SearchTableWriter:
    '''
    Class for writing the search output OTU table. Basically a summary
    of hits to the HMM/Diamond searched in the following format:
             #ID    Metagenome_1    Metagenome_2    ...
            HMM1    50              6
            HMM2    195             41
            HMM3    2               20120
            ...
    You just need to specify a series of SequenceSearchResult objects, and an
    output path.
    '''

    def _interpret_hits(self, results_list, base_list):
        '''Sort reads that hit multiple HMMs to the databases to which they had
        the highest bit score. Return a dictionary containing HMMs as keys, and
        number of hits as the values.
        '''
        # results_list: [SequenceSearchResult_1, SequenceSearchResult_2, ...]
        # base_list: [sample_1, sample_2, ...]
        # Each SequenceSearchResult must have .sample_name, .hits
        # .hits: dict mapping read_id -> list of (hmm, bitscore)
        # We'll build: {sample: {hmm: count, ...}, ...}
        db_count = {}
        for result, sample in zip(results_list, base_list):
            # result.hits: dict of read_id -> list of (hmm, bitscore)
            sample_counts = {}
            for read_id, hits in result.hits.items():
                # hits: list of (hmm, bitscore)
                if not hits:
                    continue
                # Find the hmm(s) with the highest bitscore
                max_score = max(h[1] for h in hits)
                best_hmms = [h[0] for h in hits if h[1] == max_score]
                # If multiple HMMs have the same max score, count all
                for hmm in best_hmms:
                    sample_counts[hmm] = sample_counts.get(hmm, 0) + 1
            db_count[sample] = sample_counts
        return db_count

    def _write_results(self, db_count, output_path):
        '''Write the table to the output_path directory'''
        # db_count: {sample: {hmm: count, ...}, ...}
        # Collect all HMMs
        all_hmms = set()
        for sample_counts in db_count.values():
            all_hmms.update(sample_counts.keys())
        all_hmms = sorted(all_hmms)
        samples = list(db_count.keys())
        with open(output_path, 'w') as f:
            # Write header
            f.write("#ID\t" + "\t".join(samples) + "\n")
            for hmm in all_hmms:
                row = [hmm]
                for sample in samples:
                    count = db_count[sample].get(hmm, 0)
                    row.append(str(count))
                f.write("\t".join(row) + "\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        '''
        Build an OTU from SequenceSearchResult objects
        '''
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
