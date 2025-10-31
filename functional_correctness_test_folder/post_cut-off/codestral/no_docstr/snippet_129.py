
class TranscriptionBuffer:

    def __init__(self, client_uid):
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        self.partial_segments.extend(partial_segments)
        self.completed_segments.extend(completed_segments)

    def get_segments_for_response(self):
        response = {
            'client_uid': self.client_uid,
            'partial_segments': self.partial_segments,
            'completed_segments': self.completed_segments
        }
        self.partial_segments = []
        self.completed_segments = []
        return response
