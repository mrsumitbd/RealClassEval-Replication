
class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        if completed_segments:
            self.completed_segments.extend(completed_segments)
            self.partial_segments.clear()
        if partial_segments:
            self.partial_segments = list(partial_segments)

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        response = []
        response.extend(self.completed_segments)
        response.extend(self.partial_segments)
        return response
