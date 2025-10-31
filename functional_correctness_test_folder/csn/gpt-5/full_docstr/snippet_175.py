import subprocess
from typing import List, Optional

try:
    from conu.exceptions import ConuException  # type: ignore
except Exception:
    try:
        from conu.errors import ConuException  # type: ignore
    except Exception:
        class ConuException(Exception):
            pass


class S2Image:
    '''
    Additional functionality related to s2i-enabled container images
    '''

    def __init__(self, image_name: str):
        self.image_name = image_name

    def extend(self, source, new_image_name, s2i_args: Optional[List[str]] = None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        if s2i_args is None:
            s2i_args = []
        if not isinstance(s2i_args, list):
            raise ConuException("s2i_args must be a list of strings")
        cmd = ["s2i", "build", str(source), str(self.image_name), str(
            new_image_name)] + [str(a) for a in s2i_args]
        try:
            res = subprocess.run(
                cmd, check=False, capture_output=True, text=True)
        except FileNotFoundError as e:
            raise ConuException("s2i executable not found") from e
        if res.returncode != 0:
            msg = res.stderr.strip() or res.stdout.strip() or "s2i build failed"
            raise ConuException(msg)
        return S2Image(new_image_name)

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        cmd = ["s2i", "usage", str(self.image_name)]
        try:
            res = subprocess.run(
                cmd, check=False, capture_output=True, text=True)
        except FileNotFoundError as e:
            raise ConuException("s2i executable not found") from e
        if res.returncode != 0:
            msg = res.stderr.strip() or res.stdout.strip() or "s2i usage failed"
            raise ConuException(msg)
        return res.stdout.rstrip("\n")
