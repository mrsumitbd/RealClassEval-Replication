
import subprocess
from conu.exceptions import ConuException


class S2Image:
    '''
    Additional functionality related to s2i-enabled container images
    '''

    def __init__(self, image_name):
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
        command = ['s2i', 'build', source, self.image_name, new_image_name]
        if s2i_args:
            command.extend(s2i_args)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise ConuException(f"Failed to build image: {e}")
        return S2Image(new_image_name)

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        try:
            result = subprocess.run(['s2i', 'usage', self.image_name],
                                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            raise ConuException(
                f"Failed to get usage: {e.stderr.decode('utf-8')}")
