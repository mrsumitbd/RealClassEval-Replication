class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self._partial_buffer = []
        self._completed_buffer = []

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        if partial_segments:
            self._partial_buffer.extend(partial_segments)
        if completed_segments:
            self._completed_buffer.extend(completed_segments)

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        response = {
            'client_uid': self.client_uid,
            'partial_segments': list(self._partial_buffer),
            'completed_segments': list(self._completed_buffer)
        }
        # Clear buffers after preparing response
        self._partial_buffer.clear()
        self._completed_buffer.clear()
        return response
