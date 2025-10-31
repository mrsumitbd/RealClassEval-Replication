
class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        import subprocess
        from conu import ConuException

        s2i_args = s2i_args or []
        command = ['s2i', 'build', source,
                   self.name, new_image_name] + s2i_args
        try:
            subprocess.run(command, check=True)
            return S2Image(new_image_name)
        except subprocess.CalledProcessError:
            raise ConuException(
                f"Failed to extend image with command: {' '.join(command)}")

    def usage(self):
        import subprocess

        command = ['s2i', 'usage', self.name]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(
                f"Failed to get usage information with command: {' '.join(command)}")
        return result.stdout

    def __init__(self, name):
        self.name = name
