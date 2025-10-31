
class TranscriptionBuffer:

    def __init__(self, client_uid):
        """
        Initialize the TranscriptionBuffer instance.

        Args:
        client_uid (str): Unique identifier for the client.
        """
        self.client_uid = client_uid
        self.partial_segments = []
        self.completed_segments = []

    def add_segments(self, partial_segments, completed_segments):
        """
        Add new partial and completed segments to the buffer.

        Args:
        partial_segments (list): List of partial transcription segments.
        completed_segments (list): List of completed transcription segments.
        """
        self.partial_segments.extend(partial_segments)
        self.completed_segments.extend(completed_segments)

    def get_segments_for_response(self):
        """
        Get the segments to be included in the response.

        Returns:
        tuple: A tuple containing the list of partial segments and the list of completed segments.
        The completed segments are cleared after being retrieved.
        """
        response_segments = (
            self.partial_segments[:], self.completed_segments[:])
        self.partial_segments = []
        self.completed_segments = []
        return response_segments
