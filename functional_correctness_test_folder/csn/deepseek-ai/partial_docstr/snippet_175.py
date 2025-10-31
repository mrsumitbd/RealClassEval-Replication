
import subprocess
from subprocess import CalledProcessError


class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        cmd = ['s2i', 'build', source, self.__class__.__name__, new_image_name]
        if s2i_args:
            cmd.extend(s2i_args)
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except CalledProcessError as e:
            raise ConuException(f"s2i build failed: {e.stderr}") from e
        return S2Image()

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        result = subprocess.run(
            ['s2i', 'usage', self.__class__.__name__], capture_output=True, text=True)
        return result.stdout


class ConuException(Exception):
    pass
