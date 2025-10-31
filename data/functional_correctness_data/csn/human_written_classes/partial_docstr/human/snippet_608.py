import traceback

class SegmentContextManager:
    """
    Wrapper for segment and recorder to provide segment context manager.
    """

    def __init__(self, recorder, name=None, **segment_kwargs):
        self.name = name
        self.segment_kwargs = segment_kwargs
        self.recorder = recorder
        self.segment = None

    def __enter__(self):
        self.segment = self.recorder.begin_segment(name=self.name, **self.segment_kwargs)
        return self.segment

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.segment is None:
            return
        if exc_type is not None:
            self.segment.add_exception(exc_val, traceback.extract_tb(exc_tb, limit=self.recorder.max_trace_back))
        self.recorder.end_segment()