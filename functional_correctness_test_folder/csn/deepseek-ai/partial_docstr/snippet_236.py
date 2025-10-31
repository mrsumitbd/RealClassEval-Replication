
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
            sample = result.sample_name
            hits = result.hits

            best_hits = {}
            for hit in hits:
                read_name = hit.read_name
                hmm = hit.hmm_name
                bit_score = hit.bit_score

                if read_name not in best_hits or bit_score > best_hits[read_name][1]:
                    best_hits[read_name] = (hmm, bit_score)

            for hmm, _ in best_hits.values():
                if hmm in sample_hits[sample]:
                    sample_hits[sample][hmm] += 1
                else:
                    sample_hits[sample][hmm] = 1

        return sample_hits

    def _write_results(self, db_count, output_path):
        samples = sorted(db_count.keys())
        hmms = set()
        for sample in samples:
            hmms.update(db_count[sample].keys())
        hmms = sorted(hmms)

        with open(output_path, 'w') as f:
            header = "#ID\t" + "\t".join(samples) + "\n"
            f.write(header)

            for hmm in hmms:
                line = [hmm]
                for sample in samples:
                    count = db_count[sample].get(hmm, 0)
                    line.append(str(count))
                f.write("\t".join(line) + "\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
