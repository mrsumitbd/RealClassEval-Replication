
class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        self.partial_segments.extend(partial_segments)
        self.completed_segments.extend(completed_segments)

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        response_segments = {
            'client_uid': self.client_uid,
            'partial_segments': self.partial_segments,
            'completed_segments': self.completed_segments
        }
        # Clear the buffers after sending the response
        self.partial_segments = []
        self.completed_segments = []
        return response_segments
