
class TranscriptionBuffer:

    def __init__(self, client_uid):
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        self.partial_segments = partial_segments
        self.completed_segments.extend(completed_segments)

    def get_segments_for_response(self):
        return {
            "partial": self.partial_segments,
            "completed": self.completed_segments
        }
