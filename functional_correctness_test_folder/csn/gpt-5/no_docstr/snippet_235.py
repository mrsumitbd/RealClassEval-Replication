class Deduplicator:
    def _extract_sequence(self, obj):
        # Try to extract a sequence string from various possible object shapes
        if obj is None:
            return None

        # If the object itself is a string
        if isinstance(obj, str):
            return obj

        # If the object is a dict-like
        if isinstance(obj, dict):
            for k in ("sequence", "seq", "aligned_sequence", "aligned_seq", "dna", "rna"):
                if k in obj and isinstance(obj[k], str):
                    return obj[k]
            # Sometimes the first value might be the sequence if dict is ordered
            for v in obj.values():
                if isinstance(v, str):
                    return v
            return None

        # If the object is a tuple/list, try first string-like element
        if isinstance(obj, (list, tuple)):
            for v in obj:
                if isinstance(v, str):
                    return v
            return None

        # If the object has attributes that could contain sequence
        for attr in ("sequence", "seq", "aligned_sequence", "aligned_seq", "dna", "rna"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if isinstance(val, str):
                    return val

        # Fallback: string representation if it seems sequence-like
        s = str(obj)
        return s if isinstance(s, str) else None

    def _normalize_sequence(self, seq):
        if seq is None:
            return None
        # Remove common alignment gap chars and whitespace, upper-case for uniformity
        # Keep only IUPAC letters and '*' (stop) optionally, remove others
        s = ''.join(ch for ch in seq if ch not in {
                    '-', '.', ' ', '\t', '\n', '\r'})
        return s.upper()

    def _extract_identifier_candidates(self, obj, raw_seq=None, norm_seq=None):
        # Try to derive identifiers to look up taxonomy from taxonomy_hash
        candidates = []
        if norm_seq:
            candidates.append(norm_seq)
        if raw_seq:
            candidates.append(raw_seq)

        if obj is None:
            return candidates

        # From dict-like
        if isinstance(obj, dict):
            for k in ("id", "identifier", "name", "header", "accession", "taxon", "taxid"):
                v = obj.get(k)
                if isinstance(v, str) and v:
                    candidates.append(v)
            return candidates

        # From attributes
        for attr in ("id", "identifier", "name", "header", "accession", "taxon", "taxid"):
            if hasattr(obj, attr):
                v = getattr(obj, attr)
                if isinstance(v, str) and v:
                    candidates.append(v)

        return candidates

    def _split_lineage(self, lineage):
        if lineage is None:
            return []
        if not isinstance(lineage, str):
            lineage = str(lineage)
        # Try common separators
        for sep in (';', '|', '\t', ','):
            if sep in lineage:
                parts = [p.strip() for p in lineage.split(sep)]
                return [p for p in parts if p]
        return [lineage.strip()] if lineage.strip() else []

    def _join_lineage(self, parts):
        return '; '.join(parts)

    def _lca_of_lineages(self, lineages):
        if not lineages:
            return ""
        split = [self._split_lineage(l) for l in lineages if l is not None]
        if not split:
            return ""
        # Find common prefix across all lists
        min_len = min(len(s) for s in split)
        lca = []
        for i in range(min_len):
            token = split[0][i]
            if all(s[i] == token for s in split[1:]):
                lca.append(token)
            else:
                break
        return self._join_lineage(lca)

    def deduplicate(self, aligned_sequence_objects):
        groups = {}
        order = 0
        for obj in aligned_sequence_objects or []:
            raw_seq = self._extract_sequence(obj)
            norm = self._normalize_sequence(raw_seq)
            if not norm:
                continue
            if norm not in groups:
                groups[norm] = {
                    "sequence": norm,
                    "count": 0,
                    "members": [],
                    "_first_index": order,
                }
            groups[norm]["count"] += 1
            groups[norm]["members"].append(obj)
            order += 1
        # Return an ordered list by first occurrence for stability, plus mapping
        # But to keep it simple and broadly useful, return the dict
        # Users can sort by ['_first_index'] if needed
        # Strip helper keys for cleanliness
        for g in groups.values():
            g.pop("_first_index", None)
        return groups

    def lca_taxonomy(self, deduplicated_sequences, taxonomy_hash):
        if not isinstance(deduplicated_sequences, dict):
            # Try to coerce if a list of sequences was provided
            deduplicated_sequences = self.deduplicate(deduplicated_sequences)

        result = {}
        for norm_seq, info in deduplicated_sequences.items():
            members = info.get("members", [])
            lineages = []
            # Try per-member identifiers first
            for m in members:
                raw_seq = self._extract_sequence(m)
                candidates = self._extract_identifier_candidates(
                    m, raw_seq=raw_seq, norm_seq=norm_seq)
                found = None
                for key in candidates:
                    if key in taxonomy_hash:
                        found = taxonomy_hash[key]
                        break
                if found is not None:
                    lineages.append(found)
            # Fallback: sequence key itself
            if not lineages and norm_seq in taxonomy_hash:
                lineages.append(taxonomy_hash[norm_seq])

            lca = self._lca_of_lineages(lineages)
            result[norm_seq] = {
                "lca": lca,
                "count": info.get("count", 0),
                "members": members,
            }
        return result
