from typing import List, Set, Dict, Tuple
import heapq


class TopKStringTracker:
    def __init__(self, m: int):
        self.m = max(0, int(m))
        self._counts: Dict[str, int] = {}
        self._heap: List[Tuple[int, str]] = []

    def add_strings(self, strings: List[str]) -> None:
        if not strings:
            return
        updated = set()
        for s in strings:
            if s is None:
                continue
            self._counts[s] = self._counts.get(s, 0) + 1
            updated.add(s)
        for s in updated:
            heapq.heappush(self._heap, (self._counts[s], s))
        self._enforce_heap_limit()

    def add_string_dict(self, string_counts: dict) -> None:
        if not string_counts:
            return
        updated = set()
        for s, delta in string_counts.items():
            if s is None:
                continue
            try:
                inc = int(delta)
            except Exception:
                continue
            if inc == 0:
                continue
            new_val = self._counts.get(s, 0) + inc
            if new_val <= 0:
                if s in self._counts:
                    del self._counts[s]
                updated.add(s)  # mark for cleanup
            else:
                self._counts[s] = new_val
                updated.add(s)
        for s in updated:
            if s in self._counts:
                heapq.heappush(self._heap, (self._counts[s], s))
            else:
                heapq.heappush(self._heap, (0, s))
        self._enforce_heap_limit()

    def _cleanup_heap(self) -> None:
        while self._heap and (self._heap[0][1] not in self._counts or self._counts.get(self._heap[0][1], 0) != self._heap[0][0]):
            heapq.heappop(self._heap)

    def get_top_k(self, k: int) -> Set[str]:
        if k <= 0 or not self._counts:
            return set()
        self._cleanup_heap()
        # Gather valid entries from heap snapshot
        seen = set()
        candidates: List[Tuple[int, str]] = []
        for cnt, s in self._heap:
            if s in seen:
                continue
            cur = self._counts.get(s)
            if cur is None or cur != cnt:
                continue
            seen.add(s)
            candidates.append((cnt, s))
        if len(candidates) < min(k, self.m, len(self._counts)):
            # Fallback to exact computation if heap too stale
            for s, cnt in self._counts.items():
                if s not in seen:
                    candidates.append((cnt, s))
        top = heapq.nlargest(min(k, self.m, len(self._counts)),
                             candidates, key=lambda x: (x[0], x[1]))
        return {s for _, s in top}

    def trim_to_m(self) -> None:
        if self.m <= 0 or not self._counts:
            self._counts.clear()
            self._heap.clear()
            return
        # Rebuild exact top-m from counts
        top_m = heapq.nlargest(self.m, self._counts.items(),
                               key=lambda kv: (kv[1], kv[0]))
        keep = dict(top_m)
        self._counts = keep
        self._heap = [(cnt, s) for s, cnt in keep.items()]
        heapq.heapify(self._heap)

    def size(self) -> int:
        return len(self._counts)

    def get_count(self, string: str) -> int:
        return self._counts.get(string, 0)

    def _enforce_heap_limit(self) -> None:
        self._cleanup_heap()
        while len(self._heap) > self.m:
            self._cleanup_heap()
            if not self._heap:
                break
            heapq.heappop(self._heap)
        # Final cleanup to ensure top element validity
        self._cleanup_heap()
