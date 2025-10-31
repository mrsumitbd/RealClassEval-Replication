
class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        import subprocess
        from conu import ConuException

        if s2i_args is None:
            s2i_args = []

        cmd = ['s2i', 'build', source,
               self.image_name, new_image_name] + s2i_args
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise ConuException(f"Failed to extend image: {e}")

        return S2Image(new_image_name)

    def usage(self):
        import subprocess

        cmd = ['s2i', 'usage']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
