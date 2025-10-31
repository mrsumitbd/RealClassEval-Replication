
import subprocess
from typing import List, Optional

try:
    from conu.exceptions import ConuException
except ImportError:
    class ConuException(Exception):
        pass


class S2Image:
    def extend(
        self,
        source: str,
        new_image_name: str,
        s2i_args: Optional[List[str]] = None,
    ) -> "S2Image":
        """
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        """
        cmd = ["s2i", "build", source, new_image_name]
        if s2i_args:
            cmd.extend(s2i_args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise ConuException(
                f"s2i build failed with exit code {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

        return self

    def usage(self) -> str:
        """
        Provide output of `s2i usage`
        :return: str
        """
        result = subprocess.run(
            ["s2i", "usage"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise ConuException(
                f"s2i usage failed with exit code {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

        return result.stdout
