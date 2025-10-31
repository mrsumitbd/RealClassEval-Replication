class ToTensorImage:
    """
    Convert tensor data type from uint8 to float, divide value by 255.0 and
    permute the dimensions of clip tensor
    """

    def __init__(self):
        pass

    def __call__(self, image):
        """
        Args:
            image (torch.tensor, dtype=torch.uint8): Size is (C, H, W)
        Return:
            image (torch.tensor, dtype=torch.float): Size is (C, H, W)
        """
        return to_tensor_image(image)

    def __repr__(self) -> str:
        return self.__class__.__name__