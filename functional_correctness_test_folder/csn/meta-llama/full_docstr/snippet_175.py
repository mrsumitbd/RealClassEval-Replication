
import subprocess
from conu import ConuException


class S2Image:
    '''
    Additional functionality related to s2i-enabled container images
    '''

    def __init__(self, image):
        '''
        :param image: DockerImage or similar instance
        '''
        self.image = image

    def extend(self, source, new_image_name, s2i_args=None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        s2i_cmd = ["s2i", "build"]
        if s2i_args:
            s2i_cmd.extend(s2i_args)
        s2i_cmd.extend([source, self.image.name, new_image_name])
        try:
            subprocess.check_output(s2i_cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            raise ConuException(
                f"s2i build failed: {ex.output.decode('utf-8')}")
        return S2Image(self.image.get_DockerImage_instance().tag(new_image_name))

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        s2i_cmd = ["s2i", "usage", self.image.name]
        try:
            output = subprocess.check_output(s2i_cmd, stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except subprocess.CalledProcessError as ex:
            raise ConuException(
                f"s2i usage failed: {ex.output.decode('utf-8')}")
