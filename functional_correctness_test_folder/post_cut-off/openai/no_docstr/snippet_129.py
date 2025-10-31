
class TranscriptionBuffer:
    """
    A simple buffer for storing transcription segments per client.
    Each segment is expected to be a dict containing at least an 'id' key.
    Partial segments are marked with 'is_partial': True.
    Completed segments are marked with 'is_partial': False.
    """

    def __init__(self, client_uid):
        """
        Initialize the buffer for a specific client.

        :param client_uid: Unique identifier for the client.
        """
        self.client_uid = client_uid
        # Internal storage: mapping from segment id to segment dict
        self._segments = {}

    def add_segments(self, partial_segments, completed_segments):
        """
        Add new partial and completed segments to the buffer.

        :param partial_segments: Iterable of segment dicts that are partial.
        :param completed_segments: Iterable of segment dicts that are completed.
        """
        # Add or update partial segments
        for seg in partial_segments:
            seg_id = seg.get('id')
            if seg_id is None:
                continue  # skip segments without an id
            # Preserve existing completed data if present
            existing = self._segments.get(seg_id, {})
            seg_copy = dict(seg)  # shallow copy to avoid side effects
            seg_copy['is_partial'] = True
            # Merge with existing data (e.g., keep completed flag if already set)
            seg_copy.update(existing)
            self._segments[seg_id] = seg_copy

        # Add or update completed segments
        for seg in completed_segments:
            seg_id = seg.get('id')
            if seg_id is None:
                continue
            seg_copy = dict(seg)
            seg_copy['is_partial'] = False
            self._segments[seg_id] = seg_copy

    def get_segments_for_response(self):
        """
        Retrieve all segments in the buffer sorted by their id and clear the buffer.

        :return: List of segment dicts ready to be sent in a response.
        """
        # Sort segments by id (assuming ids are comparable)
        sorted_segments = sorted(
            self._segments.values(), key=lambda s: s.get('id'))
        # Clear the buffer
        self._segments.clear()
        return sorted_segments
