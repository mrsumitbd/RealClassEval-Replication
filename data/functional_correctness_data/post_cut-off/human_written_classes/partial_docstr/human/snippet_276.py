import threading

class JobContext:
    """ファンアウトキューなどジョブ固有の状態を保持するクラス"""

    def __init__(self):
        self.bus = FanoutQueue()
        self.done = threading.Event()
        self.stop_mode = None
        self._stop_lock = threading.Lock()

    def should_stop_step(self) -> bool:
        """
        中断モードが「step」で、かつサンプラがまだ'end'を送っていない場合にTrueを返す。
        判定ロジックをヘルパー化して重複を避ける。

        UIからの同時更新を防ぐためロックを取得する。
        ロックしないとstop_modeや_sent_endが判定中に変化する恐れがある。
        """
        with self._stop_lock:
            return self.stop_mode == 'step' and (not getattr(self, '_sent_end', False))

    def reset_stop_mode(self) -> None:
        """
        ジョブ開始時に呼び出し、stop_modeと内部のend送信フラグをリセットする。
        これにより古い状態が次回の実行に影響しない。
        """
        with self._stop_lock:
            self.stop_mode = None
            self._sent_end = False