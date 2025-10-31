
import os
from collections import defaultdict


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
        # Map each query to its best hit (highest bit score)
        best_hits = {}
        for res in results_list:
            # Resolve attributes that may differ between implementations
            query = getattr(res, 'query_name', None) or getattr(
                res, 'query', None)
            if query is None:
                continue  # skip if no query name
            subject = getattr(res, 'subject_name', None) or getattr(
                res, 'subject', None)
            if subject is None:
                continue  # skip if no subject
            bit_score = getattr(res, 'bit_score', None) or getattr(
                res, 'score', None)
            if bit_score is None:
                continue  # skip if no score
            # Determine sample name
            sample_name = None
            if hasattr(res, 'sample_name'):
                sample_name = res.sample_name
            elif hasattr(res, 'sample_index'):
                idx = res.sample_index
                if isinstance(idx, int) and 0 <= idx < len(base_list):
                    sample_name = base_list[idx]
            if sample_name is None:
                # If no sample info, skip
                continue

            # Keep only the best hit per query
            if query not in best_hits or bit_score > best_hits[query]['bit_score']:
                best_hits[query] = {
                    'subject': subject,
                    'bit_score': bit_score,
                    'sample': sample_name
                }

        # Count hits per sample per HMM
        db_count = defaultdict(lambda: defaultdict(int))
        for hit in best_hits.values():
            sample = hit['sample']
            subject = hit['subject']
            db_count[sample][subject] += 1

        return db_count

    def _write_results(self, db_count, output_path):
        '''
        Write the OTU table to the specified output path.
        Parameters
        ----------
        db_count: dict
            Output of _interpret_hits: {sample: {HMM: count}}
        output_path: str
            Path to write the table.
        '''
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        # Determine all samples and HMMs
        samples = sorted(db_count.keys())
        all_hmms = set()
        for sample_dict in db_count.values():
            all_hmms.update(sample_dict.keys())
        hmms = sorted(all_hmms)

        with open(output_path, 'w', encoding='utf-8') as fh:
            # Header
            header = ['#ID'] + samples
            fh.write('\t'.join(header) + '\n')
            # Rows
            for hmm in hmms:
                row = [hmm]
                for sample in samples:
                    row.append(str(db_count[sample].get(hmm, 0)))
                fh.write('\t'.join(row) + '\n')

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        '''
        Main entry point: interpret hits and write the OTU table.
        Parameters
        ----------
        search_results_list: list
            List of SequenceSearchResult objects.
        base_list: list
            List of sample base names.
        output_path: str
            Path to write the OTU table.
        '''
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
