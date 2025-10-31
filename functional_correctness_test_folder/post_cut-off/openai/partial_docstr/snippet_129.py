class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        self.client_uid = client_uid
        # Store segments by unique id
        self._partial_segments = {}   # id -> segment dict
        self._completed_segments = {}  # id -> segment dict

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        # Normalize inputs
        if partial_segments is None:
            partial_segments = []
        if completed_segments is None:
            completed_segments = []

        # Process completed segments first
        for seg in completed_segments:
            seg_id = seg.get('id')
            if seg_id is None:
                continue
            # Mark as completed
            seg_copy = dict(seg)
            seg_copy['completed'] = True
            self._completed_segments[seg_id] = seg_copy
            # Remove from partial if present
            self._partial_segments.pop(seg_id, None)

        # Process partial segments
        for seg in partial_segments:
            seg_id = seg.get('id')
            if seg_id is None:
                continue
            # If already completed, skip
            if seg_id in self._completed_segments:
                continue
            seg_copy = dict(seg)
            seg_copy['completed'] = False
            self._partial_segments[seg_id] = seg_copy

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        # Combine and sort by id (or timestamp if available)
        all_segments = list(self._completed_segments.values()) + \
            list(self._partial_segments.values())
        # Try to sort by 'timestamp' if present, otherwise by 'id'

        def sort_key(seg):
            if 'timestamp' in seg:
                return seg['timestamp']
            return seg.get('id', 0)
        all_segments.sort(key=sort_key)
        # Return a shallow copy to avoid accidental mutation
        return [dict(seg) for seg in all_segments]
