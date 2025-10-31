
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
        for result in results_list:
            sample_name = result.sample_name
            hmm_name = result.hmm_name
            bit_score = result.bit_score
            if sample_name not in db_count:
                db_count[sample_name] = {}
            if hmm_name not in db_count[sample_name] or bit_score > db_count[sample_name][hmm_name]:
                db_count[sample_name][hmm_name] = bit_score
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
        with open(output_path, 'w') as f:
            headers = ['#ID'] + list(db_count.keys())
            f.write('\t'.join(headers) + '\n')
            all_hmms = set()
            for sample in db_count.values():
                all_hmms.update(sample.keys())
            for hmm in sorted(all_hmms):
                row = [hmm]
                for sample in headers[1:]:
                    row.append(str(db_count[sample].get(hmm, 0)))
                f.write('\t'.join(row) + '\n')

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
