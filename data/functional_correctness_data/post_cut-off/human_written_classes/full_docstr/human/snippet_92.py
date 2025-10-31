from urllib.parse import urlparse
import cv2
from pathlib import Path
import os
import numpy as np
from ultralytics.utils import IS_COLAB, IS_KAGGLE, LOGGER, ops
import time
import torch
from threading import Thread
import math

class LoadStreams:
    """
    Stream Loader for various types of video streams.

    Supports RTSP, RTMP, HTTP, and TCP streams. This class handles the loading and processing of multiple video
    streams simultaneously, making it suitable for real-time video analysis tasks.

    Attributes:
        sources (List[str]): The source input paths or URLs for the video streams.
        vid_stride (int): Video frame-rate stride.
        buffer (bool): Whether to buffer input streams.
        running (bool): Flag to indicate if the streaming thread is running.
        mode (str): Set to 'stream' indicating real-time capture.
        imgs (List[List[np.ndarray]]): List of image frames for each stream.
        fps (List[float]): List of FPS for each stream.
        frames (List[int]): List of total frames for each stream.
        threads (List[Thread]): List of threads for each stream.
        shape (List[Tuple[int, int, int]]): List of shapes for each stream.
        caps (List[cv2.VideoCapture]): List of cv2.VideoCapture objects for each stream.
        bs (int): Batch size for processing.

    Methods:
        update: Read stream frames in daemon thread.
        close: Close stream loader and release resources.
        __iter__: Returns an iterator object for the class.
        __next__: Returns source paths, transformed, and original images for processing.
        __len__: Return the length of the sources object.

    Examples:
        >>> stream_loader = LoadStreams("rtsp://example.com/stream1.mp4")
        >>> for sources, imgs, _ in stream_loader:
        ...     # Process the images
        ...     pass
        >>> stream_loader.close()

    Notes:
        - The class uses threading to efficiently load frames from multiple streams simultaneously.
        - It automatically handles YouTube links, converting them to the best available stream URL.
        - The class implements a buffer system to manage frame storage and retrieval.
    """

    def __init__(self, sources='file.streams', vid_stride=1, buffer=False):
        """Initialize stream loader for multiple video sources, supporting various stream types."""
        torch.backends.cudnn.benchmark = True
        self.buffer = buffer
        self.running = True
        self.mode = 'stream'
        self.vid_stride = vid_stride
        sources = Path(sources).read_text().rsplit() if os.path.isfile(sources) else [sources]
        n = len(sources)
        self.bs = n
        self.fps = [0] * n
        self.frames = [0] * n
        self.threads = [None] * n
        self.caps = [None] * n
        self.imgs = [[] for _ in range(n)]
        self.shape = [[] for _ in range(n)]
        self.sources = [ops.clean_str(x) for x in sources]
        for i, s in enumerate(sources):
            st = f'{i + 1}/{n}: {s}... '
            if urlparse(s).hostname in {'www.youtube.com', 'youtube.com', 'youtu.be'}:
                s = get_best_youtube_url(s)
            s = eval(s) if s.isnumeric() else s
            if s == 0 and (IS_COLAB or IS_KAGGLE):
                raise NotImplementedError("'source=0' webcam not supported in Colab and Kaggle notebooks. Try running 'source=0' in a local environment.")
            self.caps[i] = cv2.VideoCapture(s)
            if not self.caps[i].isOpened():
                raise ConnectionError(f'{st}Failed to open {s}')
            w = int(self.caps[i].get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(self.caps[i].get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.caps[i].get(cv2.CAP_PROP_FPS)
            self.frames[i] = max(int(self.caps[i].get(cv2.CAP_PROP_FRAME_COUNT)), 0) or float('inf')
            self.fps[i] = max((fps if math.isfinite(fps) else 0) % 100, 0) or 30
            success, im = self.caps[i].read()
            if not success or im is None:
                raise ConnectionError(f'{st}Failed to read images from {s}')
            self.imgs[i].append(im)
            self.shape[i] = im.shape
            self.threads[i] = Thread(target=self.update, args=[i, self.caps[i], s], daemon=True)
            LOGGER.info(f'{st}Success ✅ ({self.frames[i]} frames of shape {w}x{h} at {self.fps[i]:.2f} FPS)')
            self.threads[i].start()
        LOGGER.info('')

    def update(self, i, cap, stream):
        """Read stream frames in daemon thread and update image buffer."""
        n, f = (0, self.frames[i])
        while self.running and cap.isOpened() and (n < f - 1):
            if len(self.imgs[i]) < 30:
                n += 1
                cap.grab()
                if n % self.vid_stride == 0:
                    success, im = cap.retrieve()
                    if not success:
                        im = np.zeros(self.shape[i], dtype=np.uint8)
                        LOGGER.warning('WARNING ⚠️ Video stream unresponsive, please check your IP camera connection.')
                        cap.open(stream)
                    if self.buffer:
                        self.imgs[i].append(im)
                    else:
                        self.imgs[i] = [im]
            else:
                time.sleep(0.01)

    def close(self):
        """Terminates stream loader, stops threads, and releases video capture resources."""
        self.running = False
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)
        for cap in self.caps:
            try:
                cap.release()
            except Exception as e:
                LOGGER.warning(f'WARNING ⚠️ Could not release VideoCapture object: {e}')
        cv2.destroyAllWindows()

    def __iter__(self):
        """Iterates through YOLO image feed and re-opens unresponsive streams."""
        self.count = -1
        return self

    def __next__(self):
        """Returns the next batch of frames from multiple video streams for processing."""
        self.count += 1
        images = []
        for i, x in enumerate(self.imgs):
            while not x:
                if not self.threads[i].is_alive() or cv2.waitKey(1) == ord('q'):
                    self.close()
                    raise StopIteration
                time.sleep(1 / min(self.fps))
                x = self.imgs[i]
                if not x:
                    LOGGER.warning(f'WARNING ⚠️ Waiting for stream {i}')
            if self.buffer:
                images.append(x.pop(0))
            else:
                images.append(x.pop(-1) if x else np.zeros(self.shape[i], dtype=np.uint8))
                x.clear()
        return (self.sources, images, [''] * self.bs)

    def __len__(self):
        """Return the number of video streams in the LoadStreams object."""
        return self.bs