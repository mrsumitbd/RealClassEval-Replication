
class S2Image:
    '''
    Additional functionality related to s2i-enabled container images
    '''

    def extend(self, source, new_image_name, s2i_args=None):
        '''
        extend this s2i-enabled image using provided source, raises ConuException if
        `s2i build` fails
        :param source: str, source used to extend the image, can be path or url
        :param new_image_name: str, name of the new, extended image
        :param s2i_args: list of str, additional options and arguments provided to `s2i build`
        :return: S2Image instance
        '''
        import subprocess
        from conu import ConuException

        if s2i_args is None:
            s2i_args = []

        try:
            subprocess.run(['s2i', 'build', source, self.image_name,
                           new_image_name] + s2i_args, check=True)
        except subprocess.CalledProcessError as e:
            raise ConuException(f"Failed to extend image: {e}")

        return S2Image(new_image_name)

    def usage(self):
        '''
        Provide output of `s2i usage`
        :return: str
        '''
        import subprocess

        result = subprocess.run(
            ['s2i', 'usage'], capture_output=True, text=True)
        return result.stdout
