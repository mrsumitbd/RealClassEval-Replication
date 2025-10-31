
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
        '''
        Sort reads that hit multiple HMMs to the databases to which they had
        the highest bit score. Return a dictionary containing HMMs as keys, and
        number of hits as the values.
        This function is set up so that the read names could easily be returned
        instead of numbers, for future development of GraftM
        Parameters
        ----------
        results_list: list
            Iterable if SequenceSearchResult objects. e.g.
                [SequenceSearchResult_1, SequenceSearchResult_2, ...]
        base_list: list
            Iterable of the basenames for each sequence file provided to graftM
            e.g.
                [sample_1, sample_2, ...]
        Returns
        -------
        dictionary:
            Contains samples as entries. The value for each sample is another
            dictionary with HMM as the key, and number of hits as values:
                {"sample_1":{HMM_1: 12
                             HMM_2: 35
                             HMM_3: 1258
                             ...}
                 ...
                }
        '''
        # Each SequenceSearchResult is assumed to have a .sample_name attribute (matching base_list)
        # and a .hits attribute, which is a list of dicts with keys: 'read_id', 'hmm', 'bit_score'
        # If not, adapt as needed.

        # For each sample, for each read, keep only the hit with the highest bit score
        sample_hmm_counts = {}
        for result, sample in zip(results_list, base_list):
            # result.hits: list of dicts with 'read_id', 'hmm', 'bit_score'
            # Group by read_id, keep only the hit with highest bit_score
            read_best_hit = {}
            for hit in getattr(result, 'hits', []):
                read_id = hit['read_id']
                hmm = hit['hmm']
                bit_score = hit['bit_score']
                if read_id not in read_best_hit or bit_score > read_best_hit[read_id][1]:
                    read_best_hit[read_id] = (hmm, bit_score)
            # Count number of reads assigned to each HMM
            hmm_counts = {}
            for hmm, _ in read_best_hit.values():
                hmm_counts[hmm] = hmm_counts.get(hmm, 0) + 1
            sample_hmm_counts[sample] = hmm_counts
        return sample_hmm_counts

    def _write_results(self, db_count, output_path):
        # db_count: dict as returned by _interpret_hits
        # output_path: str
        # Write table with header: #ID <sample1> <sample2> ...
        # Rows: HMM1 <count1> <count2> ...
        import csv

        # Collect all HMMs
        all_hmms = set()
        for sample_counts in db_count.values():
            all_hmms.update(sample_counts.keys())
        all_hmms = sorted(all_hmms)

        samples = list(db_count.keys())

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(['#ID'] + samples)
            for hmm in all_hmms:
                row = [hmm]
                for sample in samples:
                    count = db_count[sample].get(hmm, 0)
                    row.append(str(count))
                writer.writerow(row)

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
