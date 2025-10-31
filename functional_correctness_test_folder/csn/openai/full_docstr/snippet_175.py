
import subprocess
from typing import List, Optional

# Try to import ConuException from the conu package; fall back to a local definition if unavailable.
try:
    from conu.exceptions import ConuException
except Exception:  # pragma: no cover
    class ConuException(Exception):
        """Fallback ConuException if the real one cannot be imported."""
        pass


class S2Image:
    """
    Additional functionality related to s2i-enabled container images.
    """

    def __init__(self, image_name: str):
        """
        Initialize an S2Image instance.

        :param image_name: Name of the s2i-enabled image.
        """
        self.image_name = image_name

    def extend(
        self,
        source: str,
        new_image_name: str,
        s2i_args: Optional[List[str]] = None,
    ) -> "S2Image":
        """
        Extend this s2i-enabled image using the provided source. Raises
        ConuException if `s2i build` fails.

        :param source: Source used to extend the image, can be a path or URL.
        :param new_image_name: Name of the new, extended image.
        :param s2i_args: Additional options and arguments provided to `s2i build`.
        :return: S2Image instance representing the new image.
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
                f"s2i build failed (return code {result.returncode}): {result.stderr.strip()}"
            )

        return S2Image(new_image_name)

    def usage(self) -> str:
        """
        Provide output of `s2i usage`.

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
                f"s2i usage failed (return code {result.returncode}): {result.stderr.strip()}"
            )

        return result.stdout.strip()
