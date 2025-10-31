from windows_capture import WindowsCapture, Frame, InternalCaptureControl
import threading
from src.utils.common import get_game_window_title_by_token, load_image, resize_window
import time
from src.utils.logger import logger
import cv2

class GameWindowCapturor:
    """
    GameWindowCapturor
    """

    def __init__(self, cfg, test_image_name=None):
        self.cfg = cfg
        self.frame = None
        self.lock = threading.Lock()
        self.is_terminated = False
        self.fps = 0
        self.fps_limit = cfg['system']['fps_limit_window_capturor']
        self.t_last_run = 0.0
        self.capture_control = None
        self.window_title = ''
        if test_image_name is not None:
            self.frame = load_image(f'test/{test_image_name}.png')
            return
        self.window_title = get_game_window_title_by_token(cfg['game_window']['title'])
        resize_window(self.window_title, width=1296, height=759)
        if self.window_title is None:
            raise RuntimeError(f"[GameWindowCapturor] Unable to find window title containing: {cfg['game_window']['title']}")
        else:
            logger.info(f'[GameWindowCapturor] Found game window title: {self.window_title}')
        self.capture = WindowsCapture(window_name=self.window_title)
        self.capture.event(self.on_frame_arrived)
        self.capture.event(self.on_closed)
        self.capture_control = self.capture.start_free_threaded()
        logger.info('[GameWindowCapturor] Init done')

    def on_frame_arrived(self, frame: Frame, capture_control: InternalCaptureControl):
        """
        Frame arrived callback: store frame into buffer with lock.
        """
        with self.lock:
            self.frame = frame.frame_buffer
        self.limit_fps()

    def on_closed(self):
        """
        Capture closed callback.
        """
        logger.warning('[GameWindowCapturor] closed.')
        cv2.destroyAllWindows()

    def get_frame(self):
        """
        Safely get latest game window frame.
        """
        with self.lock:
            if self.frame is None:
                return None
            return cv2.cvtColor(self.frame, cv2.COLOR_BGRA2BGR)

    def stop(self):
        """
        Stop capturing thread
        """
        if self.capture_control is not None:
            self.capture_control.stop()
        logger.info('[GameWindowCapturor] Terminated')

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