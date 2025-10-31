
import subprocess


class ConuException(Exception):
    pass


class S2Image:
    def __init__(self, image_name):
        self.image_name = image_name

    def extend(self, source, new_image_name, s2i_args=None):
        cmd = ["s2i", "build", source, self.image_name, new_image_name]
        if s2i_args:
            cmd.extend(s2i_args)
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        except subprocess.CalledProcessError as e:
            raise ConuException(f"s2i build failed: {e.stderr.strip()}")
        return S2Image(new_image_name)

    def usage(self):
        cmd = ["s2i", "usage", self.image_name]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise ConuException(f"s2i usage failed: {e.stderr.strip()}")
