
class Pattern:

    def __init__(self, spec, inclusive):
        self.spec = spec
        self.inclusive = inclusive

    def __str__(self):
        return f"Pattern(spec={self.spec}, inclusive={self.inclusive})"

    def matches(self, path):
        if not self.spec:
            return self.inclusive

        spec_parts = self.spec.split('/')
        path_parts = path.split('/')

        if len(spec_parts) != len(path_parts):
            return False

        for spec_part, path_part in zip(spec_parts, path_parts):
            if spec_part == '**':
                continue
            if spec_part == '*':
                if not path_part:
                    return False
                continue
            if spec_part != path_part:
                return False

        return self.inclusive
