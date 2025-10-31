
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
        sample_hits = {base: {} for base in base_list}
        for i, result in enumerate(results_list):
            for read in result.read_hits:
                max_hit = max(read.hits, key=lambda x: x.bit_score)
                hmm_name = max_hit.hmm_name
                if hmm_name not in sample_hits[base_list[i]]:
                    sample_hits[base_list[i]][hmm_name] = 0
                sample_hits[base_list[i]][hmm_name] += 1
        return sample_hits

    def _write_results(self, db_count, output_path):
        with open(output_path, 'w') as f:
            # Write header
            f.write('#ID\t' + '\t'.join(db_count.keys()) + '\n')
            # Get all HMMs across all samples
            all_hmms = set()
            for sample in db_count.values():
                all_hmms.update(sample.keys())
            # Write counts for each HMM
            for hmm in sorted(all_hmms):
                row = [hmm]
                for sample in db_count.keys():
                    row.append(str(db_count[sample].get(hmm, 0)))
                f.write('\t'.join(row) + '\n')

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
