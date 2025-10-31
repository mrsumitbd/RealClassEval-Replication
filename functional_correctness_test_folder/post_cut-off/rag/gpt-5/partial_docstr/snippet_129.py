import threading
import json
import copy


class TranscriptionBuffer:
    '''Manages buffers of transcription segments for a client'''

    def __init__(self, client_uid):
        '''Initialize with client ID'''
        self.client_uid = client_uid
        self._partial = []
        self._completed = []
        self._seen_completed_keys = set()
        self._lock = threading.RLock()

    def _segment_key(self, seg):
        if isinstance(seg, dict):
            for k in ("id", "segment_id", "uid", "uuid"):
                if k in seg:
                    return ("key", seg[k])
            try:
                return ("json", json.dumps(seg, sort_keys=True, ensure_ascii=False))
            except Exception:
                pass
        return ("obj", id(seg))

    def add_segments(self, partial_segments, completed_segments):
        '''Add new segments to the appropriate buffers'''
        with self._lock:
            if partial_segments is not None:
                self._partial = list(partial_segments)

            if completed_segments:
                for seg in completed_segments:
                    key = self._segment_key(seg)
                    if key in self._seen_completed_keys:
                        continue
                    self._completed.append(seg)
                    self._seen_completed_keys.add(key)

    def get_segments_for_response(self):
        '''Get formatted segments for client response'''
        with self._lock:
            return {
                "client_uid": self.client_uid,
                "completed_segments": copy.deepcopy(self._completed),
                "partial_segments": copy.deepcopy(self._partial),
            }
