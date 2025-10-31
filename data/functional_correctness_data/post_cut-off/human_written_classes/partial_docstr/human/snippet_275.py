import weakref
from collections import deque
import queue
import threading

class FanoutQueue:
    """履歴を再生できるスレッドセーフなファンアウトキュー"""

    def __init__(self, maxlen: int=200, maxsize: int=64):
        self._history = deque(maxlen=maxlen)
        self._subs = weakref.WeakSet()
        self._lock = threading.Lock()
        self._maxsize = maxsize
        self._closed = False

    def publish(self, item) -> None:
        """要素を全ての購読者に配信し履歴に保存する"""
        with self._lock:
            if self._closed:
                return
            self._history.append(item)
            for q in list(self._subs):
                try:
                    q.put_nowait(item)
                except queue.Full:
                    try:
                        _ = q.get_nowait()
                        q.put_nowait(item)
                    except Exception:
                        pass

    def subscribe(self) -> queue.Queue:
        """キューに購読し既存の履歴を即座に受け取る"""
        q: queue.Queue = queue.Queue(maxsize=self._maxsize)
        with self._lock:
            for item in list(self._history):
                try:
                    q.put_nowait(item)
                except queue.Full:
                    break
            self._subs.add(q)
        return q

    def unsubscribe(self, q: queue.Queue) -> None:
        with self._lock:
            try:
                self._subs.discard(q)
            except Exception:
                pass

    def clear(self) -> None:
        """履歴と全ての購読キューをクリアする"""
        with self._lock:
            self._history.clear()
            for q in list(self._subs):
                while not q.empty():
                    try:
                        q.get_nowait()
                    except queue.Empty:
                        break

    def close(self) -> None:
        """全ての購読キューを閉じて削除する。センチネルを必ず送信する。"""
        with self._lock:
            if self._closed:
                return
            self._closed = True
            for q in list(self._subs):
                try:
                    q.put_nowait(BUS_END_SENTINEL)
                except queue.Full:
                    try:
                        _ = q.get_nowait()
                        q.put_nowait(BUS_END_SENTINEL)
                    except Exception:
                        pass
            self._subs.clear()