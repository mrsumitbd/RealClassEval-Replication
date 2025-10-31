
class TranscriptionBuffer:

    def __init__(self, client_uid):
        self.client_uid = client_uid
        self.completed_segments = []
        self.partial_segments = []

    def add_segments(self, partial_segments, completed_segments):
        # Add new completed segments, avoiding duplicates
        for seg in completed_segments:
            if seg not in self.completed_segments:
                self.completed_segments.append(seg)
        # Replace partial segments with the latest ones
        self.partial_segments = list(partial_segments)

    def get_segments_for_response(self):
        # Return a tuple of (completed_segments, partial_segments)
        return (list(self.completed_segments), list(self.partial_segments))
