from spython.utils import split_uri

class ImageBase:

    def __str__(self):
        protocol = getattr(self, 'protocol', None)
        if protocol:
            return '%s://%s' % (protocol, self.image)
        return self.image

    def __repr__(self):
        return self.__str__()

    def parse_image_name(self, image):
        """
        simply split the uri from the image. Singularity handles
        parsing of registry, namespace, image.

        Parameters
        ==========
        image: the complete image uri to load (e.g., docker://ubuntu)

        """
        self._image = image
        self.protocol, self.image = split_uri(image)