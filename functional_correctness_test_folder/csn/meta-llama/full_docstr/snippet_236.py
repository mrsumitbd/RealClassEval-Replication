
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
        db_count = {base: {} for base in base_list}
        for i, result in enumerate(results_list):
            base = base_list[i]
            for read_id, hits in result.hits.items():
                if hits:
                    best_hit = max(hits, key=lambda x: x.bit_score)
                    db_count[base][best_hit.target_name] = db_count[base].get(
                        best_hit.target_name, 0) + 1
        return db_count

    def _write_results(self, db_count, output_path):
        '''Write the table to the output_path directory
        db_count: dict
            Contains samples as entries. The value for each sample is another
            dictionary with HMM as the key, and number of hits as values:
                {"sample_1":{HMM_1: 12
                             HMM_2: 35
                             HMM_3: 1258
                             ...}
                 ...
                }
        output_path: str
            Path to output file to which the resultant output file will be
            written to.
        '''
        hmm_names = set()
        for base in db_count:
            hmm_names.update(db_count[base].keys())
        hmm_names = sorted(list(hmm_names))

        with open(output_path, 'w') as f:
            f.write('#ID\t' + '\t'.join(db_count.keys()) + '\n')
            for hmm in hmm_names:
                counts = [str(db_count[base].get(hmm, 0)) for base in db_count]
                f.write(hmm + '\t' + '\t'.join(counts) + '\n')

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        '''
        Build an OTU from SequenceSearchResult objects
        Parameters
        ----------
        search_results_list: list
            Iterable if SequenceSearchResult objects. e.g.
                [SequenceSearchResult_1, SequenceSearchResult_2, ...]
        base_list: list
            Iterable of the basenames for each sequence file provided to graftM
            e.g.
                [sample_1, sample_2, ...]
        output_path: str
            Path to output file to which the resultant output file will be
            written to.
        '''
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
