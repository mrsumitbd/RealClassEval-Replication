import numpy as np


class CenterCrop:
    '''
    Applies center cropping to images for classification tasks.
    This class performs center cropping on input images, resizing them to a specified size while maintaining the aspect
    ratio. It is designed to be part of a transformation pipeline, e.g., T.Compose([CenterCrop(size), ToTensor()]).
    Attributes:
        h (int): Target height of the cropped image.
        w (int): Target width of the cropped image.
    Methods:
        __call__: Applies the center crop transformation to an input image.
    Examples:
        >>> transform = CenterCrop(640)
        >>> image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        >>> cropped_image = transform(image)
        >>> print(cropped_image.shape)
        (640, 640, 3)
    '''

    def __init__(self, size=640):
        '''
            Initializes the CenterCrop object for image preprocessing.
            This class is designed to be part of a transformation pipeline, e.g., T.Compose([CenterCrop(size), ToTensor()]).
            It performs a center crop on input images to a specified size.
            Args:
                size (int | Tuple[int, int]): The desired output size of the crop. If size is an int, a square crop
                    (size, size) is made. If size is a sequence like (h, w), it is used as the output size.
            Returns:
                (None): This method initializes the object and does not return anything.
            Examples:
                >>> transform = CenterCrop(224)
                >>> img = np.random.rand(300, 300, 3)
                >>> cropped_img = transform(img)
                >>> print(cropped_img.shape)
                (224, 224, 3)
        '''
        if isinstance(size, (list, tuple)):
            if len(size) != 2:
                raise ValueError(
                    "size must be an int or a tuple/list of length 2 (h, w)")
            self.h, self.w = int(size[0]), int(size[1])
        else:
            self.h = self.w = int(size)

        if self.h <= 0 or self.w <= 0:
            raise ValueError("size dimensions must be positive integers")

    def __call__(self, im):
        '''
        Applies center cropping to an input image.
        This method resizes and crops the center of the image using a letterbox method. It maintains the aspect
        ratio of the original image while fitting it into the specified dimensions.
        Args:
            im (numpy.ndarray | PIL.Image.Image): The input image as a numpy array of shape (H, W, C) or a
                PIL Image object.
        Returns:
            (numpy.ndarray): The center-cropped and resized image as a numpy array of shape (self.h, self.w, C).
        Examples:
            >>> transform = CenterCrop(size=224)
            >>> image = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
            >>> cropped_image = transform(image)
            >>> assert cropped_image.shape == (224, 224, 3)
        '''
        # Convert PIL to numpy if needed
        pil_input = False
        try:
            from PIL import Image
            pil_cls = Image.Image
        except Exception:
            pil_cls = None

        if pil_cls is not None and isinstance(im, pil_cls):
            pil_input = True
            im = np.asarray(im)

        if not isinstance(im, np.ndarray):
            raise TypeError("Input must be a numpy.ndarray or PIL.Image.Image")

        if im.ndim not in (2, 3):
            raise ValueError(
                "Input numpy array must have 2 (H, W) or 3 (H, W, C) dimensions")

        H, W = im.shape[:2]
        target_h, target_w = self.h, self.w

        if H == 0 or W == 0:
            raise ValueError("Input image has zero-sized dimension")

        # Compute scale so that resized image covers target (no padding needed), then center-crop
        scale_h = target_h / H
        scale_w = target_w / W
        scale = max(scale_h, scale_w)

        # Compute new dimensions, ensure they are at least target via ceil
        new_h = int(np.ceil(H * scale))
        new_w = int(np.ceil(W * scale))

        if new_h <= 0 or new_w <= 0:
            raise ValueError("Computed resized dimensions are invalid")

        # Resize
        resized = self._resize(im, new_w, new_h, upsample=scale > 1.0)

        # Center crop
        start_y = max((new_h - target_h) // 2, 0)
        start_x = max((new_w - target_w) // 2, 0)
        end_y = start_y + target_h
        end_x = start_x + target_w

        # In case of off-by-one due to rounding, clip indices
        start_y = min(start_y, max(new_h - target_h, 0))
        start_x = min(start_x, max(new_w - target_w, 0))
        end_y = min(end_y, new_h)
        end_x = min(end_x, new_w)

        cropped = resized[start_y:end_y,
                          start_x:end_x, ...] if resized.ndim == 3 else resized[start_y:end_y, start_x:end_x]

        # Ensure final shape is exactly (target_h, target_w, C) or (target_h, target_w)
        if cropped.shape[0] != target_h or cropped.shape[1] != target_w:
            # As a safety net, pad or trim
            pad_h = max(0, target_h - cropped.shape[0])
            pad_w = max(0, target_w - cropped.shape[1])
            if pad_h > 0 or pad_w > 0:
                if cropped.ndim == 3:
                    pad_spec = ((0, pad_h), (0, pad_w), (0, 0))
                else:
                    pad_spec = ((0, pad_h), (0, pad_w))
                cropped = np.pad(cropped, pad_spec, mode='edge')
            cropped = cropped[:target_h,
                              :target_w, ...] if cropped.ndim == 3 else cropped[:target_h, :target_w]

        return cropped

    def _resize(self, img: np.ndarray, new_w: int, new_h: int, upsample: bool) -> np.ndarray:
        # Try OpenCV first for speed
        try:
            import cv2
            interp = cv2.INTER_LINEAR if upsample else cv2.INTER_AREA
            # cv2 expects (width, height)
            resized = cv2.resize(img, (new_w, new_h), interpolation=interp)
            # If original had channel dim 1 and cv2 squeezed it, reshape back
            if img.ndim == 3 and resized.ndim == 2:
                resized = resized[:, :, np.newaxis]
            return resized
        except Exception:
            # Fallback to PIL
            try:
                from PIL import Image
                if img.ndim == 2:
                    mode = 'L'
                else:
                    # Determine mode based on channels
                    c = img.shape[2]
                    if c == 1:
                        mode = 'L'
                        img = img.squeeze(axis=2)
                    elif c == 3:
                        mode = 'RGB'
                    elif c == 4:
                        mode = 'RGBA'
                    else:
                        # For arbitrary channels, resize each channel independently
                        channels = [self._resize(
                            img[..., i], new_w, new_h, upsample) for i in range(c)]
                        return np.stack(channels, axis=2)

                pil_img = Image.fromarray(img, mode=mode) if mode in (
                    'L', 'RGB', 'RGBA') else Image.fromarray(img)
                resample = Image.Resampling.BILINEAR if upsample else Image.Resampling.LANCZOS
                pil_resized = pil_img.resize((new_w, new_h), resample=resample)
                arr = np.asarray(pil_resized)
                if mode == 'L' and arr.ndim == 2 and (img.ndim == 3 and img.shape[2] == 1):
                    arr = arr[:, :, np.newaxis]
                return arr
            except Exception as e:
                raise RuntimeError(
                    f"Failed to resize image using both cv2 and PIL: {e}")
