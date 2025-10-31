class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self._partial = []
        self._completed = []
        self._completed_index = {}  # id -> index in _completed

    def _as_list(self, segments):
        if segments is None:
            return []
        if isinstance(segments, (list, tuple)):
            return list(segments)
        return [segments]

    def _get_id(self, seg):
        if isinstance(seg, dict):
            if 'id' in seg:
                return seg['id']
            if 'segment_id' in seg:
                return seg['segment_id']
        return None

    def _extract_text(self, seg):
        if isinstance(seg, dict):
            for k in ('text', 'content', 'value'):
                if k in seg and isinstance(seg[k], str):
                    return seg[k]
            return str(seg)
        if isinstance(seg, str):
            return seg
        return str(seg)

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        new_partials = self._as_list(partial_segments)
        new_completed = self._as_list(completed_segments)

        # Process completed: add/update and remove from partials
        for seg in new_completed:
            sid = self._get_id(seg)
            if sid is not None:
                if sid in self._completed_index:
                    idx = self._completed_index[sid]
                    self._completed[idx] = seg
                else:
                    self._completed_index[sid] = len(self._completed)
                    self._completed.append(seg)
            else:
                # No id: avoid duplicate exact entries
                if seg not in self._completed:
                    self._completed.append(seg)

        # Overwrite partials with provided list, filtering out any that are now completed
        filtered_partials = []
        completed_ids = set(self._completed_index.keys())
        for seg in new_partials:
            sid = self._get_id(seg)
            if sid is not None:
                if sid in completed_ids:
                    continue
            else:
                if seg in self._completed:
                    continue
            filtered_partials.append(seg)

        self._partial = filtered_partials

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        all_segments = list(self._completed) + list(self._partial)
        text = ''.join(self._extract_text(s) for s in all_segments)
        return {
            'client_uid': self.client_uid,
            'completed': list(self._completed),
            'partial': list(self._partial),
            'all': all_segments,
            'text': text,
        }
