import threading
import time
import itertools
from collections import OrderedDict


class TranscriptionBuffer:
    """Manages buffers of transcription segments for a client"""

    def __init__(self, client_uid):
        """Initialize with client ID"""
        self.client_uid = str(client_uid)
        self._lock = threading.RLock()
        self._partial = OrderedDict()    # id -> record
        self._completed = OrderedDict()  # id -> record
        self._seq_counter = itertools.count()

    def add_segments(self, partial_segments, completed_segments):
        """Add new segments to the appropriate buffers"""
        with self._lock:
            # Handle completed segments first so they can supersede partials
            for seg in self._iter_segments(completed_segments):
                rec = self._normalize(seg, is_final=True)
                sid = rec["id"] or self._new_id()
                # If already completed, update text/metadata; keep original seq
                if sid in self._completed:
                    existing = self._completed[sid]
                    existing.update(self._merge_update(existing, rec))
                    existing["final"] = True
                    existing["updated_at"] = time.time()
                else:
                    rec["id"] = sid
                    rec["seq"] = next(self._seq_counter)
                    rec["created_at"] = time.time()
                    rec["updated_at"] = rec["created_at"]
                    self._completed[sid] = rec
                # Remove from partials if present
                if sid in self._partial:
                    del self._partial[sid]

            # Now handle partial segments
            for seg in self._iter_segments(partial_segments):
                rec = self._normalize(seg, is_final=False)
                sid = rec["id"] or self._new_id()
                # Do not add partial if it's already completed
                if sid in self._completed:
                    continue
                if sid in self._partial:
                    existing = self._partial[sid]
                    existing.update(self._merge_update(existing, rec))
                    existing["final"] = False
                    existing["updated_at"] = time.time()
                else:
                    rec["id"] = sid
                    rec["seq"] = next(self._seq_counter)
                    rec["created_at"] = time.time()
                    rec["updated_at"] = rec["created_at"]
                    self._partial[sid] = rec

    def get_segments_for_response(self):
        """Get formatted segments for client response"""
        with self._lock:
            completed = sorted(
                self._completed.values(),
                key=lambda r: self._order_key(r),
            )
            partial = sorted(
                self._partial.values(),
                key=lambda r: self._order_key(r),
            )

            def pub(rec):
                return {
                    "id": str(rec.get("id")),
                    "text": rec.get("text", ""),
                    "start": rec.get("start"),
                    "end": rec.get("end"),
                    "final": bool(rec.get("final", False)),
                }

            return {
                "client_uid": self.client_uid,
                "completed": [pub(r) for r in completed],
                "partial": [pub(r) for r in partial],
            }

    # Internal helpers

    def _iter_segments(self, segs):
        if segs is None:
            return []
        if isinstance(segs, (list, tuple)):
            return segs
        return [segs]

    def _normalize(self, seg, is_final=False):
        now = time.time()
        rec = {
            "id": None,
            "text": "",
            "start": None,
            "end": None,
            "final": bool(is_final),
            "created_at": now,
            "updated_at": now,
        }

        if isinstance(seg, dict):
            sid = (
                seg.get("id")
                or seg.get("segment_id")
                or seg.get("uid")
                or seg.get("uuid")
            )
            rec["id"] = sid
            text = seg.get("text")
            if text is None:
                text = seg.get("transcript") or seg.get("content") or ""
            rec["text"] = str(text)
            rec["start"] = self._coerce_time(
                seg.get("start") or seg.get("start_time") or seg.get("ts"))
            rec["end"] = self._coerce_time(
                seg.get("end") or seg.get("end_time"))
            if any(k in seg for k in ("final", "completed", "is_final", "is_completed")):
                rec["final"] = bool(
                    seg.get("final")
                    or seg.get("completed")
                    or seg.get("is_final")
                    or seg.get("is_completed")
                )
                if is_final:
                    rec["final"] = True
        elif isinstance(seg, (str, bytes)):
            rec["text"] = seg.decode(
                "utf-8", errors="ignore") if isinstance(seg, bytes) else seg
        else:
            rec["text"] = str(seg)

        return rec

    def _merge_update(self, existing, newrec):
        merged = {}
        if newrec.get("text", ""):
            merged["text"] = newrec["text"]
        if newrec.get("start") is not None:
            merged["start"] = newrec["start"]
        if newrec.get("end") is not None:
            merged["end"] = newrec["end"]
        return merged

    def _coerce_time(self, v):
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        try:
            return float(v)
        except Exception:
            return None

    def _order_key(self, rec):
        start = rec.get("start")
        has_start = 0 if start is not None else 1
        start_val = start if start is not None else 0.0
        return (has_start, start_val, rec.get("seq", 0))

    def _new_id(self):
        # Generate a simple unique id within this buffer instance
        return f"{self.client_uid}:{next(self._seq_counter)}"
