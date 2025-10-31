
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
            read_hits = {}
            for hit in result.hits:
                hmm = hit.hmm_name
                bit_score = hit.bit_score
                if hmm not in read_hits or bit_score > read_hits[hmm][1]:
                    read_hits[hmm] = (hit.sample_name, bit_score)

            for hmm, (sample_name, _) in read_hits.items():
                if sample_name in sample_hits:
                    if hmm in sample_hits[sample_name]:
                        sample_hits[sample_name][hmm] += 1
                    else:
                        sample_hits[sample_name][hmm] = 1

        return sample_hits

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
        all_hmms = set()
        for sample in db_count.values():
            all_hmms.update(sample.keys())
        sorted_hmms = sorted(all_hmms)

        samples = sorted(db_count.keys())

        with open(output_path, 'w') as f:
            header = ['#ID'] + samples
            f.write('\t'.join(header) + '\n')

            for hmm in sorted_hmms:
                row = [hmm]
                for sample in samples:
                    count = db_count[sample].get(hmm, 0)
                    row.append(str(count))
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
