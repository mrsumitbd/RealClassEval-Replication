
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
        sample_hits = {sample: {} for sample in base_list}
        for result in results_list:
            sample_index = result.sample_index
            sample_name = base_list[sample_index]
            hmm_name = result.hmm_name
            bit_score = result.bit_score
            if hmm_name not in sample_hits[sample_name]:
                sample_hits[sample_name][hmm_name] = (
                    result.read_name, bit_score)
            else:
                current_read, current_score = sample_hits[sample_name][hmm_name]
                if bit_score > current_score:
                    sample_hits[sample_name][hmm_name] = (
                        result.read_name, bit_score)

        # Convert read names and scores to just counts
        for sample in sample_hits:
            sample_hits[sample] = {hmm: 1 for hmm,
                                   _ in sample_hits[sample].items()}

        return sample_hits

    def _write_results(self, db_count, output_path):
        with open(output_path, 'w') as f:
            header = ['#ID'] + list(db_count.keys())
            f.write('\t'.join(header) + '\n')
            hmm_names = set()
            for sample in db_count.values():
                hmm_names.update(sample.keys())
            for hmm in sorted(hmm_names):
                row = [hmm]
                for sample in header[1:]:
                    row.append(str(db_count[sample].get(hmm, 0)))
                f.write('\t'.join(row) + '\n')

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
