import subprocess
from typing import List, Optional


class S2Image:

    def extend(self, source, new_image_name, s2i_args: Optional[List[str]] = None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        # ensure ConuException exists
        if 'ConuException' not in globals():
            class ConuException(Exception):
                pass
            globals()['ConuException'] = ConuException

        base_image = (
            getattr(self, 'image', None)
            or getattr(self, 'image_name', None)
            or getattr(self, 'name', None)
        )
        if not base_image:
            raise ConuException(
                "Base image name is not set on this S2Image instance (expected attribute: image, image_name, or name)")

        if not isinstance(source, str) or not source:
            raise ConuException(
                "Parameter 'source' must be a non-empty string")
        if not isinstance(new_image_name, str) or not new_image_name:
            raise ConuException(
                "Parameter 'new_image_name' must be a non-empty string")

        cmd = ["s2i", "build", source, str(base_image), new_image_name]
        if s2i_args:
            if not isinstance(s2i_args, list) or not all(isinstance(a, str) for a in s2i_args):
                raise ConuException(
                    "Parameter 's2i_args' must be a list of strings")
            # insert user args right after 'build' to allow flags before positional args
            cmd = ["s2i", "build"] + s2i_args + \
                [source, str(base_image), new_image_name]

        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True,
            )
        except FileNotFoundError as e:
            raise ConuException("s2i binary not found in PATH") from e

        if res.returncode != 0:
            msg = f"s2i build failed with exit code {res.returncode}"
            if res.stderr:
                msg += f"\nstderr:\n{res.stderr.strip()}"
            if res.stdout:
                msg += f"\nstdout:\n{res.stdout.strip()}"
            raise ConuException(msg)

        new_obj = type(self)()
        # set commonly used attributes for the new image
        setattr(new_obj, 'image_name', new_image_name)
        setattr(new_obj, 'name', new_image_name)
        setattr(new_obj, 'image', new_image_name)
        return new_obj

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        if 'ConuException' not in globals():
            class ConuException(Exception):
                pass
            globals()['ConuException'] = ConuException

        base_image = (
            getattr(self, 'image', None)
            or getattr(self, 'image_name', None)
            or getattr(self, 'name', None)
        )
        if not base_image:
            raise ConuException(
                "Base image name is not set on this S2Image instance (expected attribute: image, image_name, or name)")

        cmd = ["s2i", "usage", str(base_image)]
        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True,
            )
        except FileNotFoundError as e:
            raise ConuException("s2i binary not found in PATH") from e

        if res.returncode != 0:
            msg = f"s2i usage failed with exit code {res.returncode}"
            if res.stderr:
                msg += f"\nstderr:\n{res.stderr.strip()}"
            if res.stdout:
                msg += f"\nstdout:\n{res.stdout.strip()}"
            raise ConuException(msg)

        return res.stdout or ""
