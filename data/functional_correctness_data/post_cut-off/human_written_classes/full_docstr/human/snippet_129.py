class TranscriptionBuffer:
    """Manages buffers of transcription segments for a client"""

    def __init__(self, client_uid):
        """Initialize with client ID"""
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []
        self.max_segments = 50

    def add_segments(self, partial_segments, completed_segments):
        """Add new segments to the appropriate buffers"""
        if partial_segments:
            self.partial_segments = partial_segments
        if completed_segments:
            self.completed_segments.extend(completed_segments)
            if len(self.completed_segments) > self.max_segments:
                self.completed_segments = self.completed_segments[-self.max_segments:]

    def get_segments_for_response(self):
        """Get formatted segments for client response"""
        result = []
        if self.completed_segments:
            result.extend(self.completed_segments)
        if self.partial_segments:
            result.extend(self.partial_segments)
        return result