class TranscriptionBuffer:
    def __init__(self, client_uid):
        from collections import OrderedDict
        import threading

        self.client_uid = client_uid
        self._completed = OrderedDict()
        self._partial = {}
        self._lock = threading.RLock()
        self._seq = 0  # fallback order counter

    def _is_number(self, v):
        return isinstance(v, (int, float))

    def _normalize_key(self, v):
        if self._is_number(v):
            return (0, float(v))
        try:
            return (1, str(v))
        except Exception:
            return (2, 0)

    def _segment_key(self, seg, fallback):
        for k in ("start", "begin", "start_time", "ts", "offset", "index", "id"):
            if isinstance(seg, dict) and k in seg:
                return self._normalize_key(seg[k])
            if hasattr(seg, k):
                return self._normalize_key(getattr(seg, k))
        return (3, fallback)

    def _coerce_iterable(self, maybe_iter):
        if maybe_iter is None:
            return []
        if isinstance(maybe_iter, dict):
            # Single segment dict accidentally passed
            return [maybe_iter]
        try:
            return list(maybe_iter)
        except TypeError:
            return [maybe_iter]

    def _get_id(self, seg):
        if isinstance(seg, dict):
            return seg.get("id")
        return getattr(seg, "id", None)

    def add_segments(self, partial_segments, completed_segments):
        partial_segments = self._coerce_iterable(partial_segments)
        completed_segments = self._coerce_iterable(completed_segments)

        with self._lock:
            # Incorporate completed segments
            for seg in completed_segments:
                seg_id = self._get_id(seg)
                if seg_id is None:
                    seg_id = f"__auto__{self._seq}"
                    self._seq += 1
                    if isinstance(seg, dict):
                        seg = {**seg, "id": seg_id}
                    else:
                        # Fallback: wrap as dict
                        seg = {"id": seg_id, "segment": seg}
                # Remove from partial if exists
                self._partial.pop(seg_id, None)
                # Insert/update into completed, preserving existing order if present
                self._completed[seg_id] = seg

            # Refresh snapshot of partial segments (exclude those already completed)
            new_partial = {}
            for seg in partial_segments:
                seg_id = self._get_id(seg)
                if seg_id is None:
                    seg_id = f"__auto__p__{self._seq}"
                    self._seq += 1
                    if isinstance(seg, dict):
                        seg = {**seg, "id": seg_id}
                    else:
                        seg = {"id": seg_id, "segment": seg}
                if seg_id in self._completed:
                    continue
                new_partial[seg_id] = seg
            self._partial = new_partial

    def get_segments_for_response(self):
        with self._lock:
            # Combine completed and current partial snapshot
            combined = list(self._completed.values()) + \
                list(self._partial.values())

            # Stable sort using computed keys; fallback uses enumeration index
            def sort_key(item_enumerated):
                idx, seg = item_enumerated
                return self._segment_key(seg, idx)

            return [seg for _, seg in sorted(enumerate(combined), key=sort_key)]
