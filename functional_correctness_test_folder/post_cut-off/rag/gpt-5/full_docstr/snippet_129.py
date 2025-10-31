import threading


class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self._lock = threading.RLock()
        self._partial = {}   # key -> {'arrival': int, 'seg': dict}
        self._completed = {}  # key -> {'arrival': int, 'seg': dict}
        self._arrival_counter = 0

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        p_list = self._normalize_segments(partial_segments)
        c_list = self._normalize_segments(completed_segments)

        with self._lock:
            # First handle completed segments to supersede partials
            for seg in c_list:
                seg = self._coerce_segment(seg)
                key = self._key_for(seg)
                if key in self._completed:
                    # Update existing completed while preserving arrival
                    arrival = self._completed[key]['arrival']
                elif key in self._partial:
                    # Move from partial -> completed while preserving arrival
                    arrival = self._partial[key]['arrival']
                else:
                    arrival = self._next_arrival()

                final_seg = self._mark_final(seg, True)
                self._completed[key] = {'arrival': arrival, 'seg': final_seg}
                if key in self._partial:
                    del self._partial[key]

            # Then handle partial segments (skip ones already finalized)
            for seg in p_list:
                seg = self._coerce_segment(seg)
                key = self._key_for(seg)
                if key in self._completed:
                    continue  # already finalized
                if key in self._partial:
                    arrival = self._partial[key]['arrival']
                else:
                    arrival = self._next_arrival()

                partial_seg = self._mark_final(seg, False)
                self._partial[key] = {'arrival': arrival, 'seg': partial_seg}

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        with self._lock:
            items = []

            # Collect completed
            for key, meta in self._completed.items():
                seg = meta['seg']
                arrival = meta['arrival']
                order_hint = self._order_hint(seg)
                items.append(
                    (self._sort_tuple(order_hint, arrival, True), seg))

            # Collect partial
            for key, meta in self._partial.items():
                seg = meta['seg']
                arrival = meta['arrival']
                order_hint = self._order_hint(seg)
                items.append(
                    (self._sort_tuple(order_hint, arrival, False), seg))

            items.sort(key=lambda x: x[0])
            return [dict(seg) for _, seg in items]

    # Internal helpers

    def _normalize_segments(self, segments):
        if segments is None:
            return []
        if isinstance(segments, dict):
            return [segments]
        try:
            # Treat strings specially to avoid iterating characters
            if isinstance(segments, str):
                return [segments]
            iter(segments)
            return list(segments)
        except TypeError:
            return [segments]

    def _coerce_segment(self, seg):
        if isinstance(seg, dict):
            return dict(seg)
        return {'text': '' if seg is None else str(seg)}

    def _next_arrival(self):
        val = self._arrival_counter
        self._arrival_counter += 1
        return val

    def _mark_final(self, seg, is_final):
        d = dict(seg)
        d['is_final'] = bool(is_final)
        return d

    def _key_for(self, seg):
        # Prefer explicit stable identifiers
        for k in ('id', 'segment_id', 'uuid', 'uid'):
            if k in seg and seg[k] is not None:
                return ('id', seg[k])

        for k in ('index', 'segment_index', 'position', 'seq', 'sequence'):
            if k in seg and seg[k] is not None:
                return ('idx', seg[k])

        # Time-based fallback
        start = seg.get('start_time', seg.get('start'))
        end = seg.get('end_time', seg.get('end'))
        if start is not None or end is not None:
            return ('time', (start, end))

        # Text-based fallback (may be unstable, but better than nothing)
        text = seg.get('text')
        if text:
            return ('text', text)

        # Last resort: unique arrival-based key (ensures storage, not matching)
        # We don't consume a new arrival here; _next_arrival() is called by caller.
        return ('auto', id(seg))

    def _to_float(self, v):
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return None

    def _order_hint(self, seg):
        # Prefer explicit indices
        for k in ('index', 'segment_index', 'position', 'seq', 'sequence'):
            num = self._to_float(seg.get(k))
            if num is not None:
                return ('idx', num)

        # Then start time
        for k in ('start_time', 'start'):
            num = self._to_float(seg.get(k))
            if num is not None:
                return ('time', num)

        return None

    def _sort_tuple(self, order_hint, arrival, is_final):
        # Primary: whether we have an explicit order hint
        has_hint = 0 if order_hint is not None else 1

        # Secondary: hint type priority, then value
        hint_type_rank = 1
        hint_value = 0.0
        if order_hint is not None:
            kind, val = order_hint
            hint_type_rank = 0 if kind == 'idx' else 1  # idx preferred over time
            hint_value = float(val) if isinstance(val, (int, float)) else 0.0

        # Tertiary: arrival order
        # Quaternary: finality (final first for same order)
        return (has_hint, hint_type_rank, hint_value, arrival, 0 if is_final else 1)
