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
        if results_list is None or base_list is None:
            raise ValueError("results_list and base_list must not be None")
        if len(results_list) != len(base_list):
            raise ValueError(
                "results_list and base_list must be the same length")

        def _yield_hits_from_result(result):
            # Try several common layouts to extract (read_id, hmm_id, bitscore)
            # 1) Method iterate_hits()
            if hasattr(result, "iterate_hits") and callable(getattr(result, "iterate_hits")):
                for h in result.iterate_hits():
                    # Accept tuple or dict
                    if isinstance(h, dict):
                        q = h.get("query") or h.get("read") or h.get(
                            "read_id") or h.get("qseqid")
                        t = h.get("target") or h.get("hmm") or h.get(
                            "subject") or h.get("sseqid")
                        b = h.get("bitscore") or h.get(
                            "bit_score") or h.get("score")
                    else:
                        # Try tuple ordering: (query, target, bitscore, ...)
                        q = h[0] if len(h) > 0 else None
                        t = h[1] if len(h) > 1 else None
                        b = h[2] if len(h) > 2 else None
                    if q is not None and t is not None and b is not None:
                        yield (q, str(t), float(b))
                return

            # 2) hits_by_read-like mapping
            for attr in ("hits_by_read", "by_read", "read_hits"):
                if hasattr(result, attr):
                    mapping = getattr(result, attr)
                    if isinstance(mapping, dict):
                        for q, hit_list in mapping.items():
                            if hit_list is None:
                                continue
                            for h in hit_list:
                                if isinstance(h, dict):
                                    t = h.get("target") or h.get("hmm") or h.get(
                                        "subject") or h.get("sseqid")
                                    b = h.get("bitscore") or h.get(
                                        "bit_score") or h.get("score")
                                else:
                                    # Try tuple or list: (target, bitscore) or (target, bitscore, ...)
                                    t = h[0] if len(h) > 0 else None
                                    b = h[1] if len(h) > 1 else None
                                if t is not None and b is not None:
                                    yield (q, str(t), float(b))
                        return

            # 3) Flat hits list
            for attr in ("hits", "records", "results"):
                if hasattr(result, attr):
                    hits = getattr(result, attr)
                    if hits is None:
                        continue
                    for h in hits:
                        if isinstance(h, dict):
                            q = h.get("query") or h.get("read") or h.get(
                                "read_id") or h.get("qseqid")
                            t = h.get("target") or h.get("hmm") or h.get(
                                "subject") or h.get("sseqid")
                            b = h.get("bitscore") or h.get(
                                "bit_score") or h.get("score")
                        else:
                            q = h[0] if len(h) > 0 else None
                            t = h[1] if len(h) > 1 else None
                            b = h[2] if len(h) > 2 else None
                        if q is not None and t is not None and b is not None:
                            yield (q, str(t), float(b))
                    return

            # 4) Nothing recognized; yield nothing
            return

        sample_to_counts = {}

        for sample_name, result in zip(base_list, results_list):
            # Aggregate best target per read by highest bitscore
            best_per_read = {}
            for read_id, hmm_id, bitscore in _yield_hits_from_result(result):
                prev = best_per_read.get(read_id)
                if prev is None:
                    best_per_read[read_id] = (hmm_id, bitscore)
                else:
                    prev_hmm, prev_score = prev
                    if (bitscore > prev_score) or (bitscore == prev_score and hmm_id < prev_hmm):
                        best_per_read[read_id] = (hmm_id, bitscore)

            counts = {}
            for hmm_id, _score in (best_per_read.values()):
                counts[hmm_id] = counts.get(hmm_id, 0) + 1

            sample_to_counts[sample_name] = counts

        return sample_to_counts

    def _write_results(self, db_count, output_path):
        # Determine all HMM ids across samples
        all_hmms = set()
        for counts in db_count.values():
            all_hmms.update(counts.keys())
        ordered_hmms = sorted(all_hmms)

        # Determine sample order from self._base_list if available, else dict order
        if hasattr(self, "_base_list") and isinstance(self._base_list, (list, tuple)):
            samples = list(self._base_list)
        else:
            samples = list(db_count.keys())

        # Write TSV
        with open(output_path, "w", newline="") as fh:
            fh.write("#ID")
            for s in samples:
                fh.write("\t")
                fh.write(str(s))
            fh.write("\n")

            for hmm in ordered_hmms:
                fh.write(str(hmm))
                for s in samples:
                    val = db_count.get(s, {}).get(hmm, 0)
                    fh.write("\t")
                    fh.write(str(int(val)))
                fh.write("\n")

    def build_search_otu_table(self, search_results_list, base_list, output_path):
        if not isinstance(search_results_list, (list, tuple)):
            raise ValueError("search_results_list must be a list or tuple")
        if not isinstance(base_list, (list, tuple)):
            raise ValueError("base_list must be a list or tuple")
        if len(search_results_list) != len(base_list):
            raise ValueError(
                "search_results_list and base_list must be the same length")
        self._base_list = list(base_list)
        db_count = self._interpret_hits(search_results_list, base_list)
        self._write_results(db_count, output_path)
        return output_path
