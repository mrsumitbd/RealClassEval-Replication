from pkg_resources import parse_version

class UpgradeSteps:

    def __init__(self):
        self.steps = []

    def add(self, version):

        def decorator(func):
            self.steps.append((parse_version(version), func))
            return func
        return decorator

    def run(self, persister, from_version, to_version):
        from_version = parse_version(from_version)
        to_version = parse_version(to_version)
        results = []
        for version, func in sorted(self.steps):
            if from_version < version <= to_version:
                results.append(func(persister))
        return results