class ShaderSource:
    """
    Helper class representing a single shader type
    """

    def __init__(self, shader_type: str, name: str, source: str):
        self.type = shader_type
        self.name = name
        self.source = source.strip()
        self.lines = self.source.split('\n')
        if not self.lines[0].startswith('#version'):
            self.print()
            raise ShaderError('Missing #version in {}. A version must be defined in the first line'.format(self.name))
        self.lines.insert(1, '#define {} 1'.format(self.type))
        self.source = '\n'.join(self.lines)

    def find_out_attribs(self):
        """
        Get all out attributes in the shader source.

        :return: List of attribute names
        """
        names = []
        for line in self.lines:
            if line.strip().startswith('out '):
                names.append(line.split()[2].replace(';', ''))
        return names

    def print(self):
        """Print the shader lines"""
        print('---[ START {} ]---'.format(self.name))
        for i, line in enumerate(self.lines):
            print('{}: {}'.format(str(i).zfill(3), line))
        print('---[ END {} ]---'.format(self.name))