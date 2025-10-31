
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
        # Helper to extract sample name from a result
        def _get_sample(result):
            # Prefer explicit attribute
            for attr in ('sample', 'basename', 'file', 'filename'):
                if hasattr(result, attr):
                    val = getattr(result, attr)
                    if isinstance(val, str):
                        # If it's a path, strip extension
                        if os.path.sep in val or '.' in val:
                            return os.path.splitext(os.path.basename(val))[0]
                        return val
            # Fallback: try to infer from base_list order
            # This is a best‑effort approach; if not found, return None
            return None

        # Helper to extract HMM id
        def _get_hmm(result):
            for attr in ('query', 'hmm', 'hmm_id'):
                if hasattr(result, attr):
                    return getattr(result, attr)
            return None

        # Helper to extract read id
        def _get_read(result):
            for attr in ('subject', 'read_id', 'read'):
                if hasattr(result, attr):
                    return getattr(result, attr)
            return None

        # Helper to extract bit score
        def _get_score(result):
            for attr in ('bit_score', 'score', 'bits'):
                if hasattr(result, attr):
                    try:
                        return float(getattr(result, attr))
                    except Exception:
                        pass
            return 0.0

        # Map (sample, read) -> (hmm, score)
        best_hits = {}
        for res in results_list:
            sample = _get_sample(res)
            if sample is None:
                # Try to match by file basename
                if hasattr(res, 'file'):
                    sample = os.path.splitext(os.path.basename(res.file))[0]
                else:
                    continue  # cannot determine sample
            read_id = _get_read(res)
            if read_id is None:
                continue
            hmm = _get_hmm(res)
            if hmm is None:
                continue
            score = _get_score(res)
            key = (sample, read_id)
            if key not in best_hits or score > best_hits[key][1]:
                best_hits[key] = (hmm, score)

        # Count hits per sample per HMM
        db_count = defaultdict(lambda: defaultdict(int))
        for (sample, _), (hmm, _) in best_hits.items():
            db_count[sample][hmm] += 1

        # Convert defaultdicts to normal dicts
        return {s: dict(hmms) for s, hmms in db_count.items()}

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
        # Ensure directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        samples = sorted(db_count.keys())
        # Gather all HMMs
        all_hmms = set()
        for hmms in db_count.values():
            all_hmms.update(hmms.keys())
        all_hmms = sorted(all_hmms)

        with open(output_path, 'w', encoding='utf-8') as fh:
            # Header
            header = ['#ID'] + samples
            fh.write('\t'.join(header) + '\n')
            # Rows
            for hmm in all_hmms:
                row = [hmm]
                for sample in samples:
                    row.append(str(db_count[sample].get(hmm, 0)))
                fh.write('\t'.join(row) + '\n')

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
