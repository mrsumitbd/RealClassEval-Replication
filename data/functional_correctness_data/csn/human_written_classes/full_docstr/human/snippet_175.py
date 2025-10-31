class S2Image:
    """
    Additional functionality related to s2i-enabled container images
    """

    def extend(self, source, new_image_name, s2i_args=None):
        """
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails

        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        """
        raise NotImplementedError('extend method is not implemented')

    def usage(self):
        """
        Provide output of `s2i usage`

        :return: str
        """
        raise NotImplementedError('usage method is not implemented')