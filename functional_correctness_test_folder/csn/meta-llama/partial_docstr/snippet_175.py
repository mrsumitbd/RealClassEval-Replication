
import subprocess
from conu.exceptions import ConuException


class S2Image:
    def __init__(self, image_name):
        """
        Initialize S2Image instance.

        :param image_name: str, name of the s2i-enabled image
        """
        self.image_name = image_name

    def extend(self, source, new_image_name, s2i_args=None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        s2i_command = ["s2i", "build"]
        if s2i_args:
            s2i_command.extend(s2i_args)
        s2i_command.extend([source, self.image_name, new_image_name])
        try:
            subprocess.check_output(s2i_command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ConuException(
                f"s2i build failed: {e.output.decode('utf-8')}")
        return S2Image(new_image_name)

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        s2i_command = ["s2i", "usage", self.image_name]
        try:
            output = subprocess.check_output(
                s2i_command, stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            raise ConuException(
                f"s2i usage failed: {e.output.decode('utf-8')}")
