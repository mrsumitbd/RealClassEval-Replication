class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self._partial_segments = []
        self._completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        if partial_segments:
            if isinstance(partial_segments, (list, tuple)):
                self._partial_segments.extend(partial_segments)
            else:
                self._partial_segments.append(partial_segments)
        if completed_segments:
            if isinstance(completed_segments, (list, tuple)):
                self._completed_segments.extend(completed_segments)
            else:
                self._completed_segments.append(completed_segments)

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        response = {
            'client_uid': self.client_uid,
            'partial_segments': list(self._partial_segments),
            'completed_segments': list(self._completed_segments)
        }
        # Clear buffers after preparing response
        self._partial_segments.clear()
        self._completed_segments.clear()
        return response
