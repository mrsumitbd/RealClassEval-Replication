from ultralytics.data.utils import polygons2masks, polygons2masks_overlap
import torch
import random
import numpy as np
from ultralytics.utils.ops import segment2box, xyxyxyxy2xywhr

class Format:
    """
    A class for formatting image annotations for object detection, instance segmentation, and pose estimation tasks.

    This class standardizes image and instance annotations to be used by the `collate_fn` in PyTorch DataLoader.

    Attributes:
        bbox_format (str): Format for bounding boxes. Options are 'xywh' or 'xyxy'.
        normalize (bool): Whether to normalize bounding boxes.
        return_mask (bool): Whether to return instance masks for segmentation.
        return_keypoint (bool): Whether to return keypoints for pose estimation.
        return_obb (bool): Whether to return oriented bounding boxes.
        mask_ratio (int): Downsample ratio for masks.
        mask_overlap (bool): Whether to overlap masks.
        batch_idx (bool): Whether to keep batch indexes.
        bgr (float): The probability to return BGR images.

    Methods:
        __call__: Formats labels dictionary with image, classes, bounding boxes, and optionally masks and keypoints.
        _format_img: Converts image from Numpy array to PyTorch tensor.
        _format_segments: Converts polygon points to bitmap masks.

    Examples:
        >>> formatter = Format(bbox_format="xywh", normalize=True, return_mask=True)
        >>> formatted_labels = formatter(labels)
        >>> img = formatted_labels["img"]
        >>> bboxes = formatted_labels["bboxes"]
        >>> masks = formatted_labels["masks"]
    """

    def __init__(self, bbox_format='xywh', normalize=True, return_mask=False, return_keypoint=False, return_obb=False, mask_ratio=4, mask_overlap=True, batch_idx=True, bgr=0.0):
        """
        Initializes the Format class with given parameters for image and instance annotation formatting.

        This class standardizes image and instance annotations for object detection, instance segmentation, and pose
        estimation tasks, preparing them for use in PyTorch DataLoader's `collate_fn`.

        Args:
            bbox_format (str): Format for bounding boxes. Options are 'xywh', 'xyxy', etc.
            normalize (bool): Whether to normalize bounding boxes to [0,1].
            return_mask (bool): If True, returns instance masks for segmentation tasks.
            return_keypoint (bool): If True, returns keypoints for pose estimation tasks.
            return_obb (bool): If True, returns oriented bounding boxes.
            mask_ratio (int): Downsample ratio for masks.
            mask_overlap (bool): If True, allows mask overlap.
            batch_idx (bool): If True, keeps batch indexes.
            bgr (float): Probability of returning BGR images instead of RGB.

        Attributes:
            bbox_format (str): Format for bounding boxes.
            normalize (bool): Whether bounding boxes are normalized.
            return_mask (bool): Whether to return instance masks.
            return_keypoint (bool): Whether to return keypoints.
            return_obb (bool): Whether to return oriented bounding boxes.
            mask_ratio (int): Downsample ratio for masks.
            mask_overlap (bool): Whether masks can overlap.
            batch_idx (bool): Whether to keep batch indexes.
            bgr (float): The probability to return BGR images.

        Examples:
            >>> format = Format(bbox_format="xyxy", return_mask=True, return_keypoint=False)
            >>> print(format.bbox_format)
            xyxy
        """
        self.bbox_format = bbox_format
        self.normalize = normalize
        self.return_mask = return_mask
        self.return_keypoint = return_keypoint
        self.return_obb = return_obb
        self.mask_ratio = mask_ratio
        self.mask_overlap = mask_overlap
        self.batch_idx = batch_idx
        self.bgr = bgr

    def __call__(self, labels):
        """
        Formats image annotations for object detection, instance segmentation, and pose estimation tasks.

        This method standardizes the image and instance annotations to be used by the `collate_fn` in PyTorch
        DataLoader. It processes the input labels dictionary, converting annotations to the specified format and
        applying normalization if required.

        Args:
            labels (Dict): A dictionary containing image and annotation data with the following keys:
                - 'img': The input image as a numpy array.
                - 'cls': Class labels for instances.
                - 'instances': An Instances object containing bounding boxes, segments, and keypoints.

        Returns:
            (Dict): A dictionary with formatted data, including:
                - 'img': Formatted image tensor.
                - 'cls': Class label's tensor.
                - 'bboxes': Bounding boxes tensor in the specified format.
                - 'masks': Instance masks tensor (if return_mask is True).
                - 'keypoints': Keypoints tensor (if return_keypoint is True).
                - 'batch_idx': Batch index tensor (if batch_idx is True).

        Examples:
            >>> formatter = Format(bbox_format="xywh", normalize=True, return_mask=True)
            >>> labels = {"img": np.random.rand(640, 640, 3), "cls": np.array([0, 1]), "instances": Instances(...)}
            >>> formatted_labels = formatter(labels)
            >>> print(formatted_labels.keys())
        """
        img = labels.pop('img')
        h, w = img.shape[:2]
        cls = labels.pop('cls')
        instances = labels.pop('instances')
        instances.convert_bbox(format=self.bbox_format)
        instances.denormalize(w, h)
        nl = len(instances)
        if self.return_mask:
            if nl:
                masks, instances, cls = self._format_segments(instances, cls, w, h)
                masks = torch.from_numpy(masks)
            else:
                masks = torch.zeros(1 if self.mask_overlap else nl, img.shape[0] // self.mask_ratio, img.shape[1] // self.mask_ratio)
            labels['masks'] = masks
        labels['img'] = self._format_img(img)
        labels['cls'] = torch.from_numpy(cls) if nl else torch.zeros(nl)
        labels['bboxes'] = torch.from_numpy(instances.bboxes) if nl else torch.zeros((nl, 4))
        if self.return_keypoint:
            labels['keypoints'] = torch.from_numpy(instances.keypoints)
            if self.normalize:
                labels['keypoints'][..., 0] /= w
                labels['keypoints'][..., 1] /= h
        if self.return_obb:
            labels['bboxes'] = xyxyxyxy2xywhr(torch.from_numpy(instances.segments)) if len(instances.segments) else torch.zeros((0, 5))
        if self.normalize:
            labels['bboxes'][:, [0, 2]] /= w
            labels['bboxes'][:, [1, 3]] /= h
        if self.batch_idx:
            labels['batch_idx'] = torch.zeros(nl)
        return labels

    def _format_img(self, img):
        """
        Formats an image for YOLO from a Numpy array to a PyTorch tensor.

        This function performs the following operations:
        1. Ensures the image has 3 dimensions (adds a channel dimension if needed).
        2. Transposes the image from HWC to CHW format.
        3. Optionally flips the color channels from RGB to BGR.
        4. Converts the image to a contiguous array.
        5. Converts the Numpy array to a PyTorch tensor.

        Args:
            img (np.ndarray): Input image as a Numpy array with shape (H, W, C) or (H, W).

        Returns:
            (torch.Tensor): Formatted image as a PyTorch tensor with shape (C, H, W).

        Examples:
            >>> import numpy as np
            >>> img = np.random.rand(100, 100, 3)
            >>> formatted_img = self._format_img(img)
            >>> print(formatted_img.shape)
            torch.Size([3, 100, 100])
        """
        if len(img.shape) < 3:
            img = np.expand_dims(img, -1)
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img[::-1] if random.uniform(0, 1) > self.bgr else img)
        img = torch.from_numpy(img)
        return img

    def _format_segments(self, instances, cls, w, h):
        """
        Converts polygon segments to bitmap masks.

        Args:
            instances (Instances): Object containing segment information.
            cls (numpy.ndarray): Class labels for each instance.
            w (int): Width of the image.
            h (int): Height of the image.

        Returns:
            masks (numpy.ndarray): Bitmap masks with shape (N, H, W) or (1, H, W) if mask_overlap is True.
            instances (Instances): Updated instances object with sorted segments if mask_overlap is True.
            cls (numpy.ndarray): Updated class labels, sorted if mask_overlap is True.

        Notes:
            - If self.mask_overlap is True, masks are overlapped and sorted by area.
            - If self.mask_overlap is False, each mask is represented separately.
            - Masks are downsampled according to self.mask_ratio.
        """
        segments = instances.segments
        if self.mask_overlap:
            masks, sorted_idx = polygons2masks_overlap((h, w), segments, downsample_ratio=self.mask_ratio)
            masks = masks[None]
            instances = instances[sorted_idx]
            cls = cls[sorted_idx]
        else:
            masks = polygons2masks((h, w), segments, color=1, downsample_ratio=self.mask_ratio)
        return (masks, instances, cls)