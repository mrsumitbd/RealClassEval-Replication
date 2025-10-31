import cv2
from ultralytics.utils.patches import imread
from PIL import Image
import glob
import numpy as np
from pathlib import Path
import os
from ultralytics.utils.checks import check_requirements
from ultralytics.utils import IS_COLAB, IS_KAGGLE, LOGGER, ops
from ultralytics.data.utils import FORMATS_HELP_MSG, IMG_FORMATS, VID_FORMATS
import math

class LoadImagesAndVideos:
    """
    A class for loading and processing images and videos for YOLO object detection.

    This class manages the loading and pre-processing of image and video data from various sources, including
    single image files, video files, and lists of image and video paths.

    Attributes:
        files (List[str]): List of image and video file paths.
        nf (int): Total number of files (images and videos).
        video_flag (List[bool]): Flags indicating whether a file is a video (True) or an image (False).
        mode (str): Current mode, 'image' or 'video'.
        vid_stride (int): Stride for video frame-rate.
        bs (int): Batch size.
        cap (cv2.VideoCapture): Video capture object for OpenCV.
        frame (int): Frame counter for video.
        frames (int): Total number of frames in the video.
        count (int): Counter for iteration, initialized at 0 during __iter__().
        ni (int): Number of images.

    Methods:
        __init__: Initialize the LoadImagesAndVideos object.
        __iter__: Returns an iterator object for VideoStream or ImageFolder.
        __next__: Returns the next batch of images or video frames along with their paths and metadata.
        _new_video: Creates a new video capture object for the given path.
        __len__: Returns the number of batches in the object.

    Examples:
        >>> loader = LoadImagesAndVideos("path/to/data", batch=32, vid_stride=1)
        >>> for paths, imgs, info in loader:
        ...     # Process batch of images or video frames
        ...     pass

    Notes:
        - Supports various image formats including HEIC.
        - Handles both local files and directories.
        - Can read from a text file containing paths to images and videos.
    """

    def __init__(self, path, batch=1, vid_stride=1):
        """Initialize dataloader for images and videos, supporting various input formats."""
        parent = None
        if isinstance(path, str) and Path(path).suffix == '.txt':
            parent = Path(path).parent
            path = Path(path).read_text().splitlines()
        files = []
        for p in sorted(path) if isinstance(path, (list, tuple)) else [path]:
            a = str(Path(p).absolute())
            if '*' in a:
                files.extend(sorted(glob.glob(a, recursive=True)))
            elif os.path.isdir(a):
                files.extend(sorted(glob.glob(os.path.join(a, '*.*'))))
            elif os.path.isfile(a):
                files.append(a)
            elif parent and (parent / p).is_file():
                files.append(str((parent / p).absolute()))
            else:
                raise FileNotFoundError(f'{p} does not exist')
        images, videos = ([], [])
        for f in files:
            suffix = f.split('.')[-1].lower()
            if suffix in IMG_FORMATS:
                images.append(f)
            elif suffix in VID_FORMATS:
                videos.append(f)
        ni, nv = (len(images), len(videos))
        self.files = images + videos
        self.nf = ni + nv
        self.ni = ni
        self.video_flag = [False] * ni + [True] * nv
        self.mode = 'video' if ni == 0 else 'image'
        self.vid_stride = vid_stride
        self.bs = batch
        if any(videos):
            self._new_video(videos[0])
        else:
            self.cap = None
        if self.nf == 0:
            raise FileNotFoundError(f'No images or videos found in {p}. {FORMATS_HELP_MSG}')

    def __iter__(self):
        """Iterates through image/video files, yielding source paths, images, and metadata."""
        self.count = 0
        return self

    def __next__(self):
        """Returns the next batch of images or video frames with their paths and metadata."""
        paths, imgs, info = ([], [], [])
        while len(imgs) < self.bs:
            if self.count >= self.nf:
                if imgs:
                    return (paths, imgs, info)
                else:
                    raise StopIteration
            path = self.files[self.count]
            if self.video_flag[self.count]:
                self.mode = 'video'
                if not self.cap or not self.cap.isOpened():
                    self._new_video(path)
                success = False
                for _ in range(self.vid_stride):
                    success = self.cap.grab()
                    if not success:
                        break
                if success:
                    success, im0 = self.cap.retrieve()
                    if success:
                        self.frame += 1
                        paths.append(path)
                        imgs.append(im0)
                        info.append(f'video {self.count + 1}/{self.nf} (frame {self.frame}/{self.frames}) {path}: ')
                        if self.frame == self.frames:
                            self.count += 1
                            self.cap.release()
                else:
                    self.count += 1
                    if self.cap:
                        self.cap.release()
                    if self.count < self.nf:
                        self._new_video(self.files[self.count])
            else:
                self.mode = 'image'
                if path.split('.')[-1].lower() == 'heic':
                    check_requirements('pillow-heif')
                    from pillow_heif import register_heif_opener
                    register_heif_opener()
                    with Image.open(path) as img:
                        im0 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
                else:
                    im0 = imread(path)
                if im0 is None:
                    LOGGER.warning(f'WARNING ⚠️ Image Read Error {path}')
                else:
                    paths.append(path)
                    imgs.append(im0)
                    info.append(f'image {self.count + 1}/{self.nf} {path}: ')
                self.count += 1
                if self.count >= self.ni:
                    break
        return (paths, imgs, info)

    def _new_video(self, path):
        """Creates a new video capture object for the given path and initializes video-related attributes."""
        self.frame = 0
        self.cap = cv2.VideoCapture(path)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if not self.cap.isOpened():
            raise FileNotFoundError(f'Failed to open video {path}')
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.vid_stride)

    def __len__(self):
        """Returns the number of files (images and videos) in the dataset."""
        return math.ceil(self.nf / self.bs)