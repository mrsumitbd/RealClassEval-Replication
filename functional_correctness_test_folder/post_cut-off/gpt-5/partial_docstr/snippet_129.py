class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        self.client_uid = client_uid
        self._completed_by_key = {}
        self._completed_order = []
        self._partial_by_key = {}

    def _normalize_segments(self, segs):
        if not segs:
            return []
        if isinstance(segs, dict):
            return [segs]
        return list(segs)

    def _key_for(self, seg):
        seg_id = seg.get('id')
        if seg_id is not None:
            return ('id', seg_id)
        # Fallback stable key from content
        text = seg.get('text', '')
        start = seg.get('start')
        end = seg.get('end')
        return ('content', text, start, end)

    def _sort_key(self, seg):
        start = seg.get('start')
        if start is None:
            return (1, 0)
        try:
            return (0, float(start))
        except (TypeError, ValueError):
            return (0, 0)

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        partial_segments = self._normalize_segments(partial_segments)
        completed_segments = self._normalize_segments(completed_segments)

        # First, add completed segments and remove them from partials if present
        for seg in completed_segments:
            key = self._key_for(seg)
            if key not in self._completed_by_key:
                self._completed_order.append(key)
            self._completed_by_key[key] = dict(seg)
            if key in self._partial_by_key:
                self._partial_by_key.pop(key, None)

        # Rebuild partial state from provided partials (latest snapshot)
        new_partial = {}
        for seg in partial_segments:
            key = self._key_for(seg)
            if key in self._completed_by_key:
                continue
            new_partial[key] = dict(seg)
        self._partial_by_key = new_partial

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        # Completed segments in insertion order, then by start
        completed_list = [self._completed_by_key[k]
                          for k in self._completed_order if k in self._completed_by_key]
        completed_list.sort(key=self._sort_key)

        # Partial segments sorted by start
        partial_list = list(self._partial_by_key.values())
        partial_list.sort(key=self._sort_key)

        def format_seg(seg, is_final):
            return {
                'id': seg.get('id'),
                'text': seg.get('text', ''),
                'start': seg.get('start'),
                'end': seg.get('end'),
                'final': is_final,
            }

        formatted = [format_seg(s, True) for s in completed_list] + \
            [format_seg(s, False) for s in partial_list]
        return {
            'client_uid': self.client_uid,
            'segments': formatted,
        }
