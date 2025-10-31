import time
from src.utils.logger import logger
import threading
import cv2
import numpy as np
import mss

class GameWindowCapturor:
    """
    GameWindowCapturor for macOS
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.frame = None
        self.lock = threading.Lock()
        self.is_terminated = False
        self.window_title = get_window_title(cfg['game_window']['title'])
        if self.window_title is None:
            logger.error(f"[GameWindowCapturor] Unable to find window titles that contain {cfg['game_window']['title']}")
            return -1
        self.fps = 0
        self.fps_limit = cfg['system']['fps_limit_window_capturor']
        self.t_last_run = 0.0
        self.capture = mss.mss()
        self.update_window_region()
        threading.Thread(target=self.start_capture, daemon=True).start()
        time.sleep(0.1)
        while self.frame is None:
            self.limit_fps()

    def start_capture(self):
        """
        開始螢幕擷取，並不斷更新 frame。
        """
        while not self.is_terminated:
            self.update_window_region()
            self.capture_frame()
            self.limit_fps()

    def stop(self):
        """
        Stop capturing thread
        """
        self.is_terminated = True
        logger.info('[GameWindowCapturor] Terminated')

    def update_window_region(self):
        """
        Update window region
        """
        self.region = get_window_region(self.window_title)
        if self.region is None:
            text = f'Cannot find window: {self.window_title}'
            logger.error(text)
            raise RuntimeError(text)

    def capture_frame(self):
        """
        捕捉當前遊戲區域畫面
        """
        img = self.capture.grab(self.region)
        frame = np.array(img)
        with self.lock:
            self.frame = frame

    def get_frame(self):
        """
        安全地獲取最新的螢幕畫面
        """
        with self.lock:
            if self.frame is None:
                return None
            return cv2.cvtColor(self.frame, cv2.COLOR_BGRA2BGR)

    def on_closed(self):
        """
        捕捉結束後的回調
        """
        logger.warning('Capture session closed.')
        cv2.destroyAllWindows()

    def limit_fps(self):
        """
        Limit FPS
        """
        target_duration = 1.0 / self.fps_limit
        frame_duration = time.time() - self.t_last_run
        if frame_duration < target_duration:
            time.sleep(target_duration - frame_duration)
        self.fps = round(1.0 / (time.time() - self.t_last_run))
        self.t_last_run = time.time()