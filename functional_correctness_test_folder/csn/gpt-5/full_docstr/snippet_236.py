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
        if results_list is None:
            results_list = []
        if base_list is None:
            base_list = []
        if len(results_list) != len(base_list):
            raise ValueError(
                "results_list and base_list must be the same length")

        def _get_attr_or_key(obj, names, default=None):
            for n in names:
                if hasattr(obj, n):
                    return getattr(obj, n)
                if isinstance(obj, dict) and n in obj:
                    return obj[n]
            return default

        def _iterate_hits_from_result(result):
            # Try to detect mapping of read -> hits
            if isinstance(result, dict):
                # assume keys are read ids and values are iterable of hit dicts/objects
                for read_id, hits in result.items():
                    if hits is None:
                        continue
                    for h in hits:
                        yield read_id, h
                return

            # named attribute with mapping
            mapping = _get_attr_or_key(
                result, ['per_read_hits', 'by_read', 'read_hits', 'mapping'], None)
            if isinstance(mapping, dict):
                for read_id, hits in mapping.items():
                    if hits is None:
                        continue
                    for h in hits:
                        yield read_id, h
                return

            # flat iterable of hits
            hits_iter = _get_attr_or_key(
                result, ['hits', 'results', 'records', 'alignments', 'matches'], None)
            if hits_iter is None and hasattr(result, '__iter__'):
                hits_iter = result

            if hits_iter is not None:
                for h in hits_iter:
                    read_id = _get_attr_or_key(
                        h, ['query', 'read', 'read_id', 'qseqid', 'query_id', 'name', 'qid'])
                    yield read_id, h
                return

            # nothing found
            return

        def _extract_hit_fields(hit):
            hmm = _get_attr_or_key(
                hit, ['hmm', 'target', 'db', 'subject', 'sseqid', 'target_id', 'hmm_id', 'reference', 'model'])
            score = _get_attr_or_key(
                hit, ['bit_score', 'bitscore', 'score', 'bitScore', 'bits', 'bitscore_raw'])
            # Try convert score
            try:
                score = float(score) if score is not None else None
            except Exception:
                score = None
            return hmm, score

        db_count = {}
        for sample_name, result in zip(base_list, results_list):
            sample_counts = {}
            # Group by read
            per_read_hits = {}
            for read_id, hit in _iterate_hits_from_result(result):
                if read_id is None:
                    # best effort: treat missing read id as unique per hit object
                    read_id = id(hit)
                hmm, score = _extract_hit_fields(hit)
                if hmm is None:
                    continue
                if score is None:
                    # If no score available, treat as 0 to allow deterministic tie-break
                    score = 0.0
                per_read_hits.setdefault(
                    read_id, {}).setdefault(hmm, -float('inf'))
                if score > per_read_hits[read_id][hmm]:
                    per_read_hits[read_id][hmm] = score

            # Decide best HMM per read
            for read_id, hmm_scores in per_read_hits.items():
                if not hmm_scores:
                    continue
                # pick hmm with max score; tie-breaker by lexicographic order of hmm id
                max_score = max(hmm_scores.values())
                best_hmms = [h for h, s in hmm_scores.items() if s ==
                             max_score]
                best_hmm = sorted(best_hmms)[0]
                sample_counts[best_hmm] = sample_counts.get(best_hmm, 0) + 1

            db_count[sample_name] = sample_counts

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
        if db_count is None:
            db_count = {}

        samples = list(db_count.keys())
        # Gather all HMMs present across samples
        all_hmms = set()
        for counts in db_count.values():
            all_hmms.update(counts.keys())
        sorted_hmms = sorted(all_hmms)

        with open(output_path, 'w', encoding='utf-8') as fh:
            # Header
            fh.write("#ID")
            if samples:
                fh.write("\t" + "\t".join(samples))
            fh.write("\n")

            # Rows
            for hmm in sorted_hmms:
                row = [hmm]
                for s in samples:
                    row.append(str(db_count.get(s, {}).get(hmm, 0)))
                fh.write("\t".join(row) + "\n")

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
