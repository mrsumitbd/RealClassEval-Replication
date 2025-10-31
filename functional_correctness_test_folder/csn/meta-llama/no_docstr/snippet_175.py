
import subprocess
import os


class S2Image:
    def __init__(self, s2i_binary='s2i'):
        """
        Initialize the S2Image class.

        :param s2i_binary: The path to the s2i binary. Defaults to 's2i'.
        """
        self.s2i_binary = s2i_binary

    def extend(self, source, new_image_name, s2i_args=None):
        """
        Extend an existing image using s2i.

        :param source: The source directory or archive.
        :param new_image_name: The name of the new image.
        :param s2i_args: Additional arguments to pass to s2i. Defaults to None.
        """
        command = [self.s2i_binary, 'build', source, new_image_name]
        if s2i_args:
            command.extend(s2i_args)
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"s2i build failed with return code {e.returncode}")

    def usage(self):
        """
        Print the usage of the s2i command.
        """
        try:
            subprocess.check_call([self.s2i_binary, '--help'])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"s2i --help failed with return code {e.returncode}")
        except FileNotFoundError:
            print("s2i binary not found. Please ensure it is installed and in your PATH.")


# Example usage:
if __name__ == "__main__":
    s2_image = S2Image()
    s2_image.usage()
    # s2_image.extend('/path/to/source', 'new-image-name')
